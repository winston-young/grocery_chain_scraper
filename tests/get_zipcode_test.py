from retail_locations.resources.location_data import get_zipcode_coordinates, get_zipcode_from_coordinates


def test_get_zipcode_coordinates():
    assert get_zipcode_coordinates("01850") == {
        "latitude": 42.656045,
        "longitude": -71.303309,
        "zipcode": "01850"
    }

    assert get_zipcode_from_coordinates(37.452961, -122.181725) == '94025'
