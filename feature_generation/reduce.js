function(key, values) {
    var tweetData = {
	has_mention : 0,
	has_hashtag : 0,
	is_rt : 0,
	is_nbc : 0
    }
   
    for (var i = 0; i < values.length; i++) {
	tweetData.has_mention += values[i].has_mention;
	tweetData.has_hashtag += values[i].has_hashtag;
	tweetData.is_rt += values[i].is_rt;
	tweetData.is_nbc += values[i].is_nbc;
    }
    
    return tweetData;
}
