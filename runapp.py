from app import app
import os, redis
# create a connection to the localhost Redis server instance, by
# default it runs on port 6379
redis_db = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)
# see what keys are in Redis host="192.168.0.24"
redis_db.keys()
# output for keys() should be an empty list "[]"
redis_db.set('full stack', 'python')
# output should be "True"
redis_db.keys()
# now we have one key so the output will be "[b'full stack']"
redis_db.get('full stack')
# output is "b'python'", the key and value still exist in Redis

app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT',8080)), debug=True)
