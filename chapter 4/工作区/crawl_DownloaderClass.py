import re
import urllib.parse as urlparse
import time
from datetime import datetime
import urllib.robotparser as robotparser
import queue as Queue
# import lxml.html
# from cssselect import GenericTranslator, SelectorError
# import csv


from MongoCache import MongoCache
from Downloader import Downloader
from AlexaCallback import AlexaCallback


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, user_agent='wswp', proxies=None, num_retries=1, scrape_callback=None, cache=None):
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
	D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

	while crawl_queue:
		url = crawl_queue.pop()
		depth = seen[url]
		# check url passes robots.txt restrictions
		if True: #rp.can_fetch(user_agent, url): # robot.txt 不允许会block在这
			html = D(url) # D里面已经有延迟，爬虫身份，代理，重试次数和缓存功能, 返回html 文件
			
			links = []
			
			if scrape_callback: # 将提取的html内容放入回调
				links.extend(scrape_callback(url, html) or []) # ?????????????

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
						# if same_domain(seed_url, link):  # 这里的domain都是不同的
							# success! add this new link to queue
						crawl_queue.append(link)
			# check whether have reached downloaded maximum
			num_urls += 1
			if num_urls == max_urls:
				break
		else:
			print ('Blocked by robots.txt:', url)


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

	scrape_callback = AlexaCallback()
	print(scrape_callback.seed_url)
	link_crawler(seed_url=scrape_callback.seed_url, scrape_callback=scrape_callback, cache=MongoCache())
	
	end = time.clock()
	print ('时间:',end-start)


