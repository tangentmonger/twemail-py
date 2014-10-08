import pickle

from twemail import Twemail

def save_pickled_tweet(tweet_id):
    """Fetch tweet and save raw json data"""
    twemail = Twemail()
    api = twemail._get_authenticated_api()
    request = "statuses/show/:%s" % tweet_id
    #raw_tweet = api.request(request)
    print(raw_tweet.text)
    with open("%s.json" % tweet_id, 'wb') as f:
        pickle.dump(raw_tweet, f)

