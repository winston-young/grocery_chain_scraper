# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from retail_locations.resources.location_data import get_zipcode_coordinates, us_states, us_states_names, us_states_abbreviations

import datetime
import re


class DeduplicationPipeline:

    def __init__(self):
        self.processed_items = set()

    def process_item(self, item, spider):
        if item.unique_identifier() in self.processed_items:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.processed_items.add(item.unique_identifier())
            return item


class RetailLocationsPipeline:
    def process_item(self, item, spider):
        item['spider_name'] = 'scrapy/' + spider.name
        item['lastextracted'] = datetime.datetime.now()
        item['objectkey'] = item.unique_identifier()
        return item


class AddRetailNamePipeline:
    def process_item(self, item, spider):
        if not item.get('retailer_name'):
            item['retailer_name'] = spider.retailer_name
        return item


class NormalizeStatePipeline:
    def process_item(self, item, spider):
        if spider.country == 'United States' and item.get('state'):
            item['state'] = item['state'].upper().strip()
            item['state'] = re.sub(r'[^a-zA-Z ]', '', item['state'])
            if item['state'] in us_states_names():
                item['state'] = [value for value in us_states() if value['state'] == item['state'].title()][0]['abbreviation']

            if item['state'] not in us_states_abbreviations():
                item['state'] = ''

        return item


class AddCountryPipeline:
    def process_item(self, item, spider):
        if not item.get('country'):
            if spider.country:
                item['country'] = spider.country
            else:
                item['country'] = 'United States'
        return item


class AddCoordinateValuesPipeline:
    def process_item(self, item, spider):
        if not item.get('latitude') or not item.get('longitude'):
            coordinates = get_zipcode_coordinates(item['zip_code'])
            item['latitude'], item['longitude'] = coordinates['latitude'], coordinates['longitude']
        return item


class DataTypeNormalizationPipeline:
    def process_item(self, item, spider):
        for (prop, func) in self.CONVERTERS.items():
            value = item.get(prop)
            if value:
                item[prop] = func.__call__(value)

        return item

    def format_zip_code(value):
        # Only use first part of a zip_code:
        value = str(value).split('-')[0]

        # Pad with 0s if missing leading 0s:
        value = value.zfill(5)
        return value

    CONVERTERS = {
        'lat': float,
        'lon': float,
        'zip_code': format_zip_code
    }
