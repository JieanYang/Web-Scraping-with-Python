from datetime import datetime, timedelta
from pymongo import MongoClient
import pymongo

class MongoCache:
	def __init__(self, client=None, expires=timedelta(days=30)):
		if client is None:
			client = MongoClient('localhost', 27017)
		else:
			self.db = client.db
		self.db = client.cache
		# 创造了一个timestamp索引
		# 在达到给定时间戳一定秒数后，MongoDB 可以自动删除记录
		self.db.webpage.create_index('timestamp', expireAfterSeconds=int(expires.total_seconds()))
		
	def __getitem__(self, url):
		"""Load value at this URL
		"""
		record = self.db.webpage.find_one({'_id': url})
		if record:
			return record['result']
		else:
			raise AttributeError(url + " does not exist")
			
	def __setitem__(self, url, result):
		"""Save value for this URL
		"""
		record = {'result': result, 'timestamp': datetime.utcnow()}
		self.db.webpage.update({'_id': url},{'$set': record}, upsert=True)

# print(int(timedelta(seconds=5).total_seconds()))
# print(datetime.now())
# print(datetime.utcnow())
# 数据测试，失效时间为1s，实际情况下会有几分钟的延迟
import time
cache = MongoCache(expires=timedelta(seconds=1))
url='baidu'
result = {'html': 'what'}
cache[url]=result

while(True):	
	print(cache[url])
	time.sleep(10)

