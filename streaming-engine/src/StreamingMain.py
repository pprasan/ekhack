#Import the necessary methods from tweepy library
from TweetStreamListener import TweetStreamListener

from tweepy import OAuthHandler
from tweepy import Stream

import os
import re

#Variables that contains the user credentials to access Twitter API
access_token = os.environ['TWITTER_ACCESS_TOKEN_KEY']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.sample()
