from datetime import datetime
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "reuters.com"
    timestamp =  str(datetime.now())

    def start_requests(self):

        urls =[
        'https://www.reuters.com/news/archive?view=page&page=1&pageSize=10'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse(self, response):
            artircl =  {
                'title': response.xpath("//h1[@class='headline_2zdFM'][1]/text()").extract_first() ,
                'content': response.xpath("//div[@class='body_1gnLA']/*/text()").extract_first(),


            }
            
            yield artircl
        


    def parse_links(self, response):
        for article in response.xpath("//div[@class='story-content']/a/@href").extract():
            yield scrapy.Request(url="https://www.reuters.com"+article, callback=self.parse)
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin("https://www.reuters.com/news/archive"+next_page)
            yield scrapy.Request(next_page, callback=self.parse_links)



