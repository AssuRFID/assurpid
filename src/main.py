#!/usr/bin/env python3
# assurpid: Listen for nfc tags and check them against an SQL database

import nfc
import signal
import sys

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

# Clean up

nfc.close(pnd)
nfc.exit(context)
