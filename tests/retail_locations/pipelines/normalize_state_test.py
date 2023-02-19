from scrapy import Spider
from retail_locations.pipelines import NormalizeStatePipeline


class MockSpider(Spider):
    name = 'spidername'


def test_capitalizes_us_state_abbreviations():
    item, spider, pipeline = setup()
    spider.country = 'United States'
    item['state'] = 'cA'
    pipeline.process_item(item, spider)

    assert item['state'] == 'CA'


def test_us_state_name_becomes_abbreviation():
    item, spider, pipeline = setup()
    spider.country = 'United States'
    item['state'] = 'MINNESOTA'
    pipeline.process_item(item, spider)

    assert item['state'] == 'MN'


def test_us_state_name_capitalization_normalizes():
    item, spider, pipeline = setup()
    spider.country = 'United States'
    item['state'] = 'cAlifOrnIA'
    pipeline.process_item(item, spider)

    assert item['state'] == 'CA'


def test_us_state_name_removes_non_alphabet_values():
    item, spider, pipeline = setup()
    spider.country = 'United States'
    item['state'] = 'New Hampshire,123  '
    pipeline.process_item(item, spider)

    assert item['state'] == 'NH'


def test_invalid_state_values_removed():
    item, spider, pipeline = setup()
    spider.country = 'United States'
    item['state'] = 'Kalispell'
    pipeline.process_item(item, spider)

    assert item['state'] == ''


def setup():
    item = {
        'website': 'www.example.com'
    }
    spider = MockSpider()
    spider.country = 'United States'
    pipeline = NormalizeStatePipeline()
    return [item, spider, pipeline]
