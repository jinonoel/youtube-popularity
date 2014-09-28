import sys

sys.path.append('/Users/jino/Code/YTCrawl')
import crawler

crawler = crawler.Crawler()

data = crawler.single_crawl('OQSNhk5ICTI')

print len(data['dailyViewcount'])
