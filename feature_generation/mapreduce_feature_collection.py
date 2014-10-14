import pymongo
import datetime
import calendar
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('end_date')
args = parser.parse_args()

start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
tweet_coll = db['tweet']

map_f = open('map.js').read()
reduce_f = open('reduce.js').read()
finalize_f = open('finalize.js').read()

out_name = 'features_' + str(start_date).split()[0] + '_' + str(end_date).split()[0]

start_ts = calendar.timegm(start_date.utctimetuple()) * 1000
end_ts = calendar.timegm(end_date.utctimetuple()) * 1000

print start_ts, end_ts

tweet_coll.map_reduce(
    map_f, 
    reduce_f,
    out_name,
    query={
        'timestamp_ms' : {
            '$gte' : start_ts,
            '$lt' : end_ts
        }
    }
)

conn.close()
