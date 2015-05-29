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
    ret = nfc.initiator_select_passive_target(pnd, nmMifare, 0, 0, nt)
    print('The following (NFC) ISO14443A tag was found:')
    id = 1
    if nt.nti.nai.abtUid[0] == 8:
        id = 3
    print('       UID (NFCID%d): ' % id , end='')
    nfc.print_hex(nt.nti.nai.abtUid, nt.nti.nai.szUidLen)
    time.sleep(1)

nfc.close(pnd)
nfc.exit(context)
