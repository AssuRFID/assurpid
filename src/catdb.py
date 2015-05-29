#!/usr/bin/env python
# Simple program to list entries in assurpid sqlite database.

import sqlite3

conn = sqlite3.connect('/var/db/assurpid/assurpid.db')
print('opened database successfully')
print()

cursor = conn.execute("SELECT UID, ADMIN, ACCESS_ROOM1, INSIDE_ROOM1 FROM MAIN")
for row in cursor:
    print("For tag with UID ", row[0])
    print("Admin rights?    ", row[1])
    print("Access to Room 1?", row[2])
    print("Inside Room 1?   ", row[3])
    print()

conn.close()
