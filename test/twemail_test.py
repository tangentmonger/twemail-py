import unittest
from twemail import Twemail

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

if __name__ == "__main__":
    unittest.main()
