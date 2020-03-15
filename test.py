import random
import time
from datetime import datetime, timedelta
from threading import Timer

def hello():
    print('hello')

t = Timer(10, hello())
t.start()