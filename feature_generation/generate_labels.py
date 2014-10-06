import sys
import argparse
import datetime
import pymongo

parser.argparse.ArgumentParse()
parser.add_argument('start_date')
parser.add_argument('end_date')
args = parser.parse_args()

start_date = args.start_date
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']

#output = db['total_views']
#output.remove()

video_views = {}
total_all_videos = 0

i = 0
for result in coll.find({'uploadDate' : {'$gte' : start_date}}):
    i += 1
    if i % 100 == 0:
        print i, len(video_views)

    upload_date = datetime.datetime.strptime(result['uploadDate'], '%Y-%m-%d')
    days = (upload_date - end_date).days 
    daily_counts = result['dailyViewCount']

    total_views = 0
    for i range(0, days + 1):
        if i >= len(daily_counts):
            total_views += daily_counts[i]

    if total_views == 0:
        continue

    video_views[result['video_id']] = total_views
    total_all_videos += total_views

    if len(video_views) >= 1000:
        break

print 'Videos:', len(video_views)
print 'Total:', total_all_videos
print 'Average:', float(total_all_videos) / len(video_views)

sorted_vids = sorted(video_views, key=video_views.__getitem__)

for vid in sorted_vids:
    print vid, video_views[vid]

