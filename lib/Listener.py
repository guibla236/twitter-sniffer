import tweepy as tw
from .utils import *
from json import dumps

class StListener(tw.StreamListener):
    def __init__(self,DB,location,country_code,debug=True):
        """
        Requirements to create this object:
        -DB Object (which is defined in this app) is required to save the tweets.

        -location is a string that defines the timezone to convert the tweet's date to the tz desired.
         It uses the standard tz database (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) and the default given in main is "America/Montevideo" (GMT-3)

        -The area from which the tweets are detected is a square. Sometimes, when you define that square, Twitter sends you tweets
         from other countries you don't want. This variable permits you to filter that tweets using your desired country code
         (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

        -Debug is a binary attribute that specify if the tweet should be printed when is detected (true, by default) or not (false).

        """
        self.DB=DB
        self.api = tw.api
        self.location=location
        self.debug=debug
        self.country_code=country_code

    def on_status(self,status):
        """
        This function indicates what to do when a tweet is detected.
        If you want to modify the behaviour of the app when detects a new tweet you should transform it.
        """

        if status.place.country_code==self.country_code:
            if status.truncated==True: tweet_text=status.extended_tweet["full_text"]
            else: tweet_text=status.text

            tweet_data=[status.user.screen_name,
                                   tweet_text,
                                   timeZoneTransformer(status,self.location).ctime(),
                                   status.in_reply_to_screen_name,
                                   hashtagsExtractor(status),
                                   userMentionsExtractor(status),
                                   status.place.full_name,
                                   dumps(status._json)]

            self.DB.insertData(tweet_data)
            if self.debug: print("@"+status.user.screen_name+": "+tweet_text)

    def on_error(self,status_code):
        print("Error: "+str(status_code))

    def on_warning(self,notice):
        print("on_warning: "+str(notice))

    def on_disconnect(self, notice):
        print("on_disconnect: "+str(notice))

    def on_timeout(self):
        print("on_timeout")
