import sys
import time
import traceback
import tweepy


class AngusBot():
    """
    Twitterbot for daily tweets from Angus Maclise's "Year"
    """

    def __init__(self):

        # twitter oauth keys and tokens here
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_token = ""
        self.access_token_secret = ""
        
        # tweet storage file
        self.filename = "angus maclise - year.txt"

        # create a day-message text dictionary from file
        self.text = {}
        with open(self.filename, 'r') as f:
            for line in f:
                entry = line.strip().split("\t")
                self.text[entry[0]] = entry[1]

        # access twitter api via tweepy
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self):
    
        # select today's tweet from text
        new_tweet = self.text[time.strftime("%b %d")]
    
        # check if this tweet has already been posted before tweeting
        if self.valid_tweet(new_tweet):
            try:
                print("tweeting: " + self.api.update_status(status=new_tweet).text)
            except tweepy.TweepError:
                print(traceback.format_exc())
        else:
            print("error: " + new_tweet + " was already tweeted.")
    
    def valid_tweet(self, new_tweet, previous_tweets=7):
        
        # check recent tweets for today's tweet and abort if duplicate
        for tweet in self.api.user_timeline(count=previous_tweets):
            try:
                if new_tweet == tweet.text: 
                    return False # already tweeted!
            except UnicodeEncodeError:
                print("Ignoring a UnicodeEncodeError in valid_tweet")
        return True # didn't find a match
    
    def favorite_mentions(self):
        for mention in tweepy.Cursor(self.api.mentions_timeline).items():
            if not mention.favorited:
                try:
                    self.api.create_favorite(mention.id)
                    print("favoriting mention: " + mention.text)
                except (tweepy.TweepError, UnicodeEncodeError) as e: 
                    print(e)


if __name__ == "__main__":
    bot = AngusBot()
    bot.tweet()
    bot.favorite_mentions()