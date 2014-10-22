import sys
import argparse
import datetime
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('A')
parser.add_argument('B')
parser.add_argument('output_file')
args = parser.parse_args()

start_date = args.start_date
A_days = int(args.A)
B_days = int(args.B)

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']


video_views = {}

i = 0
for result in coll.find({'uploadDate' : {'$gte' : start_date}}):
    i += 1
    if i % 100 == 0:
        print i, len(video_views), len(daily_counts)

    upload_date = result['uploadDate']
    daily_counts = result['dailyViewCount']

    if len(daily_counts) < B_days:
        continue

    total_views = 0

    for j in range(B_days):
        total_views += daily_counts[j]

    video_views[result['video_id']] = {
        'views' : total_views,
        'uploadDate' : upload_date
    }

print 'Videos:', len(video_views)

sorted_vids = sorted(video_views, key=lambda vid: video_views[vid]['views'], reverse=True)
positive_count = int(len(video_views) * 0.05)
j = 0

output = open(args.output_file, 'w')

for vid in sorted_vids:
    if (j < positive_count):
        output.write(vid + ",1," + str(video_views[vid]['score']) + "," + videos_views[vid]['uploadDate'] + "\n")
        j += 1
    else:
        output.write(vid + ",0," + str(video_views[vid]['score']) + "," + video_views[vid]['uploadDate'] + "\n")

output.close()
