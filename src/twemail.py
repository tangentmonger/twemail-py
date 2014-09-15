#!usr/bin/python3

#stdlib
import urllib.parse
import json

#local
from secrets import Secrets

class Twemail:

    def run(self):
        last_tweet_id = self.get_last_tweet_id(Secrets.record_path)
        tweets = None
        if last_tweet_id:
            tweets = self.get_tweets_since(last_tweet_id)
        else:
            tweets = self.get_last_five_tweets()
        email_content = self.format_tweets(tweets)
        success = self.send_email(email_content)
        if success:
            self.record_last_tweet_id()
            
    def get_last_tweet_id(self, record_path):
        last_tweet_id = None
        try:
            with open(record_path, 'r') as record_file:
                record = json.load(record_file)
                last_tweet_id = record['last_tweet_id']
        except:
            pass
        return last_tweet_id


if __name__ == "__main__":
    twemail = Twemail()
    twemail.run()

  
