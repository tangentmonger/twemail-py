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

    def test_get_missing_file_last_tweet_id(self):
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
        it = iter(raw_tweets)
        raw_tweet = list(it)[2] #a tweet including a mention, a URL and a hashtag
        parsed_tweet = twemail._parse_tweet(raw_tweet)
        self.assertEqual(parsed_tweet["text"], "Want to learn how to create beautiful site? @WagtailCMS engineers are running workshop on Monday. It's FREE! http://t.co/WpUebwFwAE #PyConIE")
        self.assertEqual(str(parsed_tweet["datetime"]), "2014-09-20 09:48:20+01:00")
        self.assertEqual(parsed_tweet["author"], "pyconireland")
        self.assertEqual(parsed_tweet["id"], 513248280705499136)
        self.assertEqual(parsed_tweet["links"], [
            {"start":44, "end":55, "url":"https://twitter.com/WagtailCMS"}, #mention
            {"start":109, "end":131, "url":"http://lanyrd.com/sddyzk"}, #url
            {"start":132, "end":140, "url":"https://twitter.com/hashtag/PyConIE?src=hash"}]) #url
    
    def test_get_authenticated_api(self):
        twemail = Twemail()
        api = twemail._get_authenticated_api()
        self.assertIsNotNone(api)

    def test_format_tweets(self):
        text = "foo"
        tweet_id = 42
        author = "bob"
        date = datetime.datetime.now()
        url = "www.foo.com"
        tweets = [{"text":text, "id":tweet_id, "author":author, "datetime":date, "links": [{"url":url, "start":3, "end":8}]}]
        twemail = Twemail()
        content = twemail.format_tweets(tweets)
        self.assertIn(text, content)
        self.assertIn(str(tweet_id), content)
        self.assertIn(author, content)
        self.assertIn(str(date.hour), content)
        self.assertIn(url, content)

    def test_add_links_to_text(self):
        text = "hello @foo goodbye"
        links = [{"start":6, "end":10, "url":"www.foo.com"}]
        twemail = Twemail()
        text_with_links = twemail._add_links_to_text(text, links)
        self.assertEqual(text_with_links, "hello <a href=\"www.foo.com\">@foo</a> goodbye")

    def test_add_links_to_text_ends(self):
        text = "@foo hi @bar"
        links = [{"start":8, "end":12, "url":"www.bar.com"},
                {"start":0, "end":4, "url":"www.foo.com"}]
        twemail = Twemail()
        text_with_links = twemail._add_links_to_text(text, links)
        self.assertEqual(text_with_links, "<a href=\"www.foo.com\">@foo</a> hi <a href=\"www.bar.com\">@bar</a>")

    def test_add_links_to_text_none(self):
        text = "@foo hi @bar"
        links = []
        twemail = Twemail()
        text_with_links = twemail._add_links_to_text(text, links)
        self.assertEqual(text_with_links, text)


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
