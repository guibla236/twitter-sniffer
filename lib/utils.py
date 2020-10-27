from dateutil.tz import *

def userMentionsExtractor(status):
    """Extract particular tweet's user mentions.
    Parameters:
        tweepy.models
    Returns:
        List:User_mentions
    """
    user_mentions=None
    if len(status.entities["user_mentions"]) != 0:
        user_mentions="["
        for i in range(0,len(status.entities["user_mentions"])):
            user_mentions+=status.entities["user_mentions"][i]["screen_name"]+","
        user_mentions=user_mentions[0:-1]
        user_mentions+="]"
    return(user_mentions)

def hashtagsExtractor(status):
    """Extract particular tweet's hashtags.
    Parameters:
        tweepy.models
    Returns:
        List:hashtags
    """
    hashtags=None
    if len(status.entities["hashtags"]) != 0:
        hashtags="["
        for i in range(0,len(status.entities["hashtags"])):
            hashtags+=status.entities["hashtags"][i]["text"]+","
        hashtags=hashtags[0:-1]
        hashtags+="]"
    return(hashtags)

def timeZoneTransformer(status,localTimeZone):
    """Transform tweet's time to the specified time zone string, ie: "America/Montevideo"
    If you don't know the local time zone string, please read more about dateutil's tz functions.
    Parameters:
        tweepy.models, string
    Returns:
        datetime
    """
    time=status.created_at
    to_tz=gettz(localTimeZone)
    time=time.replace(tzinfo=gettz("UTC"))
    return(time.astimezone(to_tz))
    
def keyScanner(path):
    """Reads a file with Twitter keys used to access to a Twitter stream (remember
    you need a developer account to get this).
    The file must contain four lines:
        -Consumer Key
        -Consumer Secret
        -Access token
        -Access secret.

    The keys should be separated into lines and don't need any quotes.
    If there is a space in any part of the file, Twitter would reject the
    connection due to incorrect keyword.
    """

    handler=open(path)
    lines=handler.readlines()
    for i in range(0,len(lines)):
        #The file comes with "\n" between lines. This for erase that.
        lines[i]=lines[i][:-1]

    return(lines)
