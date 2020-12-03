# Simple API Key implementation and management tool

This is just a very simple implementation of API key generation, storage into a
Redis DB, and checking against that DB to make sure a key is valid.

When I was trying to find an example of how to do this, or even a page that simply
discussed doing this, all I could find was things for managing keys from a client
perspective - Vault and such.  Nothing for how to do it on the API end - except
overly complex (for my use case) OAuth2 type stuff, and other things along that vein.

All the security here goes right out the window if there is no SSL/TLS obviously -
and I really wouldn't use to to secure anything extremely important - I just wanted
to make something just sufficient to be able to tell 'Security' at my organization -
"Yes, we use API keys."

It's not perfect _I'm sure_, but it would certainly do the trick.

## Synoposis

```
me@manager:~/apikeys$ python3 keyman.py
Usage: keyman.py COMMAND [keyname]

Where COMMAND is one of: add, delete, list

me@manager:~/apikeys$ python3 keyman.py list
mytestkey
me@manager:~/apikeys$ python3 keyman.py add testkey

PLEASE RECORD THE NEW KEY NOW
It will be impossible to retreive later

New API Key is: testkey.ZQTXZ88jEP2Oy8PTwx3nOfxpqUMyivtEorLCuJaIgBLKhezl

me@manager:~/apikeys$ python3 keycheck.py testkey.ZQTXZ88jEP2Oy8PTwx3nOfxpqUMyivtEorLCuJaIgBLKhezl
APIKEY passes check
me@manager:~/apikeys$ python3 keycheck.py testkey.ZQTXZ88jEP2Oy8PTwx3nOfxpqUMyivtEorLCuJaIgBLKhez0
Sorry, that key does not exist.
me@manager:~/apikeys$ python3 keyman.py list
mytestkey
testkey
me@manager:~/apikeys$ python3 keyman.py delete testkey

*** PLEASE CONFIRM AS THIS CAN NOT BE UNDONE ***
Are you sure you wish to delete the API key named testkey?

Type YES to confirm: YES

Key deleted.
me@manager:~/apikeys$ python3 keyman.py list
mytestkey
me@manager:~/apikeys$ python3 keycheck.py testkey.ZQTXZ88jEP2Oy8PTwx3nOfxpqUMyivtEorLCuJaIgBLKhezl
Sorry, that key does not exist.
me@manager:~/apikeys$
```

## Config

The config.py file contains all the variables, they're entirely self-explanatory -

```
me@manager:~/apikeys$ cat config.py
REDISDBHOST = 'my.redis.server'
KEYTABLEKEY = 'apikeys'
NAMETABLEKEY = 'keynames'
me@manager:~/apikeys$
```
