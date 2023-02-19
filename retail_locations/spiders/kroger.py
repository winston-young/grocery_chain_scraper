# -*- coding: utf-8 -*-
import json
from retail_locations.items import RetailLocationsItem
from scrapy.spiders import SitemapSpider


class KrogerSpider(SitemapSpider):
    name = 'kroger'
    allowed_domains = ['kroger.com']
    retailer_name = 'Kroger'
    country = 'United States'
    host = 'www.krogers.com'
    sitemap_urls = ['https://www.kroger.com/storelocator-sitemap.xml']

    def parse(self, response):
        item = RetailLocationsItem()
        loader = item.loader(selector=response)
        location_data = json.loads(response.css('script[type="application/ld+json"]::text').get())

        address_element = response.css('[data-qa="storeAddress"] .StoreAddress-storeAddressGuts')[0]
        address = [val.get().strip() for val in address_element.css(' ::text') if val.get().strip()]

        loader.add_value(None, {
            'retailer_name': 'Krogers',
            'store_name': location_data['name'],
            'store_url': location_data['url'],
            'street_address': address[0],
            'city': address[1],
            'state': address[3],
            'zip_code': address[4],
            'latitude': location_data['geo']['latitude'],
            'longitude': location_data['geo']['longitude'],
            'store_phone': location_data['telephone']
        })

        yield loader.load_item()
