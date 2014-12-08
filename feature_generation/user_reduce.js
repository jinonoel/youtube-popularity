function(key, values) {
    var userData = {
	has_mention : 0,
	has_hashtag : 0,
	has_hashtag_interaction : 0,
	is_rt : 0,
	is_rt_interaction : 0,
	is_nbc : 0,
	tweet_count : 0,
	user_mentions : [],
	user_interactions : {
	    mention : [],
	    hashtag : [],
	    rt : [],
	    nbc : []
	}
    }
   
    for (var i = 0; i < values.length; i++) {
	userData.has_mention += values[i].has_mention;
	userData.has_hashtag += values[i].has_hashtag;
	userData.has_hashtag_interaction += values[i].has_hashtag_interaction;
	userData.is_rt += values[i].is_rt;
	userData.is_rt_interaction += values[i].is_rt_interaction;
	userData.is_nbc += values[i].is_nbc;
	userData.tweet_count += values[i].tweet_count;

	for (var j = 0; j < values[i].user_mentions.length; j++) {
	    user = values[i].user_mentions[j];
	    userData.user_mentions.push(user);

	    if (values[i].has_mention > 0) {
		userData.user_interactions.mention.push(user);
	    }

	    if (values[i].has_hashtag > 0) {
		userData.user_interactions.hashtag.push(user);
	    }

	    if (values[i].is_rt > 0) {
		userData.user_interactions.rt.push(user);
	    }

	    if (values[i].is_nbc > 0) {
		userData.user_interactions.nbc.push(user);
	    }
	}
    }
    
    return userData;
}
