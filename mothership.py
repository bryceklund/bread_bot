from send_tweet import send_tweet
from get_breads import get_breads
import random
import time
from datetime import datetime, timedelta
from threading import Timer

today = datetime.today()
target = today.replace(day=today.day, hour=23, minute=20, second=0, microsecond=0) + timedelta(days=1)
delta_t = target - today

secs = delta_t.total_seconds()
breads = get_breads()

def tweet_breads():
    success = False
    while not success: # catch failing posts
        print('grabbing a bread...')
        bread = random.choice(breads)
        print('bread grabbed. building tweet...')
        result = send_tweet(bread)
        success = result
print('target time: ', target)
print('current time: ', datetime.now())
print('seconds until next tweet: ', secs)
t = Timer(secs, tweet_breads)
t.start()
tweet_breads()
