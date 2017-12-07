import re
import urllib.request as urllib2
import urllib.parse as urlparse
import time
from datetime import datetime
import urllib.robotparser as robotparser
import queue as Queue

def F(x, y=3):
	print(x, y)

seen = {'seed_url': 0}
print(type(seen))
F(y=4, x=2)
tup1=("all",)
print(tup1)
print(type(tup1))
crawl_queue = Queue.deque(['seed_url'])
print(crawl_queue)
b = Queue.Queue()
print(type(b))
headers = None or {}
headers['User-agent'] = 'user_agent'
print(headers)
a = Queue.deque(['a', 'b', 'c'])
print(type(a))
print(a)
print('pop',a.pop())
print(a)

original = 'http://netloc/path;param?query=arg#frag'
print ('original:', original)
url, fragment = urlparse.urldefrag(original)
print ('url :', url)
print ('fragment:', fragment)

dic = {'a': 1, 'b': 2, 'c': 3}
str = 'c'
if str in dic:
	print (dic.get(str))