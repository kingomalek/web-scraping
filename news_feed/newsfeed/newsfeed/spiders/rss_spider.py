from scrapy.spider import XMLFeedSpider
class MySpider(XMLFeedSpider):
    name = "cnn.com"
    allow_domain = ['example']
    start_urls = ('https://www.yahoo.com/news/rss',
        'http://feeds.bbci.co.uk/news/world/rss.xml',
        'http://feeds.bbci.co.uk/news/uk/rss.xml',
        'http://feeds.bbci.co.uk/news/business/rss.xml',
        'http://feeds.bbci.co.uk/news/politics/rss.xml',
        'http://feeds.bbci.co.uk/news/health/rss.xml',
        'http://feeds.bbci.co.uk/news/education/rss.xml',
        'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
        'http://feeds.bbci.co.uk/news/technology/rss.xml',
        'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
        'http://feeds.foxnews.com/foxnews/latest?format=xml',
        'http://rss.cnn.com/rss/edition.rss',
        'http://rss.cnn.com/rss/edition_world.rss',
        'http://rss.cnn.com/rss/edition_africa.rss',
        'http://rss.cnn.com/rss/edition_americas.rss',
        'http://rss.cnn.com/rss/edition_asia.rss',
        'http://rss.cnn.com/rss/edition_europe.rss',
        'http://rss.cnn.com/rss/edition_meast.rss',
        'http://rss.cnn.com/rss/edition_us.rss',
        'http://rss.cnn.com/rss/money_news_international.rss',
        'http://rss.cnn.com/rss/edition_technology.rss',
        'http://rss.cnn.com/rss/edition_space.rss',
        'http://rss.cnn.com/rss/edition_entertainment.rss',
        'http://rss.cnn.com/rss/edition_sport.rss',
        'http://rss.cnn.com/rss/edition_football.rss',
        'http://rss.cnn.com/rss/edition_golf.rss',
        'http://rss.cnn.com/rss/edition_motorsport.rss',
        'http://rss.cnn.com/rss/edition_tennis.rss',
        'http://rss.cnn.com/rss/edition_travel.rss',
        'http://rss.cnn.com/rss/cnn_latest.rss',
        'https://www.usnews.com/rss/education',
        'https://www.usnews.com/rss/health',
        'https://www.usnews.com/rss/money',
        'https://www.usnews.com/rss/news',
        'https://www.usnews.com/rss/opinion',
        'https://www.usnews.com/rss/travel-editorial',
)
    iterator = 'iternodes'
    itertag = 'item'


    def parse_node(self, response, node):
        #self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))
        print('title= ',' '.join(node.xpath('title/text()').extract()))
        print('description= ',' '.join(node.xpath('description/text()').extract()))
        print('link= ',' '.join(node.xpath('link/text()').extract()))
        print('medias= ',node.xpath("*[name()='media:group']/*[name()='media:content']").extract())
        print('date= ',' '.join(node.xpath('pubDate/text()').extract()))
        print('thumbnail= ',node.xpath("*[name()='media:thumbnail']/@url").extract())
        print('category= ',' '.join(node.xpath('category/text()').extract()))


