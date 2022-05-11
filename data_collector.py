import tweepy
import csv
import pandas as pd
####input your credentials here
consumer_key = 'zHkeGOeToo7XpA5uMIJrLqmM5'
consumer_secret = 'FbawrvtrOrqf8NOkaxXc7eWf4m1HAC2KruizGKP6N8VRGWZa95'
access_token = '1513864218180784132-JfISXP8APdCNjNPyplURTLbmGRCTUM'
access_token_secret = 'pZQ6ejSvWmws1a3EMeB6ntfE9ghwZ1q8WOapWN9ForXci'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def scraptweets(search_hashtag, date_since, numTweets, numRuns):
    db_tweets = pd.DataFrame(columns = ['username', 'userID', 'location', 'followers',
                                        'retweeted_og', 'tweetcreatedts', 'text', 'hashtags'])
        
    tweets = tweepy.Cursor(api.search_tweets, q=search_hashtag, lang='en', tweet_mode='extended').items(numTweets)
    tweet_list = [tweet for tweet in tweets]
    tweets_collected = 0
    
    for tweet in tweet_list:
        username = tweet.user.screen_name
        userID = tweet.user.id
        location = tweet.user.location
        followers = tweet.user.followers_count
        tweetcreatedts = tweet.created_at
        hashtags = tweet.entities['hashtags']
        
        try:
            retweeted_og = str(tweet.retweeted_status.user.screen_name)
            #If retweet, view original tweeter
            #text = tweet.retweeted_status.full_text
        except AttributeError as e: #Not a retweet
            retweeted_og = 'none'
        text = '\n' + tweet.full_text
        
        ith_tweet = [username, userID, location, followers, retweeted_og, tweetcreatedts, text, hashtags]
        db_tweets.loc[len(db_tweets)] = ith_tweet
        tweets_collected += 1
        
    filename = 'collected_data_#quitsmoking.csv'
    db_tweets.to_csv(filename, index = False)
    print(tweets_collected)

search_hashtag = '#quitsmoking'
date_since = '2022-04-13'
scraptweets(search_hashtag, date_since, 1000, 1)


