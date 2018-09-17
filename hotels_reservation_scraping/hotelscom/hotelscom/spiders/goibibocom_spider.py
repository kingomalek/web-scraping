from datetime import datetime
import scrapy
from scrapy_splash import SplashRequest
from urllib import parse

class QuotesSpider(scrapy.Spider):
    name = "goibibo.com"
    timestamp =  str(datetime.now())


    def start_requests(self):

        urls =[
        'https://en.directrooms.com/sr/helper/20180801-20180815-1-2/?search=tunisia'
        ]

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse_cities, endpoint='render.html',meta={'country':'Tunisia'})
            #yield scrapy.Request(url=url, callback=self.parse_country)

    def parse(self, response):
        #print(response.xpath("//div[@id='holding_sec']/div[@class='nrs-body']//span[@class='nrs-name']/text()").extract_first())
        print(len(response.xpath("//div[@id='holding_sec']/div[@class='nrs-body']")))
        for hotel in response.xpath("//div[@id='holding_sec']/div[@class='nrs-body']"):
            hotl =  {
                'titre': hotel.xpath(".//span[@class='nrs-name']/text()").extract_first() ,
                'price' : hotel.xpath(".//span[@class='nrs-best-price-num']/text()").extract_first(),
                'review': hotel.xpath(".//span[@class='nrs-average-rat']/text()").extract_first(),
                'city':response.meta['city'],
                'country':response.meta['country'],
                'host' : self.name,
                'timestamp' : self.timestamp,
            }
            idx = hotel.xpath(".//@id").extract_first()
            if id is not None:
                hotl['id']=idx.split('_')[-1]
            else:
                hotl['id'] = None
            yield hotl
        
        '''
            place= hotel.xpath("//div[@class='summary']/h1/text()").extract_first().split(',')
            if place is not None:
                hotl['city'] = place[0].strip()
                hotl['country'] = place[1].strip()

            stars= hotel.xpath(".//div[@class='star-rating-text star-rating-text-strong']/text()").extract_first()
            if stars is not None:
                hotl['stars']= stars.split('-')[0]
            yield hotl
        next_page = response.xpath("//div[@class='pagination']/a/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin("https://uk.hotels.com/search.do"+next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        '''

    def parse_cities(self, response):
        blocks = response.xpath("//div[@class='helppage-whole']/span[not(contains(@onclick,'hotel_id'))]")
        for bl in blocks:
            link = bl.xpath('.//@onclick').extract_first()
            city = bl.xpath(".//span/span[@class='sg-sucgess']/text()").extract_first()
            if (link is not None) and (city is not None):
                url = link.split("'")[1]+"?currency=EUR"
                yield SplashRequest(url=url, callback=self.parse, endpoint='render.html',meta={'country':response.meta['country'],'city':city})
        '''
        for l in links:
            if l is not None:
                idcitie = str(l.extract_first()).split('=')[-1]
                url = 'https://uk.hotels.com/search/search.html?destination-id='+idcitie+'&q-check-out=2018-08-15&sort-order=STAR_RATING_HIGHEST_FIRST&q-room-0-adults=2&q-rooms=1&q-check-in=2018-08-01&f-accid=1&q-room-0-children=0'
                print(url)
                yield scrapy.Request(url=url, callback=self.parse)
        '''
        

    def parse_citieslink(self, response):
        links = response.xpath("//div[@id='all-states-container']/section/div/dl/a/@href").extract()
        if len(links)>0:
            for url in links:
                yield scrapy.Request(url="https://www.agoda.com"+url, callback=self.parse_cities)


    def parse_country(self, response):
        #countries = ['Tunisia','Lebanon','Jordan','Morocco']
        countries = ['Jordan']
        for co in countries:
            city_url = response.xpath("//ul[@class='hubs-links']/li[@data-selenium='country-item']/a[contains(text(),'"+co+"')]/@href").extract_first()
            print(city_url)
            if city_url is not None:
                yield scrapy.Request('https://www.agoda.com'+city_url, callback=self.parse_citieslink)




