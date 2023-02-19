import json
from pkg_resources import resource_filename


def get_resource_filename(name):
    module = 'retail_locations'
    path = 'resources/{}'
    return resource_filename(module, path.format(name))


def get_resource(name):
    '''Open a JSON file in resources directory and returns it as dict'''

    with open(get_resource_filename(name)) as f:
        return json.load(f)
