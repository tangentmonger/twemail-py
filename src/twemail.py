#!usr/bin/python3

#third party
from TwitterAPI import TwitterAPI
from dateutil import parser
import pytz

#stdlib
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
        
        if tweets:
            email_content = self.format_tweets(tweets)
            success = self.send_email(email_content, Secrets.email_address)
            if success:
                self.record_last_tweet_id(tweets, Secrets.record_path)
            
    def get_last_tweet_id(self, record_path):
        last_tweet_id = None
        try:
            with open(record_path, 'r') as record_file:
                record = json.load(record_file)
                last_tweet_id = record['last_tweet_id']
        except:
            pass
        return last_tweet_id


    def get_tweets_since(self, last_tweet_id):
        twitter = self._get_authenticated_api()
        raw_tweets = twitter.request('statuses/home_timeline', {'since_id':last_tweet_id})
        tweets = self._process_raw_tweets(raw_tweets)
        return tweets

    def get_last_five_tweets(self):
        twitter = self._get_authenticated_api()
        raw_tweets = twitter.request('statuses/home_timeline', {'count':'5'})
        print(raw_tweets.get_iterator().results)
        tweets = self._process_raw_tweets(raw_tweets)
        return tweets

    def _process_raw_tweets(self, raw_tweets):
        tweets = []  
        if raw_tweets.status_code == 200:
            for raw_tweet in raw_tweets:
                tweets.append(self._parse_tweet(raw_tweet))
        else:
            print(raw_tweets.status_code)
            #todo: error reporting
        return tweets

    def _get_authenticated_api(self):
        api = TwitterAPI(Secrets.consumer_key, Secrets.consumer_secret, Secrets.access_token_key, Secrets.access_token_secret, "oAuth1")
        return api

    def _parse_tweet(self, raw_tweet):
        tweet = {}
        tweet['author'] = raw_tweet['user']['screen_name']
        tweet['text'] = raw_tweet['text']
        tweet['id'] = raw_tweet['id']
      
        #these fields are all for display, so convert Twitter's UTC times to local time here
        localtz = pytz.timezone(Secrets.local_timezone)
        local_creation_time = parser.parse(raw_tweet['created_at']).astimezone(localtz)
        tweet['datetime'] = local_creation_time

        return tweet

    def format_tweets(self, tweets):
        tweet_list = sorted(list(tweets), key = lambda tweet: tweet['datetime'])

        content = "\n\n".join("<p><b><a href=\"https://twitter.com/{0}\">{0}:</a> </b>{1}<br/><small><a href=\"https://twitter.com/{0}/status/{3}\">{2}</a></small></p>".format(tweet['author'], tweet['text'], tweet['datetime'].strftime("%A %H:%M"), tweet['id']) for tweet in tweet_list)

        return content

    def send_email(self, email_content, email_address):
        ascii_content = email_content.encode('ascii', 'xmlcharrefreplace').decode('ascii')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Recent tweets"
        msg['From'] = "twemail@noreply.twemail.com"
        msg['To'] = email_address
        msg.attach(MIMEText(ascii_content, 'plain'))
        msg.attach(MIMEText(ascii_content, 'html'))
        s = smtplib.SMTP('localhost')
        s.sendmail(email_address, [email_address], msg.as_string())
        s.quit()
        return True

    def record_last_tweet_id(self, tweets, record_path):
        if tweets and len(tweets) > 0:
            tweet_list = sorted(list(tweets), key = lambda tweet: tweet['datetime'])
            last_tweet = tweet_list[-1]
            record = {'version':1, 'last_tweet_id':last_tweet['id']}
            with open(record_path, 'w') as record_file:
                json.dump(record, record_file)

if __name__ == "__main__":
    twemail = Twemail()
    twemail.run()

  
