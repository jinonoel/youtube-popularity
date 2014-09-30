import sys
import argparse
import datetime
import calendar

sys.path.append('/Users/jnoel/YTCrawl')
import crawler


parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('end_date')
args = parser.parse_args()

start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
current_date = start_date

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']

crawler = crawler.Crawler()

while current_date < end_date:
    print date

    i = 0
    for result in coll.find({}, ['_id'], timeout=false):
        vid_id = result['_id']

        i += 1
        if i % 100 == 0:
            print date, i

        try:
            data = crawler.single_crawl(vid_id)
            coll.insert(data)
        except:
            print "Unexpected error:", sys.exc_info()[0]

db.close()
