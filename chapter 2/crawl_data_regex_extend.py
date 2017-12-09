import urllib.request as urllib2
import re
from bs4 import BeautifulSoup
import lxml.html
from cssselect import GenericTranslator, SelectorError
import time

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

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent'
, 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format'
, 'postal_code_regex', 'languages', 'neighbours')

def re_scraper(html):
	results1 = {}
	for field in FIELDS:
		results1[field] = re.search('<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field
		, html).groups()[0]
	
	return results1


def bs_scraper(html):
	soup = BeautifulSoup(html, 'html.parser')
	results2 = {}
	for field in FIELDS:
		results2[field] = soup.find('table').find('tr', id='places_%s__row' % field).find('td', class_='w2p_fw').text
		
	return results2
	

def lxml_scraper(html):
	tree = lxml.html.fromstring(html)
	results3 = {}
	for field in FIELDS:
		results3[field] = tree.cssselect('table > tr#places_%s__row > td.w2p_fw'
		% field)[0].text_content()
		
	return results3

NUM_ITERATIONS = 1000 # number of times to test each scraper
html = download('http://example.webscraping.com/places/default/view/239')
for name, scraper in [('Regular expressions', re_scraper), ('BeautifulSoup'
, bs_scraper), ('Lxml', lxml_scraper)]:
	# record start time of scrape
	start = time.time()
	for i in range(NUM_ITERATIONS):
		if scraper ==  re_scraper:
			re.purge() # 对于正则表达式的方法，会生成缓存，re.purge()方法会清除缓存
		result = scraper(html)
		# check scraped result is as expected
		assert(result['area'] == '244,820 square kilometres')
	# record end tiem of scrape and output the total
	end = time.time()
	print('%s: %.2f seconds' % (name, end-start))