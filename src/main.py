#!/usr/bin/env python3
# assurpid: Listen for nfc tags and check them against an SQL database

import nfc
import signal
import sys

# Define cleanup function, used on exit
def clean_up():
    nfc.close(pnd)
    nfc.exit(context)

# Make sure ^C does not mess anything up
def signal_handler(signal, frame):
    clean_up()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler) 

# Initialise NFC
context = nfc.init()
pnd = nfc.open(context)

if pnd is None:
    print('ERROR: unable to open NFC device (this program requires root privileges).')
    exit()

if nfc.initiator_init(pnd) < 0:
    nfc.perror(pnd, "nfc_initiator_init")
    print('ERROR: unable to init NFC device')
    exit()

print('NFC reader %s opened' % nfc.device_get_name(pnd))

nm = nfc.modulation()

while True:
    tag_number, tag = nfc.initiator_list_passive_targets(pnd, nm, 1)        # tag_number contains number of tags detected, tag contains their names
    
    if (tag_number > 0):
        print("Detected tag...")
        nfc.print_nfc_target(tag, verbose)

# Clean up
clean_up()
