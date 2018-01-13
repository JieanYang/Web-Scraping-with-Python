def normalize(seed_url, link):
	"""Normalize this URL by removing hash and adding domain
	"""
	link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
	return urlparse.urljoin(seed_url, link)


# 之后测试