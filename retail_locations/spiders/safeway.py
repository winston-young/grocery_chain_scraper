# -*- coding: utf-8 -*-
from retail_locations.items import RetailLocationsItem
import scrapy


class Safeway(scrapy.Spider):
    name = 'safeway'
    allowed_domains = ['safeway.com']
    retailer_name = 'Safeway'
    country = 'United States'
    host = 'www.safeway.com'

    def start_requests(self):
        yield scrapy.Request(
            'https://local.safeway.com/safeway.html',
            callback=self.parse_states_request_cities
        )

    def parse_states_request_cities(self, response):
        for state in response.css('.Directory-listLink::attr(href)'):
            yield scrapy.Request(
                response.urljoin(state.get()),
                callback=self.parse_cities_request_locations
            )

    def parse_cities_request_locations(self, response):
        for city in response.css('.Directory-listLink'):
            city_url = response.urljoin(city.css('::attr(href)').get())
            location_count = city.css('::attr(data-count)').re_first(r'(\d+)')
            if location_count == '1':
                yield scrapy.Request(
                    city_url
                )

            else:
                yield scrapy.Request(
                    city_url,
                    callback=self.parse_locations_request_location
                )

    def parse_locations_request_location(self, response):
        for location in response.css('.Teaser-titleLink'):
            yield scrapy.Request(
                response.urljoin(location.css('::attr(href)').get())
            )

    def parse(self, response):
        item = RetailLocationsItem()
        loader = item.loader(selector=response)

        store_name = ' '.join([val.get().strip() for val in response.css('.ContentBanner-h1 ::text')])
        phone_number = response.css('#phone-main::text').get()

        loader.add_css('street_address', '.c-address-street-1::text')
        loader.add_css('city', '.c-address-city::text')
        loader.add_css('state', '.c-address-state::text')
        loader.add_css('zip_code', '.c-address-postal-code::text')
        loader.add_css('latitude', '.coordinates [itemprop="latitude"]::attr(content)')
        loader.add_css('longitude', '.coordinates [itemprop="longitude"]::attr(content)')

        loader.add_value(None, {
            'retailer_name': 'Safeway',
            'country': 'United States',
            'store_name': store_name,
            'store_url': response.request.url,
            'store_phone': phone_number,
            'store_id': phone_number
        })

        yield loader.load_item()
