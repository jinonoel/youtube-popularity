
import sys
import argparse
import datetime
import calendar
import pymongo

sys.path.append('/home/jnoel/YTCrawl')
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

existing = coll.distinct('video_id')
existing.extend(db['statics_disabled'].distinct('video_id'))

existing_set = set(existing)

print "Existing:", len(existing_set)

crawler = crawler.Crawler()

while current_date < end_date:
    print current_date
    mr_name = 'features_' + str(current_date).split()[0]
 
    i = 0
    for result in db[mr_name].find({}, ['_id'], timeout=False):
        vid_id = result['_id']

        if vid_id in existing_set:
            continue

        i += 1
        if i % 100 == 0:
            print current_date, i

        try:
            data = crawler.single_crawl(vid_id)
            if 'uploadDate' not in data or 'dailyViewcount' not in data:
                continue
            
            coll.insert({
                'video_id' : vid_id,
                'uploadDate' : str(data['uploadDate']).split()[0],
                'dailyViewCount' : data['dailyViewcount']
            })

            existing_set.add(vid_id)

        except Exception as ex:
            if 'statistics disabled' in str(ex):
                db['statics_disabled'].insert({'video_id' : vid_id})
                existing_set.add(vid_id)
            else:
                print "Exception:", ex, vid_id
        except:
            print "WTF"

    current_date += delta

db.close()
