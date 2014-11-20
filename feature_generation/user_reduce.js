function(key, values) {
    var userData = {
	has_mention : 0,
	has_hashtag : 0,
	is_rt : 0,
	is_nbc : 0,
	tweet_count : 0
    }
   
    for (var i = 0; i < values.length; i++) {
	userData.has_mention += values[i].has_mention;
	userData.has_hashtag += values[i].has_hashtag;
	userData.is_rt += values[i].is_rt;
	userData.is_nbc += values[i].is_nbc;
	userData.tweet_count += values[i].tweet_count;
    }
    
    return userData;
}
