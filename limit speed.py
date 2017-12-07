import urllib.request as urllib2
import urllib.parse as urlparse
import datetime
import time

class Throttle:
	"""
	Add a delay between downloads to the same domain
	"""
	def __init__(self, delay):
		#amount of delay between downloads for each domain
		self.delay = delay
		#timestamp of when a domain was last accessed
		self.domains = {'domain': datetime.datetime.now()}
		
	def wait(self, url):
		domain = urlparse.urlparse(url).netloc
		last_accessed = self.domains.get('domain')
		
		if self.delay > 0 and last_accessed is not None:
			sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
			if sleep_secs >0:
				#domain has been accessed recently
				#so need to sleep
				time.sleep(sleep_secs)
		#update the last accessed time
		self.domains[domain] = datetime.datetime.now()
		

def download(url, user_agent='wswp', proxy=None, num_retries=2, delay=2):
	throttle = Throttle(delay)
	print('Downloading:',url)
	headers = {'user-agent':user_agent}
	request = urllib2.Request(url, headers=headers)
	
	opener = urllib2.build_opener()
	if proxy:
		proxy_params = {urlparse.urlparse(url).scheme: proxy}
		opener.add_handler(urllib2.ProxyHandler(proxy_params))
	try:
		throttle.wait(url)
		html = opener.open(request).read().decode('utf-8')
	except urllib2.URLError as e:
		print('Download error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code <600:
				#retry 5xx HTTP errors
				html = download(url, user_agent, proxy, num_retries-1)
	return html

url = 'http://example.webscraping.com/'
print(download(url))	

