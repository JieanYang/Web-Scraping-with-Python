import urllib.request as urllib2
import urllib.parse as urlparse

"""
#使用urllib2支持代理的代码
proxy = 'http://10.10.1.10:3128'
opener = urllib2.build_opener()
proxy_params = {urlparse.urlparse(url).scheme: proxy}
opener.add_handler(urllib2.ProxyHandler(proxy_params))
response = opener.open(request)
"""

def download(url, user_agent='wswp', proxy=None, num_retries=2):
	print('Downloading:',url)
	headers = {'user-agent':user_agent}
	request = urllib2.Request(url, headers=headers)
	
	opener = urllib2.build_opener()
	if proxy:
		proxy_params = {urlparse.urlparse(url).scheme: proxy}
		opener.add_handler(urllib2.ProxyHandler(proxy_params))
	try:
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