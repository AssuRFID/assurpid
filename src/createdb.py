#!/usr/bin/env python
# A simple program to create a new db for assurpid and/or populate it with cards

import sqlite3
import nfc

# Function to wait for an return a single tag UID. Returns a string.
def get_tag():
    context = nfc.init()
    pnd = nfc.open(context)
    if pnd is None:
        print('ERROR: Unable to open NFC device.')
        exit()
    if nfc.initiator_init(pnd) < 0:
        nfc.perror(pnd, "nfc_initiator_init")
        print('ERROR: Unable to init NFC device.')
        exit()

    # Declare modulations
    nmMifare = nfc.modulation()
    nmMifare.nmt = nfc.NMT_ISO14443A
    nmMifare.nbr = nfc.NBR_106

    nt = nfc.target()
    # Wait for tag
    ret = nfc.initiator_select_passive_target(pnd, nmMifare, 0, 0, nt)
    # Convert raw uid to hex, then trim to length (2*nt.nti.nai.szUidLen)
    tag = ''.join(format(x, '02x') for x in nt.nti.nai.abtUid)[:2*nt.nti.nai.szUidLen]
    nfc.close(pnd)
    nfc.exit(context)

    # Return UID
    return tag 

# Function to ask user a yes/no question. Returns a bool
def query_yes_no(question, defualt):
    valid = {"yes": 1, "y": 1, "no": 0, "n": 0}
    
    if default is None:
        prompt = " [y/n] "
    elif default == "yes" or default == True:
        prompt == " [Y/n] "
    elif default == "no" or default == False:
        prompt == " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        # Ask for yes/no/y/n
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        # If user doesn't type anything and a default was set, the default is returned
        if default is not None and choice == '':
            return valid[default]
        # If the choice is a valid response, return it
        elif choice in valid:
            return valid[choice]
        # Otherwise, loop
        else:
            sys.stdout.write("Please respond with 'yes', 'no', 'y' or 'n'"

conn = sqlite3.connect('/var/db/assurpid/assurpid.db')
print('opened database successfully')

# Creates table with columns (tag id, admin rights, access rights to room1, if inside room1)
conn.execute('''CREATE TABLE IF NOT EXISTS MAIN (UID TEXT, ADMIN INT, ACCESS_ROOM1 INT, INSIDE_ROOM1 INT);''')

run = True

while run:
    print("Place a tag against the sensor")
    newtag = get_tag()
    # check if tag already exists
    conn.execute("SELECT count(*) FROM MAIN WHERE NAME = ?", (newtag,))
    exists = conn.fetchone()[0]

    # If entry does not exist (no result), make a new one
    if exists == 0:
        print("Creating new tag entry with UID", newtag)
        # Ask the user if he wants this to be an admin, and if it can access room1
        admin = query_yes_no("Should this be an administrator?", None)
        access_room1 = query_yes_no("Should this have access to Room 1?", "yes")

        # Insert row with specified values (SQLite doesn't have booleans, so we use ints)
        conn.execute("INSERT INTO MAIN (UID,ADMIN,ACCESS_ROOM1,INSIDE_ROOM1) \
            VALUES (?, ?, ?, 0)", newtag, admin, access_room1)
        # Always commit
        conn.commit()
        print("Records created successfully")

    # Otherwise, update the existing one
    else:
        print("Updating tag entry with UID", newtag)
        # Read existing values for tag
        cursor = conn.execute("SELECT * FROM MAIN WHERE UID = '?'", newtag)
        # Print them for clarity
        for row in cursor:
            print("UID              = ", row[0])
            print("Admin            = ", bool(row[1]))
            print("Access to Room 1 = ", bool(row[2])

        # Then ask to amend them. Existing values (row[x]) are passed to query_yes_no as the default
        admin = query_yes_no("Should this be an administrator?", bool(row[1]))
        access_room1 = query_yes_no("Should this have access to Room 1?", bool(row[2]))

        # Update the database with the updated information
        conn.execute("UPDATE MAIN SET ADMIN = ?, ACCESS_ROOM1 = ? WHERE UID = ?", admin, access_room1, newtag)

        # Always commit!
        conn.commit()
        print("Records updated successfully")

    # Ask to re-run the process. Otherwise terminate.
    run = query_yes_no("Add another tag?", "yes")

conn.close()
