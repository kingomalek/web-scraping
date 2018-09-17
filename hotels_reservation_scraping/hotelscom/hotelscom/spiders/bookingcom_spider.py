from datetime import datetime
import scrapy
from hotelscom.items import HotelscomItem


class QuotesSpider(scrapy.Spider):
    name = "booking.com"
    timestamp =  str(datetime.now()).replace(' ','T')[:19]

    def start_requests(self):
        url = 'https://www.booking.com/searchresults.en-gb.html?&ss=@@country&checkin_year=2018&checkin_month=8&checkin_monthday=1&checkout_year=2018&checkout_month=8&checkout_monthday=15&group_adults=2&group_children=0&no_rooms=1&from_sf=1&ss_raw=Tunisia&ac_position=0&ac_langcode=en&dest_type=country&place_id_lat=35&place_id_lon=9.5375&search_pageview_id=db8042e24d370142&search_selected=true&search_pageview_id=db8042e24d370142&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0&selected_currency=EUR'
        #countries = ['214','73','215','143']
        countries = ['Tunisia','Lebanon','Jordan','Morocco','Algeria','United+Arab+Emirates']
        #countries = ['Tunisia']
        for co in countries:
            link = url[:].replace('@@country',co)
            print(link)
            yield scrapy.Request(url=link, callback=self.parse)
            #yield SplashRequest(url=link, callback=self.parse, endpoint='render.html')

    def parse(self, response):
        print(len(response.xpath("//div[@data-hotelid]")))
        for hotel in response.xpath("//div[@data-hotelid]"):
         try:
            item = HotelscomItem()

            item['titre']= hotel.xpath(".//span[contains(@class,'sr-hotel__name')]/text()").extract_first()
            item['price'] = hotel.xpath(".//strong[contains(@class,'price')]/b/text()").extract_first()
            item['review']= hotel.xpath(".//span[contains(@class,'r_main_score_badge')]/span[@class='review-score-badge']/text()").extract_first()
            item['idx']= hotel.xpath(".//@data-hotelid").extract_first()
            item['host'] = self.name
            item['timestamp'] = self.timestamp
            place = hotel.xpath(".//a[contains(@class,'bicon-map-pin')]/following-sibling::a[1]/text()").extract_first()
            if place is not None:
                item['city'] = place.split('–')[0]
            else : item['city'] = None
            item['country'] = response.xpath("//input[@name ='ss']/@placeholder").extract_first()
            stars = hotel.xpath(".//i[contains(@class,'star_track')]/span/text()").extract_first()
            if stars is not None:
            	item['stars']= stars[0]
            else : item['stars'] = None
            #print(item)
            yield item
         except Exception as e:
        		continue
           
        next_page = response.xpath("//a[@data-page-next]/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin("https://www.booking.com/"+next_page+'&selected_currency=EUR')
            yield scrapy.Request(next_page, callback=self.parse)


