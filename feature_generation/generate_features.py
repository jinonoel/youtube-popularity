import sys
import argparse
import datetime
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('collection')
parser.add_argument('label_file')
parser.add_argument('output_file')
args = parser.parse_args()

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
feature_coll = db[args.collection]

video_features = {}

valid_videos = set()

for line in open(args.label_file):
    tokens = line.strip().split(',')
    valid_videos.add(tokens[0])

output = open(args.output_file, 'w')

i = 0
written = 0

print 'valid', len(valid_videos)

for result in feature_coll.find():
    i += 1
    if i % 10000 == 0:
        print i, written

    vid_id = result['_id']
    if vid_id not in valid_videos:
        continue

    has_mention = result['value']['has_mention']
    has_hashtag = result['value']['has_hashtag']
    is_rt = result['value']['is_rt']
    is_nbc = result['value']['is_nbc']
    tweet_count = result['value']['tweet_count']
    
    written += 1
    output.write(vid_id + ',' + str(has_mention) + ',' + str(has_hashtag) + ',' + str(is_rt) + ',' + str(is_nbc) + ',' + str(tweet_count) + '\n')

output.close()
