import csv
import codecs
import urllib.request as urllib2

# 保存下载的zip文件到本地
url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
path = r"C:\Users\yang\Desktop\Web Scraping with Python\chapter 4\test.zip"
 
# 网上下下来的zip是二进制格式的，不能转换成字符格式
# 只可以打开的时候，同时进行utf-8的编码才行
# req = urllib2.urlopen(url).read().decode('utf_8_sig') 

req = urllib2.urlopen(url)
data = req.read()
print (data)
with open(path, "wb") as zip:
    zip.write(data)
req.close()





csvfile = codecs.open(r'C:\Users\yang\Desktop\Web Scraping with Python\chapter 4\top-1m.csv', 'r+', 'utf_8_sig')
print (type(csvfile))
reader = csv.reader(csvfile)

# for line in reader: #代表第一行的所有列
#     print(line)

for _, website in csv.reader(csvfile): # _下划线代表一列，这里的website是第二列
	print(website)

csvfile.close()
