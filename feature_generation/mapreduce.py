import pymongo
import datetime
import calendar
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start_date')
parser.add_argument('end_date')
parser.add_argument('delta')
args = parser.parse_args()

start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d')
delta = datetime.timedelta(int(args.delta))
current_date = start_date

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
tweet_coll = db['tweet']

map_f = open('map.js').read()
reduce_f = open('reduce.js').read()
finalize_f = open('finalize.js').read()

while (current_date < end_date):
    out_name = 'features_' + str(current_date).split()[0]
    print current_date, out_name

    start_ts = calendar.timegm(current_date.utctimetuple()) * 1000
    current_date += delta
    end_ts = calendar.timegm(current_date.utctimetuple()) * 1000

    print start_ts, end_ts

    tweet_coll.map_reduce(
        map_f, 
        reduce_f,
        out_name,
        #finalize=finalize_f,
        query={
            'timestamp_ms' : {
                '$gte' : start_ts,
                '$lt' : end_ts
            }
        }
    )
