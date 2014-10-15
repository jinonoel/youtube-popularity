import sys
import argparse
import datetime
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('mid_date')
parser.add_argument('end_date')
parser.add_argument('output_file')
args = parser.parse_args()

start_date = args.start_date
mid_date = datetime.datetime.strptime(args.mid_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']

#output = db['total_views']
#output.remove()

video_views = {}
video_mid_views = {}

i = 0
for result in coll.find({'uploadDate' : {'$gte' : start_date}}):
    i += 1
    if i % 100 == 0:
        print i, len(video_views), len(daily_counts)

    upload_date = datetime.datetime.strptime(result['uploadDate'], '%Y-%m-%d')
    if upload_date > mid_date:
        continue

    days = (end_date - upload_date).days 
    if days < 0:
        continue

    daily_counts = result['dailyViewCount']

    total_views = 0

    for j in range(0, days + 1):
        if j < len(daily_counts):
            total_views += daily_counts[j]

    if total_views == 0:
        continue

    video_views[result['video_id']] = total_views
    
    mid_days = (mid_date - upload_date).days
    if mid_days < 0 or len(daily_counts) < mid_days:
        continue

    mid_views = 0
    for j in range(0, mid_days+1):
        if j < len(daily_counts):
            mid_views += daily_counts[j]

    video_mid_views[result['video_id']] = mid_views

print 'Videos:', len(video_views)

sorted_vids = sorted(video_views, key=video_views.__getitem__, reverse=True)
positive_count = int(len(video_views) * 0.05)
j = 0

output = open(args.output_file, 'w')

for vid in sorted_vids:
    if (j < positive_count):
        output.write(vid + ",1," + str(video_views[vid]) + "\n")
        j += 1
    else:
        output.write(vid + ",0," + str(video_views[vid]) + "\n")

output.close()
