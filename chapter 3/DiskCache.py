import os
import re
from urllib import parse as urlparse
import pickle

class DiskCache:
	def __init__(self, cache_dir='cache'):
		self.cache_dir = cache_dir
		# self.max_length = max_length
		
	def url_to_path(self, url):
		"""
		Create file system path for this URL
		"""
		#分析url为好几块，分别是 scheme, netloc, path, query, fragment
		components = urlparse.urlsplit(url)
		#append index.html to empty paths
		#对url进行处理生成适合的文件路径
		path = components.path
		if not path:
			path = '/index.html'
		elif path.endswith('/'):
			path += 'index.html'
		filename = components.netloc + path + components.query
		#replace invalid characters
		#文件系统对名字有规定
		filename = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)
		#retrict maximum number of characters
		filename = '/'.join(segment[:255] for segment in filename.split('/'))
		return os.path.join(self.cache_dir, filename) # 返回url对应的文件路径
		
	def __getitem__(self, url):
		"""
		Load data from disk for this URL
		"""
		path = self.url_to_path(url)
		if os.path.exists(path):
			with open(path, 'rb') as fp:
				# 反序列化，恢复文件原始数据类型
				return pickle.load(fp)
				# 解压缩
				## return pickle.loads(zlib.decompress(fp.read()))
		else:
			#URL has not yet been cached
			raise AttributeError(url + ' does not exist')
			
	def __setitem__(self, url, result):
		"""Save data to disk for this url
		"""
		path = self.url_to_path(url)
		folder = os.path.dirname(path)
		if not os.path.exists(folder):
			os.makedirs(folder)
		with open(path, 'wb') as fp:
			#pickle 会将输入转换成序列化字符串然后保存在磁盘中
			fp.write(pickle.dumps(result))
			# 使用压缩 节省磁盘空间
			## fp.write(zlib.compress(pickle.dumps(result)))