from bs4 import BeautifulSoup
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
	

print(' ')
broken_html="<ul class=country><li>Area<li>Population</ul>"
#parse the HTML
soup = BeautifulSoup(broken_html, 'html.parser')
# 解析器 https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
fixed_html = soup.prettify()
print(fixed_html)	
print(' ')
ul = soup.find('ul', attrs={'class': 'country'})
print(ul)
print(' ')
result1 = ul.find('li') # return just the first match
print(result1)
print(' ')
result2 = ul.find_all('li') # return all matches
print(result2)

print(' ')
url = 'http://example.webscraping.com/places/default/view/239'
html = download(url)
soup = BeautifulSoup(html, 'html.parser')
#lkocate the area row
tr = soup.find(attrs={'id': 'places_area__row'})
td = tr.find(attrs={'class': 'w2p_fw'}) # locate the area tag
area = td.text # extract the text from this tag

print(area)