import tweepy

####input your credentials here
consumer_key = '###'
consumer_secret = '###'
access_token = '###'
access_token_secret = '###'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,retry_count=3, retry_delay=20,
                 retry_errors=set([401, 404, 500, 503]))


for page in tweepy.Cursor(api.search,q="#tunisia",count=20,
                           lang="en",
                           since="2017-04-03",tweet_mode='extended').pages():
    for tweet in page:
    	#print("full_text",tweet._json['full_text'].replace('\n',''),tweet._json.keys())
    	#print(tweet._json)
    	urls = []
    	if 'urls' in tweet._json['entities'].keys():
    		urls = tweet._json['entities']['urls']
    		if(len(urls)>0):
		    	if 'hashtags' in tweet._json['entities'].keys():
		    		hashtags = tweet._json['entities']['hashtags']
		    	if 'full_text' in tweet._json.keys():
		    		full_text = tweet._json['full_text']
		    	print(hashtags,urls,full_text)
