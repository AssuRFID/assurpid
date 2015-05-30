# assurpid
A Raspberry Pi based prototype, written in Python. It is released under the BSD 2-Clause license.

## Dependencies
* [nfc-bindings](https://github.com/xantares/nfc-bindings)
* [libnfc](http://nfc-tools.org/index.php?title=Libnfc)
* [RPi.GPIO](http://sourceforge.net/projects/raspberry-gpio-python)
* [SQLite](https://www.sqlite.org)

## Instructions
1. Wire up the NFC as described [here](https://www.adrive.com/public/Tw4su6/NFC_PN532.pdf)
1. To enable SPI, required for NFC, copy [confix.txt](config.txt) to `/boot`, then reboot.
1. Then run [src/createdb.py](src/createdb.py) as root. This will create the database. Add at least one admin tag, add as many as you like. They will be added to the database.
1. Then you can run [src/main.py](src/main.py) as root. This will run main tag scanning loop.
1. To add tags, scan an admin tag, then the tag you would like to add. To remove a tag, scan an admin tag followed by the one you want to remove.
1. If you want to read the current database entries, run [src/catdb.py](src/catdb.py). It will print them all out.

## Using systemd
To make use of systemd for service startup and logging:
1. Link main.py to /usr/local/bin/assurpid.py (`ln -s /path/to/assurpid/src/main.py /usr/local/bin/assurpid.py`)
1. Copy `assurpid.service` to `/etc/systemd/system/`
1. Reload systemd (`systemctl daemon-reload`)
1. Start the service with `systemctl start assurpid`. You can start it on boot with `systemctl enable assurpid`.
1. To read journal entries (output) run `journalctl -u assurpid`.
