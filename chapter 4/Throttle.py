import urllib.parse as urlparse
from datetime import datetime

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
			sleep_secs = self.delay - (datetime.utcnow() - last_accessed).seconds
			if sleep_secs > 0:
				time.sleep(sleep_secs)
		self.domains[domain] = datetime.utcnow()