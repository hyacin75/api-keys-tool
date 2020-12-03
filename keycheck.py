import hashlib
import redis
import sys
import config

#
# Just a very simple example of how key checking could be implemented on the API end
# using the keys generated and inserted into the Redis DB by keyman.py
#

def usage():
    print("Usage: %s APIKEY\n" % sys.argv[0])

if len(sys.argv) < 2:
    usage()
    quit()

r = redis.Redis(host=config.REDISDBHOST)

apikey = sys.argv[1]

keyhash = hashlib.sha256(apikey.encode('utf-8')).hexdigest()

if not r.hexists(config.KEYTABLEKEY, keyhash):
    # In an actual API at this point you'll want to return a 401 I suppose
    print("Sorry, that key does not exist.")
    quit()

# Still running?  Key is valid
print("APIKEY passes check")
