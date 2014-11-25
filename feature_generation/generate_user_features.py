import sys
import argparse
import datetime
import pymongo

parser = argparse.ArgumentParser()
parser.add_argument('date')
parser.add_argument('output_file')
args = parser.parse_args()

conn = pymongo.MongoClient('localhost')
db = conn['nicta']

video_features = {}

output = open(args.output_file, 'w')

coll_name = 'features_' + args.date + '_10'
feature_coll = db[coll_name]

i = 0
written = 0


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

for result in feature_coll.find():
    i += 1
    if i % 100000 == 0:
        print i, written

    user_id = result['_id']
    has_mention = result['value']['has_mention']
    has_hashtag = result['value']['has_hashtag']
    is_rt = result['value']['is_rt']
    is_nbc = result['value']['is_nbc']
    tweet_count = result['value']['tweet_count']
    
    written += 1

    if not is_ascii(user_id):
        continue

    output.write(user_id + ',' + str(has_mention) + ',' + str(has_hashtag) + ',' + str(is_rt) + ',' + str(is_nbc) + ',' + str(tweet_count) + '\n')


output.close()
