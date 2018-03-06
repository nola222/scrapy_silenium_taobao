# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse

class TaobaoSpiderMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the spider middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_spider_input(self, response, spider):
		# Called for each response that goes through the spider
		# middleware and into the spider.

		# Should return None or raise an exception.
		return None

	def process_spider_output(self, response, result, spider):
		# Called with the results returned from the Spider, after
		# it has processed the response.

		# Must return an iterable of Request, dict or Item objects.
		for i in result:
			yield i

	def process_spider_exception(self, response, exception, spider):
		# Called when a spider or process_spider_input() method
		# (from other spider middleware) raises an exception.

		# Should return either None or an iterable of Response, dict
		# or Item objects.
		pass

	def process_start_requests(self, start_requests, spider):
		# Called with the start requests of the spider, and works
		# similarly to the process_spider_output() method, except
		# that it doesn’t have a response associated.

		# Must return only requests (not items).
		for r in start_requests:
			yield r

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)


class TaobaoDownloaderMiddleware(object):
	# Not all methods need to be defined. If a method is not defined,
	# scrapy acts as if the downloader middleware does not modify the
	# passed objects.

	@classmethod
	def from_crawler(cls, crawler):
		# This method is used by Scrapy to create your spiders.
		s = cls()
		crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
		return s

	def process_request(self, request, spider):
		# Called for each request that goes through the downloader
		# middleware.

		# Must either:
		# - return None: continue processing this request
		# - or return a Response object
		# - or return a Request object
		# - or raise IgnoreRequest: process_exception() methods of
		#   installed downloader middleware will be called
		return None

	def process_response(self, request, response, spider):
		# Called with the response returned from the downloader.

		# Must either;
		# - return a Response object
		# - return a Request object
		# - or raise IgnoreRequest
		return response

	def process_exception(self, request, exception, spider):
		# Called when a download handler or a process_request()
		# (from other downloader middleware) raises an exception.

		# Must either:
		# - return None: continue processing this exception
		# - return a Response object: stops process_exception() chain
		# - return a Request object: stops process_exception() chain
		pass

	def spider_opened(self, spider):
		spider.logger.info('Spider opened: %s' % spider.name)

# 实现淘宝搜索框输入关键字搜索得到返回的页面信息 -- scrapy + selenium
# 自定义中间件 -- js
class JsMiddleware(object):
	# 初始化  发现每次请求都会打开一个浏览器？？
	def __init__(self):
		# 设置不加载图片
		chrome_options = webdriver.ChromeOptions() # 设置options
		prefs = {"profile.managed_default_content_settings.images":2} # 不加图片
		chrome_options.add_experimental_option('prefs',prefs)
		self.driver = webdriver.Chrome(chrome_options=chrome_options)

	# request -- 处理的request  spider -- 该request对应的spider
	def process_request(self,request,spider):
		# 请求的url  --- 这里重写了download middleware 需要在配置中改一下
		url = request.url
		print(url)
		self.driver.get(url)
		# 获得输入框
		search_input = WebDriverWait(self.driver,10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
		)
		# 输入要查询的东西
		search_input.send_keys(input('请输入您想查询的内容>>>:'))
		# 查找搜索按钮
		search_btn = self.driver.find_element_by_css_selector('#J_TSearchForm > div.search-button > button')
		# 点击搜索按钮
		search_btn.click()
		return HtmlResponse(url=self.driver.current_url,body=self.driver.page_source,encoding='utf-8',request=request)


