# twitter-sniffer
This little app gets tweets in real time from a specific geographical location and saves them in a SQLite database.

The SQLite database created saves one file by day, detailing the username, the text of the tweet, who is answering, and a lot of other things you can check if you run it.

But before you can try this, you need to get a twitter developer account and credentials. See above for more information about this. 

The default location of the tweets is the country Uruguay. To get tweets from another location, you need to change one parameter in the main file. More information above, too.


Creating Twitter Credentials
----------------------------

To get a Twitter Developer account you need to keep the following steps:

1-[Apply for a developer account](https://developer.twitter.com/en/apply-for-access)

2-Create a Project and a developer App in the [developer portal](https://developer.twitter.com/en/portal/dashboard).

3-After create, you can check your credentials at the section "Keys and Tokens" of your app's settings.

4-In that section you have two groups of tokens: "Consumer keys" and "Authentication Tokens"
	4.1-Generate and save the "API Key", "API Key Secret" from Consumer keys in a file, putting each one in a line.
	4.2-In the Authentication Tokens section, generate the Access Token and Access Token Secret. Save them in the same file separed in lines.
	4.3-The final result must be a auth.key file in the working directory (the one from which main.py is being executed) with 4 lines: in the first one is the API Key, the second has the API Key Secret, the third has the Access Token and the last one has the Access Token Secret.

5-If the execution prints an 401 error, the auth.key file has some errors. Check if the copied keys are right and check there is not spaces or line break in the file (all that things will be detected and can be the root of the error).

This section was created with information from the [Twitter Documentacion](https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/quick-start).

Filtering tweet locations in real time
--------------------------------------

Twitter API uses GEOJson to recognize the geo-located data. If we want to filter tweets by location, we need to give twitter a geographical area GEOJson-formatted. 

For that, we recommend to use the page [geojson.io](geojson.io) page. There, you select the square(*) and create an area in the map. In the right side of the page you should see a code with a list of numerical elements. Those elements are the points that define the square. 

If you look slowly, you can see there is repeated elements. If nothing goes wrong, there should be only 4 unique elements showed. Copy and paste them in the definition of variable country_location in the main.py file, being carefull of mantain the original format.

After that, don't forget to read the message left behind that line and change the country code from "UY" to your desired country. If you don't change this line probably can't detect anything!


