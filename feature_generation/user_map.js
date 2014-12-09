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
    var userHashtags = [];
    var userRTs = [];
    var userNBCs = [];


    if (typeof entities != 'undefined') {
	if (typeof entities.user_mentions != 'undefined' && entities.user_mentions.length > 0) {
	    hasMention = 1;
	    if (text.charAt(0) == '@') {
		isNBC = 1;
	    }

            for (var i = 0; i < entities.user_mentions.length; i++) {
		if (typeof entities.user_mentions[i].screen_name != 'undefined' && entities.user_mentions[i].screen_name.length > 0) {
		    userMentions.push(entities.user_mentions[i].screen_name);

		    if (entities.user_mentions[i].indices[0] == 0) {
			userNBCs.push(entities.user_mentions[i].screen_name);
		    }
		}
            }
	}

	if (typeof entities.hashtags != 'undefined' && entities.hashtags.length > 0) {
	    hasHashtag = 1;

	    for (var i = 0; i < entities.hashtags.length; i++) {
		if (typeof entities.hashtags[i].text != 'undefined' && entities.hashtags[i].text.length > 0) { 
		    userHashtags.push(entities.hashtags[i].text);
		}
            }
	}

	if (typeof this.retweeted_status != 'undefined' && typeof this.retweeted_status.id != 'undefined') {
	    isRT = 1;

	    userRTs.push(this.retweeted_status.user.screen_name);
	}
    }

    userData = {
	has_mention : hasMention,
	has_hashtag : hasHashtag,
	is_rt : isRT,
	is_nbc : isNBC,
        tweet_count : 1,
	mentions : userMentions,
	hashtags : userHashtags,
	rts :userRTs,
	nbcs : userNBCs
    };
    
    emit(key, userData);
}
