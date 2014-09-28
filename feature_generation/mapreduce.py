import pymongo
import datetime
import calendar

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
tweet_coll = db['tweet']

start_date = datetime.datetime(2014, 9, 21)
end_date = datetime.datetime(2014, 9, 22)
current_date = start_date
delta = datetime.timedelta(1)

map_f = open('map.js').read()
reduce_f = open('reduce.js').read()
finalize_f = open('finalize.js').read()

print map_f
print
print reduce_f
print
print finalize_f
print
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
        finalize=finalize_f,
        query={
            'timestamp_ms' : {
                '$gte' : str(start_ts),
                '$lt' : str(end_ts)
            }
        }
    )
