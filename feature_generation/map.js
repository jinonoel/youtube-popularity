function() {
    var getYoutubeId1 = function(url) {
	var vars = url.split('?')[1].split('&');
	for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split('=');
            if (decodeURIComponent(pair[0]) == 'v') {
		return decodeURIComponent(pair[1]);
            }
	}
	
	return '';
    }
    
    var getYoutubeId2 = function(url) {
	tokens = url.split('/');
	videoId = tokens[tokens.length-1];
	
	if (videoId.indexOf('?')) {
	    return videoId.split('?')[0];
	}
	else {
	    return videoId;
	}
    }

    var user = this.user.id;
    var entities = this.entities;
    var urls = entities.urls;
    var text = this.text;

    var hasHashtag = false;
    var hasMention = false;
    var isRT = false;
    var isNBC = false;

    if (typeof entities != 'undefined') {
	if (typeof entities.user_mentions != 'undefined' && entities.user_mentions.length > 0) {
	    hasMention = true;
	    if (text.charAt(0) == '@') isNBC = true;
	}

	if (typeof entities.hashtags != 'undefined' && entities.hashtags.length > 0) {
	    hasHashtag = true;
	}

	if (typeof this.retweeted_status != 'undefined' && typeof this.retweeted_status.id != 'undefined') {
	    isRT = true;
	}
    }
    
    for (var i = 0; i < entities.urls.length; i++) {
	var expanded = entities.urls[i].expanded_url;

	tweets = []
	key = ''
	
	if (expanded.indexOf("youtube") > -1 && expanded.indexOf('?') > -1) {
	    key = getYoutubeId1(expanded);
	}
	else if (expanded.indexOf("youtu.be") > -1 && expanded.indexOf('/') > -1) {
	    key = getYoutubeId2(expanded);
	}

	if (key != '') {
	    tweets.push({
		timestamp : this.timestamp_ms, 
		user : user,
		has_mention : hasMention,
		has_hashtag : hasHashtag,
		is_rt : isRT,
		is_nbc : isNBC,
		text : text
	    });

	    emit(key, {tweets : tweets});
        }
    }
}
