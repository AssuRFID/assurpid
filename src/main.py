#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nfc
import time
import signal
import sys
import sqlite3
import RPi.GPIO as GPIO

def light_on(colour):
    colours = {'red': [1,0,0], 'green': [0,1,0], 'blue': [0,0,1],\
            'yellow': [1,1,0], 'cyan': [0,1,1], 'magenta': [1,0,1],\
            'white': [1,1,1], True: [1,1,1],\
            'black': [0,0,0], 'off': [0,0,0], False: [0,0,0], None: [0,0,0]}
    pins = {'red': 18, 'green': 23, 'blue': 24}
    if colour in colours:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pins['red'], GPIO.OUT)
        GPIO.setup(pins['green'], GPIO.OUT)
        GPIO.setup(pins['blue'], GPIO.OUT)

        GPIO.output(pins['red'], colours[colour][0])
        GPIO.output(pins['green'], colours[colour][1])
        GPIO.output(pins['blue'], colours[colour][2])
    else:
        print("Not a valid colour.")

def clean_up():
    nfc.close(pnd)
    nfc.exit(context)
    conn.close()

def signal_handler(signal, frame):
    clean_up()
    sys.exit(0)

sleep_time = 2

# Ensure ^C doesn't corrupt/leave anything broken.
signal.signal(signal.SIGINT, signal_handler)

conn = sqlite3.connect('/var/db/assurpid/assurpid.db')
print('opened database successfully')

print('libnfc version: ', nfc.__version__)

context = nfc.init()
pnd = nfc.open(context)
if pnd is None:
    print('ERROR: Unable to detect RFID sensor (run this as root).')
    exit()

if nfc.initiator_init(pnd) < 0:
    nfc.perror(pnd, "nfc_initiator_init")
    print('ERROR: Unable to init RFID sensor.')
    exit()

print('NFC reader: %s opened' % nfc.device_get_name(pnd))

nmMifare = nfc.modulation()
nmMifare.nmt = nfc.NMT_ISO14443A
nmMifare.nbr = nfc.NBR_106

nt = nfc.target()

admin_switch = False

while True:
    if not admin_switch:
        GPIO.cleanup()

    print()

    # Wait for tag
    ret = nfc.initiator_select_passive_target(pnd, nmMifare, 0, 0, nt)

    # Convert raw uid to hex, then trim to length (2*nt.nti.nai.szUidLen)
    tag = ''.join(format(x, '02x') for x in nt.nti.nai.abtUid)[:2*nt.nti.nai.szUidLen]
    print('Found tag with UID of', tag)
    cursor = conn.cursor()
    cursor.execute("SELECT UID, ADMIN, ACCESS_ROOM1, INSIDE_ROOM1 FROM MAIN WHERE UID = ?", (tag,))
    details = cursor.fetchone()

    if details is None:
        print("Tag is unrecognised")
        light_on('red')
        if admin_switch:
            conn.execute("INSERT INTO MAIN(UID, ADMIN, ACCESS_ROOM1, INSIDE_ROOM1) VALUES(?, 0, 1, 0)", (tag,))
            conn.commit()
            admin_switch = False
            light_on('green')
            print("Added tag to database")
        time.sleep(sleep_time)
        continue
    else:
        print("Tag is recognised")
        if admin_switch and details[1] == 0:
            conn.execute("DELETE FROM MAIN WHERE UID = ?", (tag,))
            conn.commit()
            admin_switch = False
            light_on('red')
            print("Deleted tag from database")
            time.sleep(sleep_time)
            continue

    if details[1] == 1:
        print("Tag is admin.")
        light_on('magenta')
        admin_switch = True
        time.sleep(sleep_time)
        continue

    if details[3] == 1:
        print("Tag is inside Room 1.")
    else:
        print("Tag is outside Room 1.")

    if details[2] == 1:
        print("Tag can open door to Room 1.")
        light_on('green')
    else:
        print("Tag cannot open door to Room 1.")
        light_on('blue')
    
    if details[2] == 1 and details[3]:
        conn.execute("UPDATE MAIN SET INSIDE_ROOM1 = 0 WHERE UID = ?", (tag,))
        print("Door opened from inside, tag now outside.")
    
    if details[2] == 1 and details[3] == 0:
        conn.execute("UPDATE MAIN SET INSIDE_ROOM1 = 1 WHERE UID = ?", (tag,))
        print("Door opened from outside, tag now inside.")
    time.sleep(sleep_time)

clean_up()
sys.exit(0)
