# -*- coding: utf-8 -*-
import csv
import codecs
from zipfile import ZipFile
import io
from Downloader import Downloader

def alexa():
    urls = [] # top 1 million URL's will be stored in this list
    D = Downloader()
    zipped_data = D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
    # 网上下下来的zip是二进制格式的，不能转换成字符格式
    # 只可以打开的时候，同时进行utf-8的编码才行
    # 这里我们用了codecs来打开，编码为utf_8_sig
    with ZipFile(io.BytesIO(zipped_data)) as zf: # io.StringIO()不接受byte数据，所以无法使用作者原版本
        csv_filename = zf.namelist()[0]
        # data = zf.read(csv_filename).decode('utf-8') #返回格式str, str格式在后面的for循环无法应用
        data = codecs.open(csv_filename, 'r+', 'utf_8_sig') # 返回格式 codecs.StramReaderWriter
        # print(data)
        for _, website in csv.reader(data): # _下划线代表一列，这里的website是第二列
            urls.append('http://' + website)
        # ====================================================================
        # 作者原本版本，zip.open 不能用编码解码
        # for _, website in csv.reader(zf.open(csv_filename, mode='r')): # _下划线代表一列，这里的website是第二列
        #     urls.append('http://' + website)
        # =====================================================================
    return urls


if __name__ == '__main__':
    print(len(alexa()))