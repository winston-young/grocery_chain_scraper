# -*- coding: utf-8 -*-
from retail_locations.items import RetailLocationsItem
import scrapy


class SuperOneFoodsSpider(scrapy.Spider):
    name = 'superone'
    allowed_domains = ['superonefoods.com']
    retailer_name = 'Super One Foods'
    country = 'United States'
    host = 'www.superonefoods.com'

    def start_requests(self):
        yield scrapy.Request(
            'https://www.superonefoods.com/store-finder'
        )

    def parse(self, response):
        for location in response.css('.table-bordered tbody tr'):

            item = RetailLocationsItem()
            loader = item.loader(selector=location)

            full_address = [val.get() for val in location.css('div ::text')]
            zip_code = full_address[1].split()[-1]
            store_phone = location.css('a[href^="tel"]::text').get()

            loader.add_css('store_name', '.store-name::text')

            loader.add_value(None, {
                'store_url': response.urljoin(location.css('.store-name::attr(href)').get()),
                'street_address': full_address[0],
                'city': full_address[1].split(',')[0],
                'state': full_address[1].split(',')[1].split()[0],
                'zip_code': zip_code,
                'store_phone': store_phone,
                'store_id': store_phone
            })

            yield loader.load_item()
