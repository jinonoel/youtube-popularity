function() {
    var user = this.user.id;
    var entities = this.entities;
    var urls = entities.urls;
    var text = this.text;

    var hasHashtag = 0;
    var hasMention = 0;
    var isRT = 0;
    var isNBC = 0;

    var key = this.user.screen_name;

    if (typeof entities != 'undefined') {
	if (typeof entities.user_mentions != 'undefined' && entities.user_mentions.length > 0) {
	    hasMention = 1;
	    if (text.charAt(0) == '@') isNBC = 1;
	}

	if (typeof entities.hashtags != 'undefined' && entities.hashtags.length > 0) {
	    hasHashtag = 1;
	}

	if (typeof this.retweeted_status != 'undefined' && typeof this.retweeted_status.id != 'undefined') {
	    isRT = 1;
	}
    }

    userData = {
	has_mention : hasMention,
	has_hashtag : hasHashtag,
	is_rt : isRT,
	is_nbc : isNBC,
        tweet_count : 1,
    };
    
    emit(key, userData);
}
