import scrapy
import re
from skindl.items import SkinItem

class MinecraftskinsSpider(scrapy.Spider):
    name = 'minecraftskins'
    allowed_domains = ['www.minecraftskins.net']
    start_urls = ['http://www.minecraftskins.net/']

    def parse(self, response):
        for content in response.xpath('//div[@class="row grid"]'):
            
            skinItem = SkinItem()

            for skin in content.xpath('//div[@class="card"]'):
                skinItem['title'] = skin.xpath('//h2[@class="card-title"]/text()').getall()
                skinItem['description'] = skin.xpath('//p[@class="card-description"]/text()').getall()
                skinItem['designer'] = skin.xpath('//h3[@class="card-designer"]/text()').getall()
                skinItem['preview_url'] = skin.xpath('//div[@class="card-image"]//img/@src').getall()
                skinItem['preview_url'] = [response.urljoin(re.sub("front_preview","preview",u)) for u in skinItem['preview_url']]
                skinItem['skin_url'] = skin.xpath('//div[@class="card-controls clearfix"]//a[2]/@href').getall()
                skinItem['skin_url'] = [response.urljoin(u) for u in skinItem['skin_url']]

            yield skinItem

        ### Get Next page if available ###
        # next_page = response.xpath('//a[@class="next-page"]/@href').get()
        # if next_page is not None:
        #   next_page = response.urljoin(next_page)
        #   yield scrapy.Request(next_page, callback=self.parse)
        
        ##### alternate
        for href in response.xpath('//a[@class="next-page"]/@href'):
            yield response.follow(href, callback=self.parse)