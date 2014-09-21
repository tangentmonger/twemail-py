import unittest
import pickle
import mock
import datetime
from twemail import Twemail
from TwitterAPI import TwitterAPI

class TwemailTest(unittest.TestCase):

    def test_get_last_tweet_id(self):
        twemail = Twemail()
        self.assertEqual(twemail.get_last_tweet_id('test/record.log'), 3)

    def test_get_missing_file_lest_tweet_id(self):
        twemail = Twemail()
        self.assertEqual(twemail.get_last_tweet_id('no/such/file'), None)

    def test_get_missing_content_run_time(self):
        twemail = Twemail()
        self.assertEqual(twemail.get_last_tweet_id('test/empty.log'), None)

    def test_process_raw_tweets_success(self):
        #Using previously pickled data of 5 tweets:
        #with open("../test/raw_tweets.pickle", 'wb') as f:
        #   pickle.dump(raw_tweets, f)
        raw_tweets = pickle.load(open("test/raw_tweets.pickle", "rb"))
        twemail = Twemail()
        processed_tweets = twemail._process_raw_tweets(raw_tweets)
        self.assertEqual(len(processed_tweets), 5)

    def test_process_raw_tweets_fail(self):
        #this data is an unsuccessful (unauthenticated) attempt
        raw_tweets = pickle.load(open("test/raw_tweets_fail.pickle", "rb"))
        twemail = Twemail()
        processed_tweets = twemail._process_raw_tweets(raw_tweets)
        self.assertEqual(len(processed_tweets), 0)

    def test_parse_tweet(self):
        raw_tweets = pickle.load(open("test/raw_tweets.pickle", "rb"))
        twemail = Twemail()
        #it = iter(raw_tweets.get_iterator())
        it = iter(raw_tweets)
        raw_tweet = next(it)
        parsed_tweet = twemail._parse_tweet(raw_tweet)
        self.assertEqual(parsed_tweet["text"], "@Alittlenutmeg oh, that's ages away!")
        self.assertEqual(str(parsed_tweet["datetime"]), "2014-09-20 10:27:44+01:00")
        self.assertEqual(parsed_tweet["author"], "Alittlenutmeg")
        self.assertEqual(parsed_tweet["id"], 513258196925161472)
    
    def test_get_authenticated_api(self):
        twemail = Twemail()
        api = twemail._get_authenticated_api()
        self.assertIsNotNone(api)

    def test_format_tweets(self):
        text = "foo"
        tweet_id = 42
        author = "bob"
        date = datetime.datetime.now()
        tweets = [{"text":text, "id":tweet_id, "author":author, "datetime":date}]
        twemail = Twemail()
        content = twemail.format_tweets(tweets)
        self.assertIn(text, content)
        self.assertIn(str(tweet_id), content)
        self.assertIn(author, content)
        self.assertIn(str(date.hour), content)

    @mock.patch('smtplib.SMTP')
    def test_sendmail(self, mock_smtp):
        email_content = "foo"
        email_address = "bar@baz.com"
        twemail = Twemail()
        twemail.send_email(email_content, email_address)
        mock_smtp.return_value.sendmail.assert_called()
        mock_smtp.return_value.quit.assert_called()
        
        

    def test_record_last_tweet_ok(self):
        tweets = [{"datetime":2013, "id":42}, {"datetime":2014, "id":43}, {"datetime":2012, "id":44}]
        path = "test/last_tweet.log"
        twemail = Twemail()
        twemail.record_last_tweet_id(tweets, path)
        with open(path, "r") as log:
            self.assertEqual(log.read(), '{"last_tweet_id": 43, "version": 1}')

    def test_record_last_tweet_no_tweets(self):
        path = "test/last_tweet.log"
        with open(path, 'w'):
            #clear file
            pass
        twemail = Twemail()
        twemail.record_last_tweet_id([], path)
        with open(path, "r") as log:
            self.assertEqual(log.read(), '')


if __name__ == "__main__":
    unittest.main()
