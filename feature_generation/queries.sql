YT-VIEWS

T.tweet(v,t)
SELECT count(*) 
FROM tweet_video 
WHERE video_id=v 
       AND timestamp_ms >= t1 AND timestamp_ms <= t2;

T.hashtag(v,t)
SELECT count(*) 
FROM tweet_video 
     JOIN tweet ON tweet_video.tweet_id=tweet.tweet_id
WHERE video_id=v AND has_hashtag = true
      AND timestamp_ms >= t1 AND timestamp_ms <= t2

T.mention(v,t)
SELECT count(*) 
FROM tweet_video 
     JOIN tweet ON tweet_video.tweet_id=tweet.tweet_id
WHERE video_id=v AND has_mention = true
      AND timestamp_ms >= t1 AND timestamp_ms <= t2;

T.nbcTweet(v,t)
SELECT count(*) 
FROM tweet_video 
     JOIN tweet ON tweet_video.tweet_id=tweet.tweet_id
WHERE video_id=v AND is_nbc = true
      AND timestamp_ms >= t1 AND timestamp_ms <= t2;

T.RT(v,t)
SELECT count(*)
FROM tweet_video
     JOIN tweet ON tweet_video.tweet_id=tweet.tweet_id
WHERE video_id=v AND is_rt = true
      AND timestamp_ms >= t1 AND timestamp_ms <= t2;

G.outdegree(u)
SELECT followers_count FROM user WHERE user_id=u;

G.pagerank(u)
G.hubauthority(u)


A.tweet(u)
A.hashtag(u) 
A.mention(u) 
A.nbcTweet(u) 
A.RT(u)

P.nbcTweet(u)
P.mention(u)
P.RT(u)

