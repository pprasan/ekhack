from tweepy.streaming import StreamListener
from textblob import TextBlob
import MySQLdb
from datetime import datetime

import os
import re

import MySQLdb

# conn.close()

class TweetStreamListener(StreamListener):

    def __init__(self):
        self.sql_insert_tweet = '''
                INSERT INTO `tweets`(
                `country_code`,
                `created_at`,
                `sentiment`)
                VALUES (%s, %s, %s);
            '''
        self.conn = MySQLdb.connect(host= "localhost", user="root", passwd="imrenagi", db="emirates")
        self.x = self.conn.cursor()
        super(TweetStreamListener, self).__init__()

    def on_status(self, status):
        if status.place:
            # print status.place
            created_at = status.created_at
            country_code = status.place.country_code
            sentiment = self.get_tweet_sentiment(status.text)

            try:
                self.x.execute(self.sql_insert_tweet, [country_code, created_at, sentiment])
                self.conn.commit()
            except:
                self.conn.rollback()


    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
