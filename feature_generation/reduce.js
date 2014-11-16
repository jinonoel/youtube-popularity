function(key, values) {
    var tweetData = {
	has_mention : 0,
	has_hashtag : 0,
	is_rt : 0,
	is_nbc : 0,
	tweet_count : 0,
	tweets : [],
	authors : []
    }
   
    for (var i = 0; i < values.length; i++) {
	tweetData.has_mention += values[i].has_mention;
	tweetData.has_hashtag += values[i].has_hashtag;
	tweetData.is_rt += values[i].is_rt;
	tweetData.is_nbc += values[i].is_nbc;
	tweetData.tweet_count += values[i].tweet_count;

	for (var j = 0; j < values[i].tweets.length; j++) {
	    if (tweetData.tweets.length < 5) {
		tweetData.tweets.push(values[i].tweets[j]);
		tweetData.authors.push(values[i].authors[j]);
	    }
	}
    }
    
    return tweetData;
}
