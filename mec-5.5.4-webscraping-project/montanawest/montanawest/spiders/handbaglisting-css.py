import scrapy
from scrapy.http import Request
import re


class HandbaglistingSpider(scrapy.Spider):
    name = 'handbaglisting-css'
    allowed_domains = ['montanawestusa.com']
    start_urls = ['https://www.montanawestusa.com/collections/handbag-western-wholesale-purse-concealed-gun-purse']

    '''
    response.xpath("//div[@class='product-info']/h3/text()").extract()
    '''


    def parse(self, response):
        handbags = response.css('#product-loop>div>div>a::attr(href)').extract()
        for handbag in handbags:
            url = 'https://www.montanawestusa.com' + handbag
            yield Request(url, callback=self.parse_handbag)

        current_page = re.findall(r"(?<!page)[\d]+", response.request.url)
        next_page = re.findall(r"(?<!page)[\d]+", response.css('#pagination > a::attr(href)').extract()[-1])
     
        if not current_page:
            next_page = response.css('#pagination > a::attr(href)').extract()[-1] 
            next_url = response.urljoin(next_page)
            yield Request(next_url)

        elif int(current_page[0]) < int(next_page[0]):
            next_page = response.css('#pagination > a::attr(href)').extract()[-1] 
            next_url = response.urljoin(next_page)
            yield Request(next_url)

    def parse_handbag(self, response):
        title = response.css('#product-description >h1::text').extract()[0]
        price = response.css('#product-description > div > p > span::text').extract()[0]
        sku = response.css('#product-description > div >  span::text').extract()[0]

        yield {
            'title': title,
            'price': price,
            'sku': sku
        }