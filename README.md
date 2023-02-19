# Winston Young - Grocery Chain Location Extractor

Python scrapy repo designed to extract location data from well known grocery chains (Aldi, Kroger, Safeway, Super One, and Whole Foods)


## Data Normalization
Data collected from the internet is messy. To produce meaningful and usable data, normalization and cleaning techniques are used.

 - Household values like the date and time of data extraction, and the name of the crawling spider are automatically added
 - Missing values like the location country and retailer name are inferred and added
 - If the lat/lng coordinates are missing, they are calculated collected from a zip code data file using the existing zip code
 - Lat/lng coordinate values are converted to floats
 - The US state name is normalized, the abbreviation is always used over the full name
 - Zip codes are formatted to only include the first five values
 - A deduplication process is used using the retailer website and store id as a location key

## Tests
Proper data parsing and normalization are important. There are a series of tests in `retail_locations/tests`. Various tests for geographic parsing and data normalization are included.

## Geographic Processing
Various geographic utility methods are included in `location_data.py`. These are used for generating missing coordinate values, as well as generating an efficient (as small as possible with full coverage) input list of a zip code grid. This grid provides a minimum number of zip codes at a given radius to request retail locations.

## Running a retail location scraper

 1. Install the virtual environment from the Pipfile.
 2. Open `debug_runner.py`.
 3. Edit the desired values for the spider to run, and the output filename and type. 
 4. Common output types include CSV, JSON, and JL.
 5. This executes the command `scrapy crawl safeway -s HTTPCACHE_ENABLED=false -o sample_safeway_output.csv`
 6. A sample data output (from the above command) is included: `sample_safeway_output.csv`