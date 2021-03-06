import sys
import argparse
import datetime
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('A')
parser.add_argument('B')
parser.add_argument('output_file')
parser.add_argument('baseline_file')
args = parser.parse_args()

start_date = args.start_date
A_days = int(args.A)
B_days = int(args.B)

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
coll = db['videos']


video_views = {}

i = 0
less = 0
for result in coll.find({'uploadDate' : {'$gte' : start_date}}):
    i += 1
    if i % 100 == 0:
        print i, len(video_views), len(daily_counts), less

    vid_id = result['video_id'].split('#')[0]
    if vid_id in video_views:
        continue
    
    upload_date = result['uploadDate']
    daily_counts = result['dailyViewCount']

    if len(daily_counts) < B_days:
        less += 1
        continue

    total_views = 0
    baseline_views = 0

    for j in range(A_days):
        baseline_views += daily_counts[j]

    for j in range(B_days):
        total_views += daily_counts[j]

    video_views[vid_id] = {
        'views' : total_views,
        'baselineViews' : baseline_views,
        'uploadDate' : upload_date
    }

print 'Videos:', len(video_views)

sorted_vids = sorted(video_views, key=lambda vid: video_views[vid]['views'], reverse=True)
positive_count = int(len(video_views) * 0.05)
j = 0

output = open(args.output_file, 'w')
baseline_file = open(args.baseline_file, 'w')

for vid in sorted_vids:
    if (j < positive_count):
        output.write(vid + ",1," + str(video_views[vid]['views']) + "," + video_views[vid]['uploadDate'] + "\n")
        j += 1
    else:
        output.write(vid + ",0," + str(video_views[vid]['views']) + "," + video_views[vid]['uploadDate'] + "\n")

    baseline_file.write(vid + "," + str(video_views[vid]['baselineViews']) + "\n")

output.close()
baseline_file.close()


