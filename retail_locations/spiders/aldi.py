# -*- coding: utf-8 -*-
import json
import scrapy
from retail_locations.items import RetailLocationsItem
from retail_locations.resources.location_data import zipcode_grid


class AldiSpider(scrapy.Spider):
    name = 'aldi'
    allowed_domains = ['aldi.us']
    retailer_name = 'Aldi'
    country = 'United States'
    host = 'www.aldi.us'

    def start_requests(self):
        for zip_code in zipcode_grid(200):
            yield scrapy.Request(
                f'https://www.aldi.us/stores/en-us/Search?SingleSlotGeo={zip_code["zipcode"]}'
            )

    def parse(self, response):
        if response.css('#no-results:contains("No city could be found")'):
            return

        for location in response.css('#resultList li'):
            item = RetailLocationsItem()
            loader = item.loader(selector=location)
            store_data = json.loads(location.css('::attr(data-json)').get())
            city_state_zip = location.css('[itemprop="addressLocality"]::text').get()

            loader.add_css('street_address', '[itemprop="streetAddress"]::text')
            phone_number = location.css('[itemprop="telephone"]::text').get().strip()

            loader.add_value(None, {
                'city': city_state_zip.split(',')[0],
                'state': city_state_zip.split(',')[1].split()[0],
                'country': 'United States',
                'zip_code': city_state_zip.split()[-1],
                'latitude': store_data['locX'],
                'longitude': store_data['locY'],
                'store_phone': phone_number,
                'store_id': phone_number
            })

            yield loader.load_item()
