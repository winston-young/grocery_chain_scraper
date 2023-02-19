# Scrapy settings for retail_locations project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'retail_locations'

SPIDER_MODULES = ['retail_locations.spiders']
NEWSPIDER_MODULE = 'retail_locations.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'retail_locations (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
LOG_FORMATTER = 'retail_locations.logformatter.LogFormatter'

ITEM_PIPELINES = {
    'retail_locations.pipelines.DeduplicationPipeline': 1,
    'retail_locations.pipelines.RetailLocationsPipeline': 100,
    'retail_locations.pipelines.AddRetailNamePipeline': 101,
    'retail_locations.pipelines.NormalizeStatePipeline': 102,
    'retail_locations.pipelines.AddCountryPipeline': 102,
    'retail_locations.pipelines.AddCoordinateValuesPipeline': 500,
    'retail_locations.pipelines.DataTypeNormalizationPipeline': 800
}
