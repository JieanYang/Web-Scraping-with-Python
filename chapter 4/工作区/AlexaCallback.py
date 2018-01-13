import csv
import codecs
import zipfile as ZipFile

class AlexaCallback:
	def __init__(self, max_urls=1000):
		self.max_urls = max_urls
		self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

	def __call__(self, url, html):
		if url == self.seed_url:
			urls = []

			zf = ZipFile.ZipFile(r'C:\Users\yang\Desktop\Web Scraping with Python\chapter 4\工作区\top-1m.csv.zip')
			zf.extract(zf.namelist()[0])
			zf.close()

			csvfile = codecs.open(r'C:\Users\yang\Desktop\Web Scraping with Python\chapter 4\工作区\top-1m.csv', 'r+', 'utf_8_sig')

			for _, website in csv.reader(csvfile): # _下划线代表一列，这里的website是第二列
				urls.append('http://'+website)
				if len(urls) == self.max_urls:
					break
			csvfile.close()
			# print (urls)
			return urls