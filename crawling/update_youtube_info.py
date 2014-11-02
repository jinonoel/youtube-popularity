import pymongo
import sys
import datetime

sys.path.append('/home/jnoel/YTCrawl')
import crawler

start_date = '2014-09-27'

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']

i = 0

last_updated = {}

print "Get last updated"
for result in coll.find({'uploadDate' : {'$gte' : start_date}}, timeout=False):
    i += 1
    if i % 1000 == 0:
        print i, len(last_updated)


    vid_id = result['video_id'].split('#')[0]
    if vid_id in last_updated:
        continue

    #if result['uploadDate'] > '2014-09-28':
    #    continue


    upload_date = datetime.datetime.strptime(result['uploadDate'], '%Y-%m-%d')
    days_delta = datetime.timedelta(len(result['dailyViewCount']))
    last_update = str(upload_date + days_delta).split()[0]


    last_updated[vid_id] = {
        'upload_date' : upload_date,
        'last_update' : last_update
    }

sorted_vids = sorted(last_updated.keys(), key=lambda vid: last_updated[vid]['last_update'])

crawler = crawler.Crawler()

for vid_id in sorted_vids:
    print vid_id, last_updated[vid_id]['upload_date'], last_updated[vid_id]['last_update']

    try:
        data = crawler.single_crawl(vid_id)
        if 'uploadDate' not in data or 'dailyViewcount' not in data:
            continue

        uploadDate = str(data['uploadDate']).split()[0]

        coll.update({
            'video_id' : vid_id
        }, {
            '$set' : {
                'uploadDate' : uploadDate,
                'dailyViewCount' : data['dailyViewcount']
            }
        })
    except Exception as ex:
        print "Exception:", ex, vid_id
    except:
        print "WTF"

conn.close()
