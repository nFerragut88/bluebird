from app import app
import os, redis

app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT',8080)), debug=True)


