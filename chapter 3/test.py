import re
url = 'http://example.webscraping.com/places/default/view/Antarctica-9'
a = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', url)
c = a+'/'
print(a)
print(c)



filename = '/'.join(segment[:255] for segment in a.split('/'))
print('12312')
print(filename)

print(c.split('/'))
print('/'.join(segment[:3] for segment in c.split('/')))