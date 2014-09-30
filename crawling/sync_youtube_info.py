import sys
import argparse
import datetime
import calendar
import pymongo

sys.path.append('/Users/jnoel/YTCrawl')
import crawler


parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('delta')
args = parser.parse_args()

start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
current_date = start_date
delta = datetime.timedelta(int(args.delta))

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']

crawler = crawler.Crawler()

while current_date < end_date:
    print current_date
    mr_name = 'features_' + str(current_date).split()[0]
 
    i = 0
    for result in mr_name.find({}, ['_id'], timeout=False):
        vid_id = result['_id']

        i += 1
        if i % 100 == 0:
            print date, i

        try:
            data = crawler.single_crawl(vid_id)
            coll.insert(data)
        except:
            print "Unexpected error:", sys.exc_info()[0]

    current_date += delta

db.close()
