import urllib.request as urllib2
import itertools

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

#maximum number of consecutive download errors allowed
max_errors = 5
#current number of consecutive download errors
num_errors = 0
for page in itertools.count(1):
	url = 'http://example.webscraping.com/places/default/view/-%d' % page
	html = download(url)
	if html is None:
		#received an error trying to download this webpage
		num_errors += 1
		if num_errors == max_errors:
			#reached maximum number of consecutive errors so exit
			break
	else:
		#success - can scrape the result
		#...
		num_errors = 0
		
