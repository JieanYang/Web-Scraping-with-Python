import re
import pickle
import os
import zlib
url = 'http://example.webscraping.com/places/default/view/Antarctica-9'
a = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', url)
c = a+'/'
print(a)
print(c)



filename = '/'.join(segment[:255] for segment in a.split('/'))
print('12312')
print(filename)

print(c.split('/'))
print('/'.join(segment[:3] for segment in c.split('/')))

path = r'C:\Users\yang\Desktop\Web Scraping with Python\chapter 3\test.txt'
if os.path.exists(path):
	with open(path, 'rb') as fp:
		# 写入文件，模式为 wb
		# fp.write(zlib.compress(pickle.dumps('result')))
		# 读取文件，模式为 rb
		print(pickle.loads(zlib.decompress(fp.read())))
