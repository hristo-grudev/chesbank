import scrapy

from scrapy.loader import ItemLoader

from ..items import ChesbankItem
from itemloaders.processors import TakeFirst


class ChesbankSpider(scrapy.Spider):
	name = 'chesbank'
	start_urls = ['https://chesbank.com/about-us/in-the-news/']

	def parse(self, response):
		post_links = response.xpath('/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('/text()').get()

		item = ItemLoader(item=ChesbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
