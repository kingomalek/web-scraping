from datetime import datetime
import scrapy
from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = "hotels.com"
    timestamp =  str(datetime.now()).replace(' ','T')[:19]

    def start_requests(self):

        urls =[
        'https://uk.hotels.com/change_currency.html?currency=EUR'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_tocountry)


    def parse(self, response):
        print(len(response.xpath("//div[@id='listings']/ol/li[@data-hotel-id]")))
        for hotel in response.xpath("//div[@id='listings']/ol/li[@data-hotel-id]"):
            try:
                hotl = HotelscomItem()
                hotl['titre']: hotel.xpath(".//h3[@class='p-name']/a/text()").extract_first() 
                hotl['price']: hotel.xpath(".//div[@class='price']/a/b/text() | .//div[@class='price']/a/span/ins/text()").extract_first()
                hotl['review']: hotel.xpath(".//span[@class='guest-rating-value']/strong/text()").extract_first()
                hotl['idx']: hotel.xpath(".//@data-hotel-id").extract_first()
                hotl['host']: self.name
                hotl['timestamp'] : self.timestamp
                place= hotel.xpath("//div[@class='summary']/h1/text()").extract_first()
                if place is not None:
                    hotl['city'] = place.split(',')[0]
                    hotl['country'] = place.split(',')[-1]
                else:
                    hotl['city'] = None
                    hotl['country'] = None

                stars= hotel.xpath(".//div[@class='star-rating-text star-rating-text-strong']/text()").extract_first()
                if stars is not None:
                    hotl['stars']= stars.split('-')[0]
                else: hotl['stars']= None
                print(hotl)
                yield hotl
            except Exception as e:
                continue
        '''
        next_page = response.xpath("//div[@class='pagination']/a/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin("https://uk.hotels.com/search.do"+next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        '''


    def parse_cities(self, response):
        script = """
        function main(splash, args)
        splash.images_enabled = false
        local steps = 0
        local scroll_delay = 2
        local prev = 0
        local html = " "
        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        local expanded = splash:select('.expanded-area-message')
        assert(splash:go(splash.args.url))
        assert(splash:wait(3))
        while((get_body_height() ~= prev) and (expanded == nil) and (steps < 400))
        do
            html = splash:html()
            prev = get_body_height()
            scroll_to(0, get_body_height())
            splash:wait(scroll_delay)
            steps = steps + 1
            expanded = splash:select('.expanded-area-message')
        end
           
        return html
        end
        """
        links = response.xpath('//a[@title and not(@rel)]/@href')
        for l in links:
            if l is not None:
                idcitie = str(l.extract()).split('/')[3][2:]
                url = 'https://uk.hotels.com/search/search.html?destination-id='+idcitie+'&q-check-out=2018-08-15&sort-order=STAR_RATING_HIGHEST_FIRST&q-room-0-adults=2&q-rooms=1&q-check-in=2018-08-01&f-accid=1&q-room-0-children=0'
                print(url)
                #yield scrapy.Request(url=url, callback=self.parse)
                yield SplashRequest(url=url, callback=self.parse, endpoint='execute',args={'lua_source': script})
        

    def parse_country(self, response):
        countries = ['Tunisia','Lebanon','Jordan','Morocco','Algeria','Emirates']
        #countries = ['Tunisia']
        az = ['a-c','d-f','g-i','j-l','m-o','p-r','s-u','y-z']
        for co in countries:
            id = response.xpath("//a/bdi[contains(text(),'"+co+"')]/../@href").extract_first().split('/')[3]
            for aux in az:
                link ="https://uk.hotels.com/"+id+"-"+aux.replace('-','')+"/hotels-in-"+co.lower()+"-"+aux+"/"
                yield scrapy.Request(link, callback=self.parse_cities)

    def parse_tocountry(self, response):
                yield scrapy.Request('https://uk.hotels.com/allcountries/', callback=self.parse_country)


