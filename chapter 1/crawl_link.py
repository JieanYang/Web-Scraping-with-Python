import urllib.request as urllib2
import re
import urllib.parse as urlparse

def download(url, user_agent='wswp', num_retries=2):
	print ('Downloading:',url)
	headers = {'User-agent': user_agent}
	request = urllib2.Request(url, headers=headers)
	try:
		html = urllib2.urlopen(request).read().decode('utf-8')
	except urllib2.URLError as e:
		print ('Download error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				#recursively retry 5xx HTTP errors
				return download(url, num_retries-1)
	return html

def link_crawler(seed_url, link_regex):
	"""Crawl from the given seed URL following links matched by link_regex
	"""	
	crawl_queue = [seed_url]
	#keep track which URL's have seen before
	seen = set(crawl_queue)
	while crawl_queue:
		url = crawl_queue.pop()
		html = download(url)
		#filter for links matching our regular expression
		for link in get_links(html):
		#check if link matches expected regex
			if re.search(link_regex, link):
				#from absolute link
				link = urlparse.urljoin(seed_url, link)
				#check if have already seen this link
				if link not in seen:
					seen.add(link)
					crawl_queue.append(link)

def get_links(html):
	"""Return a list of links from html
	"""
	#a regular expression to extract all links from the webpage
	webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
	#list of all links from the webpage
	return webpage_regex.findall(html)
	
link_crawler('http://example.webscraping.com', '/(index|view)')