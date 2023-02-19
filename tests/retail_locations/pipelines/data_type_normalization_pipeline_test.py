from retail_locations.pipelines import DataTypeNormalizationPipeline


def test_lat_lon_as_float():
    item = {'lat': '100', 'lon': '-100'}
    pipeline = DataTypeNormalizationPipeline()
    pipeline.process_item(item, None)

    assert item['lat'] == 100.0
    assert item['lon'] == -100.0


def test_zip_code_has_leading_zeros():
    item = {'zip_code': '1234'}
    pipeline = DataTypeNormalizationPipeline()
    pipeline.process_item(item, None)

    assert item['zip_code'] == '01234'


def test_zip_code_only_has_first_five():
    item = {'zip_code': '12345-6789'}
    pipeline = DataTypeNormalizationPipeline()
    pipeline.process_item(item, None)

    assert item['zip_code'] == '12345'
