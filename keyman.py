import hashlib
import redis
import sys
import string
import random
import config

#
# Simple CLI tool to create and manage API keys
#

def usage():
    print("Usage: %s COMMAND [keyname]\n" % sys.argv[0])
    print("Where COMMAND is one of: add, delete, list\n")

if len(sys.argv) < 2:
    usage()
    quit()
elif sys.argv[1].lower() not in ["add", "delete", "list"]:
    usage()
    quit()

r = redis.Redis(host=config.REDISDBHOST)

command = sys.argv[1]

if command.lower() == "add":
    if len(sys.argv) < 3:
        usage()
        quit()

    keyname = sys.argv[2]

    # Make sure a key with that name does not already exist and let's force
    # everything lowercase in checking and creating just to keep things simple
    if r.hexists(config.NAMETABLEKEY,  keyname.lower()):
        print("Sorry, that key name is already taken.")
        quit()
    
    # Generate a key
    letters_and_digits = string.ascii_letters + string.digits
    key = keyname + "." + ''.join((random.choice(letters_and_digits) for i in range(48)))

    # Show it to the user
    print("\nPLEASE RECORD THE NEW KEY NOW")
    print("It will be impossible to retreive later\n")
    print("New API Key is:", key + "\n")

    # Hash it
    keyhash = hashlib.sha256(key.encode('utf-8')).hexdigest()

    # Store the key name and the hash in one table
    r.hset(config.NAMETABLEKEY, keyname.lower(), keyhash)
    # Store the hash and the key name in the other table
    r.hset(config.KEYTABLEKEY, keyhash, keyname.lower())

    quit()

if command.lower() == "delete":
    keyname = sys.argv[2]

    # Quit if no such key exists
    if not r.hexists(config.NAMETABLEKEY, keyname):
        print("Sorry, that key does not exist.")
        quit()

    # Still running?  Confirm the user wants to delete the key
    print("\n*** PLEASE CONFIRM AS THIS CAN NOT BE UNDONE ***")
    print("Are you sure you wish to delete the API key named %s?\n" % keyname)
    confirm = input("Type YES to confirm: ")
    if confirm != "YES":
        print("\nNot confirmed, quitting\n")
        quit()

    # Get key hash using name
    keyhash = r.hget(config.NAMETABLEKEY, keyname)
    
    # Delete both records
    r.hdel(config.NAMETABLEKEY, keyname)
    r.hdel(config.KEYTABLEKEY, keyhash)

    # Tell the user we deleted it
    print("\nKey deleted.")
    quit()

if command.lower() == "list":
    # Get list of key names
    list = r.hkeys(config.NAMETABLEKEY)

    # Print list
    for item in list:
        print(item.decode('utf-8'))

    quit()

print("It should not be possible to get here.  How did you get here?")
