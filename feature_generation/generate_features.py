import sys
import argparse
import datetime
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('label_file')
parser.add_argument('output_file')
args = parser.parse_args()

conn = pymongo.MongoClient('localhost')
db = conn['nicta']

current_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
delta = datetime.timedelta(1)

video_features = {}
valid_videos = {}

for line in open(args.label_file):
    tokens = line.strip().split(',')
    valid_videos[tokens[0]] = tokens[3]

print 'valid', len(valid_videos)
output = open(args.output_file, 'w')

while current_date <= end_date:
    current_date_str = str(current_date).split()[0]
    print current_date_str

    coll_name = 'features_' + current_date_str
    feature_coll = db[coll_name]

    i = 0
    written = 0

    for result in feature_coll.find():
        i += 1
        if i % 100000 == 0:
            print i, written

        vid_id = result['_id']
        if vid_id not in valid_videos:
            continue

        if valid_videos[vid_id] != current_date_str:
            continue

        has_mention = result['value']['has_mention']
        has_hashtag = result['value']['has_hashtag']
        is_rt = result['value']['is_rt']
        is_nbc = result['value']['is_nbc']
        tweet_count = result['value']['tweet_count']
    
        written += 1
        output.write(vid_id + ',' + str(has_mention) + ',' + str(has_hashtag) + ',' + str(is_rt) + ',' + str(is_nbc) + ',' + str(tweet_count) + '\n')

    current_date += delta
    #print "next:", current_date
output.close()
