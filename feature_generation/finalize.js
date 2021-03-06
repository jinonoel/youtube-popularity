function(key, value) {
    var hashtagCount = 0;
    var mentionCount = 0;
    var nbcCount = 0;
    var rtCount = 0;
    var uniqueUsers = [];
    var finalVal = {}

    for (var i = 0; i < value.tweets.length; i++) {
	if (value.tweets[i].has_mention) mentionCount++;
	if (value.tweets[i].has_hashtag) hashtagCount++;
	if (value.tweets[i].is_rt) rtCount++;
	if (value.tweets[i].is_nbc) nbcCount++;
	
	var added = false;
	for (var j = 0; j < uniqueUsers.length; j++) {
	    if (uniqueUsers[j] == value.tweets[i].user) {
		added = true;
		break;
	    }
	}
	
	if (!added) {
	    uniqueUsers.push(value.tweets[i].user);
	}
    }

    finalVal.hashtag_count = hashtagCount;
    finalVal.mention_count = mentionCount;
    finalVal.nbc_count = nbcCount;
    finalVal.rt_count = rtCount;
    finalVal.user_count = uniqueUsers.length;
    finalVal.tweet_count = value.tweets.length;

    return value;
}
