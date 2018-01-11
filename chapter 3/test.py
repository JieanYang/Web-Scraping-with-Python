from MongoCache import MongoCache
from datetime import datetime, timedelta
import time

print(int(timedelta(seconds=5).total_seconds()))
print(datetime.now())
print(datetime.utcnow())
# =============================================================================
# 数据测试，失效时间为1s，实际情况下会有几分钟的延迟
cache = MongoCache(expires=timedelta(seconds=1))
url='baidu'
result = {'html': 'what'}
cache[url]=result

while(True):	
	print(cache[url])
	time.sleep(10)
# ============================================================================
cache = MongoCache(expires=timedelta(seconds=600))


url='baidu'
result = {'html': 'what'}
cache[url]=result # 如果有赋值出现，引用set方法
print(cache[url])

time.sleep(1)

cache['urls'] # 引用get方法

print(cache[url])

# ===================================================================
# 测试压缩功能
cache = MongoCache()
print(cache['http://example.webscraping.com'])