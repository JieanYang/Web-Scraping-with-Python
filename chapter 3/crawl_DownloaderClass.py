import re
import urllib.request as urllib2
import urllib.parse as urlparse
import time
from datetime import datetime
import urllib.robotparser as robotparser
import queue as Queue
import lxml.html
from cssselect import GenericTranslator, SelectorError
import csv

from DiskCache import DiskCache


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxies=None, num_retries=1,\
	scrape_callback=None, cache=None):
	"""Crawl from the given seed URL following links matched by link_regex
	"""
	# the queue of URL's that still need to be crawled
	# <class 'collections.deque'> for crawl_queue
	crawl_queue = Queue.deque([seed_url])
	# the URL's that have been seen and at what
	# depth
	seen = {seed_url: 0}
	# track how many URL's have been downloaded
	num_urls = 0
	# check the file robot.txt
	rp = get_robots(seed_url)
	D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, \
	num_retries=num_retries, cache=cache)

	while crawl_queue:
		url = crawl_queue.pop()
		depth = seen[url]
		# check url passes robots.txt restrictions
		if rp.can_fetch(user_agent, url):
			'''throttle.wait(url)'''
			html = D(url) # D里面已经有延迟，爬虫身份，代理，重试次数和缓存功能
			
			links = []
			
			if scrape_callback: # 将提取的内容生成csv文件
				links.extend(scrape_callback(url, html) or []) # ?????????????
				
			depth = seen[url]
			if depth != max_depth:
				# can still crawl further
				if link_regex:
					# filter for links matching our regular expression
					links.extend(link for link in get_links(html) if re.search(link_regex, link))

				for link in links:
					link = normalize(seed_url, link)
					# check whether already crawled this link
					if link not in seen:
						seen[link] = depth + 1
						# check link is within same domain
						if same_domain(seed_url, link):
							# success! add this new link to queue
							crawl_queue.append(link)

			# check whether have reached downloaded maximum
			num_urls += 1
			if num_urls == max_urls:
				break
		else:
			print ('Blocked by robots.txt:', url)
			

			
class ScrapeCallback:
	def __init__(self):
		self.writer = csv.writer(open('countries.csv', 'w'))
		self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent'
		, 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format'
		, 'postal_code_regex', 'languages', 'neighbours')
		self.writer.writerow(self.fields)

	def __call__(self, url, html):
		if re.search('/view/', url) and re.search('^((?!user).)*$', url):
			tree = lxml.html.fromstring(html)
			row = []
			for field in self.fields:
				row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
			self.writer.writerow(row)
			
class Throttle:
	"""Throttle downloading by sleeping between requests to same domain
	"""
	def __init__(self, delay):
		# amount of delay between downloads for each domain
		# 延迟时间
		self.delay = delay
		# timestamp of when a domain was last accessed
		self.domains = {}
		
	def wait(self, url):
		domain = urlparse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.now()

class Downloader:
	def __init__(self, delay=5, user_agent='wswp', proxies=None, \
	num_retries=1, cache=None):
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
				if self.num_retries > 0 and \
				500 <= result['code'] <600: # 下载下来的缓存不完整或有错误的，重置result
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
			result = download(url, headers, proxy, \
			self.num_retries)
			if self.cache: #如果缓存，则保存到cache字典里
				# save result to cache
				self.cache[url] = result
		return result['html']
		
def download(url, headers, proxy, num_retries, data=None):
	print ('Downloading:', url)
	request = urllib2.Request(url, data, headers)
	opener = urllib2.build_opener()
	if proxy:
		proxy_params = {urlparse.urlparse(url).scheme: proxy}
		opener.add_handler(urllib2.ProxyHandler(proxy_params))
	try:
		response = opener.open(request)
		html = response.read().decode('utf-8')
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


def normalize(seed_url, link):
	"""Normalize this URL by removing hash and adding domain
	"""
	link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
	return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
	"""Return True if both URL's belong to same domain
	"""
	return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
	"""Initialize robots parser for this domain
	"""
	rp = robotparser.RobotFileParser()
	rp.set_url(urlparse.urljoin(url, '/robots.txt'))
	rp.read()
	return rp
		

def get_links(html):
	"""Return a list of links from html 
	"""
	# a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	# list of all links from the webpage
	return webpage_regex.findall(html)


if __name__ == '__main__':
	#print(link_crawler('http://example.webscraping.com', '/(index|view)', delay=1, num_retries=1, user_agent='BadCrawler'))
	#print(link_crawler('http://example.webscraping.com', '/(index|view)', delay=1, num_retries=1, max_depth=1, user_agent='GoodCrawler'))

	start = time.clock()

	link_crawler('http://example.webscraping.com', '/(index|view)', delay=1, max_depth=-1, scrape_callback=ScrapeCallback(), cache=DiskCache())
	
	end = time.clock()
	print ('时间:',end-start)


