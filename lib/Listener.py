import tweepy as tw
from .utils import *
from json import dumps

class StListener(tw.StreamListener):
    def __init__(self,DB):
        self.DB=DB
        self.api = tw.api
    #    self.actual_status=None
    # DEBUG
    #def getActual_status(self):
    #    return(self.actual_status)

    def on_warning(self,notice):
        print("\033[1;37;40m on_warning:"+notice)

    def on_disconnect(self,notice):
        print("\033[1;37;40m on_disconnect: "+notice)

    def on_timeout(self):
        print("\033[1;37;40m on_timeout")


    def on_status(self,status):
        """
        This function indicates what to do when a tweet is detected.
        If you want to modify the behaviour of the app when detects a new tweet you should modify it.
        """
    #    self.actual_status=status
        #if status.text[0:2]!="RT":
        if status.place.country_code=="UY":
            if status.truncated==True:

                self.DB.insertData(status.user.screen_name,
                                   status.extended_tweet["full_text"],
                                   timeZoneTransformer(status,"America/Buenos_Aires").ctime(),
                                   status.in_reply_to_screen_name,
                                   hashtagsExtractor(status),
                                   userMentionsExtractor(status),
                                   status.place.full_name,
                                   dumps(status._json))
                print("\033[1;37;40m @"+status.user.screen_name+": "+status.extended_tweet["full_text"])
            else:
                #DEBUG: a.append(status)
                self.DB.insertData(status.user.screen_name,
                                   status.text,
                                   timeZoneTransformer(status,"America/Buenos_Aires").ctime(),
                                   status.in_reply_to_screen_name,
                                   hashtagsExtractor(status),
                                   userMentionsExtractor(status),
                                   status.place.full_name,
                                   dumps(status._json))
                print("\033[1;37;40m @"+status.user.screen_name+": "+status.text)
        #DEBUG: else:
            #print("SE DETECTÓ UN TWIT DE: "+status.place.country_code+" con nombre completo: "+status.place.full_name)

    def on_error(self,status_code):
        print(status_code)
