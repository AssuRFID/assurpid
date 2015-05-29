#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nfc
import time
import signal
import sys

def clean_up():
    nfc.close(pnd)
    nfc.exit(context)

def signal_handler(signal, frame):
    clean_up()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print('Version: ', nfc.__version__)

context = nfc.init()
pnd = nfc.open(context)
if pnd is None:
    print('ERROR: Unable to open NFC device.')
    exit()

if nfc.initiator_init(pnd) < 0:
    nfc.perror(pnd, "nfc_initiator_init")
    print('ERROR: Unable to init NFC device.')
    exit()

print('NFC reader: %s opened' % nfc.device_get_name(pnd))

nmMifare = nfc.modulation()
nmMifare.nmt = nfc.NMT_ISO14443A
nmMifare.nbr = nfc.NBR_106

nt = nfc.target()

while True:
    # Wait for tag
    ret = nfc.initiator_select_passive_target(pnd, nmMifare, 0, 0, nt)
    # Convert raw uid to hex, then trim to length (2*nt.nti.nai.szUidLen)
    tag = ''.join(format(x, '02x') for x in nt.nti.nai.abtUid)[:2*nt.nti.nai.szUidLen]
    print('Found tag with UID of', tag)
    time.sleep(1)

nfc.close(pnd)
nfc.exit(context)
