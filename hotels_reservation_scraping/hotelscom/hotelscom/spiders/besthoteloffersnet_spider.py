from datetime import datetime
import scrapy
from scrapy_splash import SplashRequest
from urllib import parse
from hotelscom.items import HotelscomItem

class QuotesSpider(scrapy.Spider):
    name = "besthoteloffers.net"
    timestamp =  str(datetime.now()).replace(' ','T')[:19]
     

    def start_requests(self):
        urls =[]
        countries = ['Tunisia','Lebanon','Jordan','Morocco','Algeria','United_Arab_Emirates']
        #countries = ['United_Arab_Emirates']
        for co in countries:
            urls.append('https://offers-en.besthoteloffers.net/Hotels/Search?destination=place:@@c&radius=0km&checkin=2018-08-01&checkout=2018-08-16&Rooms=1&adults_1=2&pageSize=999999&pageIndex=0&sort=Popularity-desc&showSoldOut=false&scroll=1&HotelID=&mapState=expanded%3D0'.replace('@@c',co))
        script = """
        function main(splash, args)
          splash.images_enabled = false
          assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
          assert(splash:go(splash.args.url))
          local version = splash:evaljs("$.fn.jquery")
          assert(splash:wait(10))
          return {
            html = splash:html(),
          }
        end
        """

        for url in urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='execute',args={'lua_source': script})
            #yield scrapy.Request(url=url, callback=self.parse_country)

    def parse(self, response):
        print(len(response.xpath("//div[@id='hc_sr']/div[contains(@class,'hc_sri')]")))
        for hotel in response.xpath("//div[@id='hc_sr']/div[contains(@class,'hc_sri')]"):
            hotl = HotelscomItem()
            hotl['titre'] =hotel.xpath(".//div[@class='hc_m_content']/div/h3/a/text()").extract_first() 
            hotl['price'] = hotel.xpath(".//div[@class='hc_sri_result_promotedDeal']/p[@class='hc_hotel_price ']/text()[3]").extract_first()
            hotl['review']= hotel.xpath(".//p[@class='hc_hotel_userRating']/a/text()").extract_first()
            hotl['city']= hotel.xpath(".//p[@class='hc_hotel_location']/text()").extract_first()
            hotl['country']=response.xpath("//h1[@class='hc-searchproperties']/text()").extract_first()
            hotl['host'] = self.name
            hotl['timestamp'] = self.timestamp
            hotl['idx'] = hotel.xpath(".//@data-hotelid").extract_first() 
            stars= hotel.xpath(".//p[contains(@class,'hc-hotelrating hc')]/@title").extract_first()
            if stars is not None:
                hotl['stars']= stars
            else: hotl['stars']= None
            print(hotl)
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
        bloks = response.xpath("//div[@id='hc_sr']/div[contains(@class,'hc_sri')]")

        if len(bloks)>0:
            for bl in bloks:
                l =  bl.xpath(".//a/@href").extract_first()
                print(l)
                city_name = bl.xpath(".//a/text()").extract_first()
                if (l is not None) and (city_name is  not None):
                    namec = " ".join(city_name.split()[:-1])
                    meta = response.meta.copy()
                    meta['city']=namec
                    yield SplashRequest(url="https://directrooms.com"+l+"?currency=EUR", callback=self.parse_citieslink, endpoint='render.html',meta=meta)



    def parse_citieslink(self, response):
        link = response.xpath("//div[@class='content_all']/div[contains(@class,'content_row')]/a/@href").extract_first()
        if link is not None:
            city_id = link.split('/')[-2]
            url = "https://en.directrooms.com/sr/dl/%s/20180801-20180815-1-2/?currency=EUR" % city_id
            print(url)
            yield SplashRequest(args={'wait': 5},url=url, callback=self.parse, endpoint='render.html',meta=response.meta.copy())


