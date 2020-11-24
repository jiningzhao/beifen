import redis
import time

r = redis.Redis(host='0.0.0.0', port=6379)
ACCESS_TOKEN = '123123123123123123'
r.set('token', ACCESS_TOKEN, px=60000)
p = r.get('token')
print(p)
