# assurpid
A Raspberry Pi based prototype, written in Python.

## Dependencies:
* [nfc-bindings](https://github.com/xantares/nfc-bindings)
* [libnfc](http://nfc-tools.org/index.php?title=Libnfc)
* [RPi.GPIO](http://sourceforge.net/projects/raspberry-gpio-python)
* [SQLite](https://www.sqlite.org)

## Instructions
1. Firstly run [src/createdb.py](src/createdb.py) as root. This will create the database. Add at least one admin tag, add as many as you like. They will be added to the database.
2. Then you can run [src/main.py](src/main.py) as root. This will run main tag scanning loop.
3. To add tags, scan an admin tag, then the tag you would like to add. To remove a tag, scan an admin tag followed by the one you want to remove.
4. If you want to read the current database entries, run [src/catdb.py](src/catdb.py). It will print them all out.

