import lxml.html
from cssselect import GenericTranslator, SelectorError
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
	
'''
print(' ')
broken_html="<ul class=country><li>Area<li>Population</ul>"
#parse the HTML
tree = lxml.html.fromstring(broken_html)
fixed_html = lxml.html.tostring(tree, pretty_print=True)
print(tree)
print(type(tree))
print(fixed_html)
print(type(fixed_html))
'''

url = 'http://example.webscraping.com/places/default/view/239'
html = download(url)
tree = lxml.html.fromstring(html)
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
area = td.text_content()
print(area)