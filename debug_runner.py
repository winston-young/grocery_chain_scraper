from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'crawl',
            'safeway',
            '-s',
            'HTTPCACHE_ENABLED=false',
            '-o',
            'sample_safeway_output.csv',
        ]
    )
except SystemExit:
    pass
