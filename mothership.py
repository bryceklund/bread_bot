from send_tweet import send_tweet
from get_breads import get_breads
import random
import time
from datetime import datetime, timedelta
from threading import Timer

today = datetime.today()
target = today.replace(day=today.day, hour=16, minute=20, second=0, microsecond=0) + timedelta(days=1)
delta_t = target - today

secs = delta_t.total_seconds()
breads = get_breads()

def tweet_breads():
    bread = random.choice(breads)
    send_tweet(bread)

tweet_breads()
tweet_breads()
tweet_breads()

t = Timer(secs, tweet_breads)
t.start()