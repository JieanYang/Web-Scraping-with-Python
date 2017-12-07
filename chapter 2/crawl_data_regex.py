import re
import urllib.request as urllib2

def download(url, num_retries=2):
	print ('Downloading:',url)
	try:
		html = urllib2.urlopen(url).read().decode('utf-8')
	except urllib2.URLError as e:
		print ('Download error:', e.reason)
		html = None
		if num_retries > 0:
			if hasattr(e, 'code') and 500 <= e.code < 600:
				#recursively retry 5xx HTTP errors
				return download(url, num_retries-1)
	return html
	

url = 'http://example.webscraping.com/places/default/view/239'
html = download(url)

result1 = re.findall('<td class="w2p_fw">(.*?)</td>', html)
print(' ')
print(result1)
print(result1[1])
print(' ')
result2 = re.findall('<tr id="places_area__row"><td class="w2p_fl"><label class="readonly" for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html)
print(result2)
print(' ')
result3 = re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html)
# \s 表示空白符 ["\'] 表示双引号或者单引号
print(result3)