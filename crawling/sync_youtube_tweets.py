import twitter
import sys
import json
import pymongo
import datetime
import pprint
import argparse

def get_credentials(config_file):
    credentials = {}

    for line in open(config_file):
        key,val = line.strip().split('=')
        credentials[key] = val

    return credentials

parser = argparse.ArgumentParser()
parser.add_argument('config_file')

args = parser.parse_args()

credentials = get_credentials(args.config_file)

api = twitter.Api(
    consumer_key=credentials['CONSUMER_KEY'], 
    consumer_secret=credentials['CONSUMER_SECRET'], 
    access_token_key=credentials['ACCESS_TOKEN_KEY'], 
    access_token_secret=credentials['ACCESS_TOKEN_SECRET']
)

conn = pymongo.MongoClient('localhost')
db = conn['nicta']
tweet_coll = db['tweet']

to_remove = {
    "coordinates" : "",
    "id_str" : "",
    "in_reply_to_status_id" : "",
    "in_reply_to_screen_name" : "",
    "in_reply_to_user_id" : "",
    "source" : "",
    "truncated" : "",
    "favorited" : "",
    "retweeted" : "",
    "possibly_sensitive" : "",
    "filter_level" : "",
    "user.id_str" : "",
    "user.contributors_enabled" : "",
    "user.is_translator" : "",
    "user.is_translation_enabled" : "",
    "user.profile_background_color" : "",
    "user.profile_background_image_url" : "",
    "user.profile_background_image_url_https" : "",
    "user.profile_background_tile" : "",
    "user.profile_image_url" : "",
    "user.profile_image_url_https" : "",
    "user.profile_link_color" : "",
    "user.profile_sidebar_border_color" : "",
    "user.profile_sidebar_fill_color" : "",
    "user.profile_text_color" : "",
    "user.profile_use_background_image" : "",
    "user.default_profile" : "",
    "user.default_profile_image" : "",
    "user.following" : "",
    "user.follow_request_sent" : "",
    "user.notifications" : "",
    "user.verified" : "",
    "user.utc_offset" : "",
    "user.geo_enabled" : "",
    "user.url" : "",
    "user.protected" : "",
    "retweeted_status.id_str" : "",
    "retweeted_status.truncated" : "",
    "retweeted_status.favorited" : "",
    "retweeted_status.retweeted" : "",
    "retweeted_status.possibly_sensitive" : "",
    "retweeted_status.filter_level" : "",
    "retweeted_status.user.id_str" : "", 
    "retweeted_status.user.contributors_enabled" : "",
    "retweeted_status.user.is_translator" : "",
    "retweeted_status.user.is_translation_enabled" : "",
    "retweeted_status.user.profile_background_color" : "",
    "retweeted_status.user.profile_background_image_url" : "",
    "retweeted_status.user.profile_background_image_url_https" : "",
    "retweeted_status.user.profile_background_tile" : "",
    "retweeted_status.user.profile_image_url" : "",
    "retweeted_status.user.profile_image_url_https" : "",
    "retweeted_status.user.profile_link_color" : "",
    "retweeted_status.user.profile_sidebar_border_color" : "",
    "retweeted_status.user.profile_sidebar_fill_color" : "",
    "retweeted_status.user.profile_text_color" : "",
    "retweeted_status.user.profile_use_background_image" : "",
    "retweeted_status.user.default_profile" : "",
    "retweeted_status.user.default_profile_image" : "",
    "retweeted_status.user.following" : "",
    "retweeted_status.user.follow_request_sent" : "",
    "retweeted_status.user.notifications" : ""
}


dates = [u"Jan", u"Feb", u"Mar", u"Apr", u"May", u"Jun", u"Jul", u"Aug",
    u"Sep", u"Oct", u"Nov", u"Dec"]
dates = dict(map(lambda x: (x[1], x[0]+1), enumerate(dates)))


# transform dates into the internal MongoDb format
def find_created_at(tdict):
    for key, value in tdict.iteritems():
        if key == "created_at":
            tokens = value.split()
            times = map(int, tokens[3].split(":"))
            dt = datetime.datetime(int(tokens[-1]), dates[tokens[1]],
                                   int(tokens[2]), times[0], times[1], times[2], 0)
            tdict[key] = dt.isoformat()+".000"+tokens[-2]
        elif isinstance(value, dict):
            find_created_at(value)



stream = api.GetStreamFilter(track=['youtube', 'youtu be'])
i = 0


for tweet in stream:
    i += 1
    if i % 1000 == 0:
        print i
     
    #delete useless fields for lower disk comsumption
    for key in to_remove:
        tokens = key.split(".")
        try:
            tdict = tweet
            for token in tokens[:-1]:
                tdict = tdict[token]
            del tdict[tokens[-1]]
        except: pass
    
    find_created_at(tweet)
    tweet['timestamp_ms'] = long(tweet['timestamp_ms'])

    try:
        tweet_coll.insert(tweet)
    except pymongo.errors.DuplicateKeyError, e:
        print e
