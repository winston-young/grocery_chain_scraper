# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


class RetailLocationsItem(scrapy.Item):

    spider_name = scrapy.Field()

    lastextracted = scrapy.Field(serializer=str)

    objectkey = scrapy.Field()

    # Name common to all locations of a chain retailer, ex: "Best Buy"
    retailer_name = scrapy.Field()

    # Name specific to individual location, ex: "Best Buy Richfield"
    store_name = scrapy.Field()

    # Store url specific to individual location, ex: "https://stores.bestbuy.com/mn/richfield/1000-west-78th-st-281.html?ref=NS&loc=ns100"
    store_url = scrapy.Field()

    street_address = scrapy.Field()

    city = scrapy.Field()

    state = scrapy.Field()

    zip_code = scrapy.Field()

    country = scrapy.Field()

    # Email address for an individual location
    store_email = scrapy.Field()

    # Phone number for an individual location
    store_phone = scrapy.Field()

    # Name of owner/manager for an individual location
    contact_name = scrapy.Field()

    # Geographic coordinates of store location
    latitude = scrapy.Field()
    longitude = scrapy.Field()

    store_id = scrapy.Field()

    def loader(self, **kwargs):
        return RetailLocationLoader(item=self, **kwargs)

    def unique_identifier(self):
        return ':'.join((str(self.get(k)) for k in ('website', 'store_id')))


class RetailLocationLoader(ItemLoader):
    default_input_processor = MapCompose(
        lambda x: x.strip() if type(x) == str else x
    )

    # Default take first extracted candidate
    default_output_processor = TakeFirst()
