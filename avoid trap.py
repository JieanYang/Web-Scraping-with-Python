#查看crawl_link.py文件
def link_crawler(. . ., max_depth=2):
	max_depth = 2
	seen={}
	. . .
	depth = seen[url]
	if depth != max_depth:
		for link in links:
			seen[link] = depth + 1
			crawl_queue.append(link)