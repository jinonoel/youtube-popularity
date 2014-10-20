
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

start_date = args.start_date
end_date = args.end_date


conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']


existing = []

print "Getting existing"
for vid in coll.find():
    existing.append(vid['video_id'])

print "Getting disabled"

for vid in db['statics_disabled'].find():
    existing.append(vid['video_id'])


existing_set = set(existing)

print "Existing:", len(existing_set)

crawler = crawler.Crawler()

mr_name = 'features_' + start_date + '_' + end_date
 
i = 0
for result in db[mr_name].find({}, ['_id'], timeout=False):
    vid_id = result['_id']

    if vid_id in existing_set:
        continue

    i += 1
    if i % 100 == 0:
        print i

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

conn.close()
