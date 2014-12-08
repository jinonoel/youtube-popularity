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

    var userMentions = [];

    if (typeof entities != 'undefined') {
	if (typeof entities.user_mentions != 'undefined' && entities.user_mentions.length > 0) {
	    hasMention = 1;
	    if (text.charAt(0) == '@') isNBC = 1;

            for (var i = 0; i < entities.user_mentions.length; i++) {
		if (typeof entities.user_mentions[i].screen_name != 'undefined' && entities.user_mentions[i].screen_name.length > 0) {
		    userMentions.push(entities.user_mentions[i].screen_name);
		}
            }
	}

	if (typeof entities.hashtags != 'undefined' && entities.hashtags.length > 0) {
	    hasHashtag = 1;
	}

	if (typeof this.retweeted_status != 'undefined' && typeof this.retweeted_status.id != 'undefined') {
	    isRT = 1;
	}
    }

    var hasHashtagInteraction = 0;
    var isRTInteraction = 0;

    if (hasMention > 0 && hasHashtag > 0) {
	hasHashtagInteraction = 1;
    }

    if (hasMention > 0 && isRT > 0) {
	isRTInteraction = 1;
    }

    userData = {
	has_mention : hasMention,
	has_hashtag : hasHashtag,
	has_hashtag_interaction : hasHashtagInteraction,
	is_rt : isRT,
	is_rt_interaction : isRTInteraction,
	is_nbc : isNBC,
        tweet_count : 1,
	user_mentions : userMentions,
	user_interactions : {
	    mention : [],
	    hashtag : [],
	    rt : [],
	    nbc : []
	}
    };
    
    emit(key, userData);
}
