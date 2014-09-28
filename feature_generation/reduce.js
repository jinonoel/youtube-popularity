function(key, values) {
    var tweets = [];
   
    for (var i = 0; i < values.length; i++) {
	vTweets = values[i].tweets;
	
	for (var j = 0; j < vTweets.length; j++) {
	    tweets.push(vTweets[j]);
	}
    }
    
    return {tweets : tweets};
}
