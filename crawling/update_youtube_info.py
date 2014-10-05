import pymongo
import sys

sys.append('/Users/jnoel/YTCrawl')
import crawler

start_date = '2014-09-27'

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']

i = 0
for resulr in coll.find({'uploadDate' : {'$gte' : start_date}}, timeout=False):
    vid_id = result['_id']

    i += 1
    if i % 1000 == 0:
        print date, i

    try:
        data = crawler.single_crawl(vid_id)
        uploadDate = str(data['uploadDate']).split()[0]

        if uploadDate < start_date:
            print 'wtf date', vid_id
            sys.exit()
        
        if len(data['dailyViewCount']) == 0:
            print 'wtf view count'
            sys.exit()

        coll.update({
            'video_id' : vid_id
        }, {
            'uploadDate' : uploadDate,
            'dailyViewCount' : data['dailyViewCount']
        })
    except Exception as ex:
        print "Exception:", ex, vid_id
    except:
        print "WTF"

db.close()
