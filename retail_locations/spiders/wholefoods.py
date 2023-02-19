# -*- coding: utf-8 -*-
import json
from retail_locations.items import RetailLocationsItem
from scrapy.spiders import SitemapSpider


class WholeFoodsSpider(SitemapSpider):
    name = 'wholefoods'
    allowed_domains = ['wholefoodsmarket.com']
    retailer_name = 'Whole Foods'
    host = 'www.wholefoods.com'
    country = 'United States'
    sitemap_urls = ['https://www.wholefoodsmarket.com/sitemap/sitemap-stores.xml']

    def parse(self, response):
        item = RetailLocationsItem()
        loader = item.loader(selector=response)

        store_data = json.loads(response.css('script[type="application/ld+json"]::text').get())

        loader.add_css('store_id', 'wfm-store-selector::attr(store-id)')

        loader.add_value(None, {
            'street_address': store_data['address']['streetAddress'],
            'city': store_data['address']['addressLocality'],
            'state': store_data['address']['addressRegion'],
            'zip_code': store_data['address']['postalCode'],
            'store_url': store_data['url'],
            'latitude': store_data['geo']['latitude'],
            'longitude': store_data['geo']['longitude'],
            'store_phone': store_data['telephone']
        })

        yield loader.load_item()
