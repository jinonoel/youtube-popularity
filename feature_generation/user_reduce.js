function(key, values) {
    var userData = {
	has_mention : 0,
	has_hashtag : 0,
	is_rt : 0,
	is_nbc : 0,
	tweet_count : 0,
	mentions : [],
	hashtags : [],
	rts : [],
	nbcs : []
    }
   
    for (var i = 0; i < values.length; i++) {
	userData.has_mention += values[i].has_mention;
	userData.has_hashtag += values[i].has_hashtag;
	userData.is_rt += values[i].is_rt;
	userData.is_nbc += values[i].is_nbc;
	userData.tweet_count += values[i].tweet_count;

	for (var j = 0; j < values[i].mentions.length; j++) {
	    var exists = false;
	    user = values[i].mentions[j];

	    for (var k = 0; k < userData.mentions.length; k++) {
		if (userData.mentions[k] == user) {
		    exists = true;
		    break;
		}
	    }

	    if (!exists) {
		userData.mentions.push(user);
	    }
	}
	

	for (var j = 0; j < values[i].hashtags.length; j++) {
	    var exists = false;
	    user = values[i].hashtags[j];

	    for (var k = 0; k < userData.hashtags.length; k++) {
		if (userData.hashtags[k] == user) {
		    exists = true;
		    break;
		}
	    }

	    if (!exists) {
		userData.hashtags.push(user);
	    }
	}

	for (var j = 0; j < values[i].rts.length; j++) {
	    var exists = false;
	    user = values[i].rts[j];

	    for (var k = 0; k < userData.rts.length; k++) {
		if (userData.rts[k] == user) {
		    exists = true;
		    break;
		}
	    }

	    if (!exists) {
		userData.rts.push(user);
	    }
	}

	for (var j = 0; j < values[i].nbcs.length; j++) {
	    var exists = false;
	    user = values[i].nbcs[j];

	    for (var k = 0; k < userData.nbcs.length; k++) {
		if (userData.nbcs[k] == user) {
		    exists = true;
		    break;
		}
	    }

	    if (!exists) {
		userData.nbcs.push(user);
	    }
	}
    }
    
    return userData;
}
