import pytest
import scrapy
from retail_locations.pipelines import AddRetailNamePipeline


class MockSpider(scrapy.Spider):
    name = 'spidername'


def test_item_with_retailer_name():
    item, spider, pipeline = setup()
    item['retailer_name'] = 'test_retail_name'
    pipeline.process_item(item, spider)

    assert item['retailer_name'] == 'test_retail_name'


def test_only_spider_with_retailer_name_defined():
    item, spider, pipeline = setup()
    spider.retailer_name = 'defined_retailer_name'
    pipeline.process_item(item, spider)

    assert item['retailer_name'] == 'defined_retailer_name'


def test_item_takes_precedent_over_spider_retailer_name():
    item, spider, pipeline = setup()
    item['retailer_name'] = 'item_name'
    spider.retailer_name = 'spider_name'
    pipeline.process_item(item, spider)

    assert item['retailer_name'] == 'item_name'


def test_raises_exception_if_not_defined():
    item, spider, pipeline = setup()

    with pytest.raises(AttributeError):
        pipeline.process_item(item, spider)


def setup():
    item = {'website': 'www.example.com'}
    spider = MockSpider()
    pipeline = AddRetailNamePipeline()
    return [item, spider, pipeline]
