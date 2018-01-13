# -*- coding: utf-8 -*-
import urllib.request as urllib2
from Throttle import Throttle


class Downloader:
	def __init__(self, delay=5, user_agent='wswp', proxies=None, num_retries=1, cache=None):
		self.throttle = Throttle(delay) # 时间推迟
		self.user_agent = user_agent # 爬虫用户
		self.proxies = proxies # 代理设置
		self.num_retries = num_retries # 重试次数
		self.cache = cache # 缓存
		
	def __call__(self, url):
		result = None
		if self.cache: # 下载url页面前先检查是否有缓存
			try:
				result = self.cache[url]
			except AttributeError as e: # KeyError 表示错误类型: cashe映射中没有url这个键
				# url is not available in cache
				pass
			else:
				if self.num_retries > 0 and 500 <= result['code'] <600: # 下载下来的缓存不完整或有错误的，重置result
					# server error so ignore result from cache
					# and re-download
					result = None
		
		if result is None:
			# result was not loaded from cache
			# so still need to download
			self.throttle.wait(url)
			if self.proxies:
				proxy = random.choice(self.proxies)
			else:
				proxy = None
			headers = {'User-agent': self.user_agent}
			result = download(url, headers, proxy, self.num_retries)
			if self.cache: #如果缓存，则保存到cache字典里
				# 将数据存入Mongdb缓存， {'html': html, 'code': code }
				self.cache[url] = result
		return result['html'] # 返回html结果
		
def download(url, headers, proxy, num_retries, data=None):
	print ('Downloading:', url)
	request = urllib2.Request(url, data, headers)
	opener = urllib2.build_opener()
	if proxy:
		proxy_params = {urlparse.urlparse(url).scheme: proxy}
		opener.add_handler(urllib2.ProxyHandler(proxy_params))
	try:
		response = opener.open(request)
		# 因为zip是二进制，所以去掉了decode语句
		html = response.read() # .decode('utf-8')
		html = html.decode('utf-8')
		code = response.code
	except urllib2.URLError as e:
		print ('Download error:', e.reason)
		html = ''
		if hasattr(e, 'code'):
			code = e.code
			if num_retries > 0 and 500 <= code < 600:
				# retry 5XX HTTP errors
				return download(url, headers, proxy, num_retries-1, data)
		else:
			code = None
	return {'html': html, 'code': code}