import urllib.request as urllib2
import re

def download(url, user_agent='wswp', num_retries=2):
	print ('Downloading:',url)
	headers = {'User-agent': user_agent}
	request = urllib2.Request(url, headers=headers)
	try:
		html = urllib2.urlopen(request).read()
	except urllib2.URLError as e:
		print ('Download error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				#recursively retry 5xx HTTP errors
				return download(url, num_retries-1)
	return html
	
def crawl_sitemap(url):
	#download the sitemap file
	sitemap = download(url)
	print(sitemap)
	#extract the sitemap links
	p = re.compile(r'<loc>(.*?)</loc>')
	links = p.findall(sitemap)
	# cannot use a string pattern on a bytes-like object
	#不能在类似字节的对象上使用字符串模式
	#之后想解决办法
	for link in links:
		print(link)
		#html = download(link)
		#scrap html here
		#...
		#print(html)

crawl_sitemap('https://www.google.com/sitemap.xml')