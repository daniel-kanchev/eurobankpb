import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from eurobankpb.items import Article


class EuroSpider(scrapy.Spider):
    name = 'euro'
    start_urls = ['https://www.eurobankpb.lu/en/Media/NewsAndEvents']

    def parse(self, response):
        links = response.xpath('//article/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1[@class="article__title"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="article__date"]/text()').get()
        if date:
            date = datetime.strptime(date.strip(), '%d %B %Y')
            date = date.strftime('%Y/%m/%d')

        content = response.xpath('//div[@class="article__body"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
