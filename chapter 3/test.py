from MongoCache import MongoCache
from datetime import datetime, timedelta
import time

print(int(timedelta(seconds=5).total_seconds()))
print(datetime.now())
print(datetime.utcnow())

cache = MongoCache(expires=timedelta(seconds=600))


url='baidu'
result = {'html': 'what'}
cache[url]=result # 如果有赋值出现，引用set方法
print(cache[url])

time.sleep(1)

cache['urls'] # 引用get方法

print(cache[url])
