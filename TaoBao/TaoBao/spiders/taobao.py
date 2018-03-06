# -*- coding: utf-8 -*-
import scrapy
# 使用selenium抓取ajax异步加载的内容
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 导入信号
from scrapy import signals
# 导入分发器 两种方式
from scrapy.xlib.pydispatch import dispatcher
from pydispatch import dispatcher
# 导入urllib的parse转码url
from urllib import parse
# 从scrapy导入Request 处理request
from scrapy.http import Request

class TaobaoSpider(scrapy.Spider):
	name = 'taobao'
	allowed_domains = ['taobao.com']
	# start_urls = ['https://s.taobao.com/search?q=zhuawawa&s=44']
	# start_urls = ['https://www.taobao.com']

	def __init__(self):
		super(TaobaoSpider,self).__init__()
		# 开启chromeoption()
		chrome_options = webdriver.ChromeOptions()  # 设置options
		prefs = {"profile.managed_default_content_settings.images":2} # 不加图片
		chrome_options.add_experimental_option('prefs',prefs)
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		# 显示等待10s
		self.driver.implicitly_wait(10)
		# 使用分发器
		# 通过分发器发信息，建立分发连接
		# dispatcher.connect(receiver信号触发函数，signal=signal触发信号)signals.spider_closed是爬虫结束信息
		dispatcher.connect(receiver=self.my_signal, signal=signals.spider_closed)

	# 定义信号触发函数
	def my_signal(self):
		# 当spider关闭时触发此函数，退出浏览器
		self.driver.quit()

	# 重写Spider类的start_requests()方法
	def start_requests(self):
		self.kw = input('请输入您想搜索的内容>>>:')
		# 拼接url 把传入的参数和url进行拼接
		data = {
			'q':self.kw
		}
		# 'https://s.taobao.com/search?q={}&s=0' 一页44条
		# 注意：url尽量简短，可以不用传的参数省略 urlencode转码的是键值对字典格式
		url = 'https://s.taobao.com/search?{0}&s=0'.format(parse.urlencode(data))
		# 请求url
		self.driver.get(url)
		yield Request(url=url,callback=self.parse)

	def parse(self, response):
		# 写入文件
		with open('zhuawawa_info1.html','w+',encoding='utf-8') as f:
			f.write(response.body.decode('utf-8'))
		# print(response.body.decode('utf-8'))

