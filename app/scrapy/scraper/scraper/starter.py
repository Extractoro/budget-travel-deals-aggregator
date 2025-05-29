import os
from sys import argv

scraper_name = argv[-1]

spiders = [spider for spider in os.listdir('spiders')]

print(spiders)

test_spider = spiders[2]

