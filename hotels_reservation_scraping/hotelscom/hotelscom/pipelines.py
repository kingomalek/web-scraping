# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import unidecode

from elasticsearch import Elasticsearch

from scrapy.exceptions import DropItem


class HotelscomPipeline(object):
	def get_digit(self,x):
		if isinstance(x, str):
		    if x is not None:
		        s =''
		        for i in x:
		            if i.isdigit():
		                s+=i
		    return float(s)
		return x

	def clean_removeUnicodes(self,x):
	    if isinstance(x, str):
	        return unidecode.unidecode(x)
	    return x		

	def process_item(self, item, spider):
		try:
			es = Elasticsearch('localhost',port=9200)
			print("Connected", es.info())
			return self.process_item_booking(item,es)
		except Exception as ex:
			print("Error:", ex)



	def process_item_booking(self, item,es):
			keys = ['titre', 'price','stars','idx','country','city']
			for k in keys:
				if item[k] is None:
					raise DropItem("Dropping Item %s" % item)
			item['price'] = self.get_digit(item['price'])/10.
			item['stars'] = int(self.get_digit(item['stars']))
			item['review'] = self.get_digit(item['review'])
			item['titre'] = self.clean_removeUnicodes(item['titre'].lower().strip())
			item['city'] = self.clean_removeUnicodes(item['city'].lower().strip())
			item['country'] = self.clean_removeUnicodes(item['country'].lower().strip())
			el_id =item['idx']+item['host']+item['timestamp']
			item['idx'] = int(item['idx'])

			if item['country'] in ['united arab emirates', 'algeria', 'morocco', 'jordan', 'tunisia', 'lebanon']:
				print(item)
				es.index(index="hotel", doc_type='Hotel',body=dict(item), id=el_id,refresh=True)
