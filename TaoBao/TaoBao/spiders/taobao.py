# -*- coding: utf-8 -*-
import scrapy


class TaobaoSpider(scrapy.Spider):
	name = 'taobao'
	allowed_domains = ['taobao.com']
	# start_urls = ['https://s.taobao.com/search?q=zhuawawa&s=44']
	start_urls = ['https://www.taobao.com']

	def parse(self, response):
		with open('zhuawawa_info.html','w+',encoding='utf-8') as f:
			f.write(response.body.decode('utf-8'))
		# print(response.body.decode('utf-8'))
