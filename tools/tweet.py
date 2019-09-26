# This Tool receives a file f with one tweet ID on each line.
from twython import Twython
import time

APP_KEY = "6Chp62aRA6ivZxvadDgoldlD5"
APP_SECRET = "7tRqt6Z3FFgLeu2T7bucIRku6ti80H3BZh0UXmDj9YQdJUoXwO"
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

f = open("pakistan2013", 'r')
writer = open("2013-pakistan-date.csv", 'w+')
writerDetails = open("2013-pakistan-details.csv", 'w+')

i=0
tweetCount = 0
calls = 0
successCount = 0
IDs = ""
for line in f:
    line=line.strip()
    tweetID=line
    # tweetID = line.split(';')[0]
    # tweetID = tweetID[1:-1]
    i+=1
    if i == 1 or i == 100:
        IDs+=tweetID
        if i == 100:
            callsLimit = twitter.get_application_rate_limit_status(resources="statuses")
            remainingCalls = callsLimit["resources"]["statuses"]["/statuses/lookup"]["remaining"]
            if(remainingCalls == 0 or calls == 170):
                time.sleep(60*15)
                twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
                calls=0

            tweets = twitter.lookup_status(id=IDs) # only gets the tweets that exists or can be viewed by the given APP_KEY
            successCount += len(tweets)
            calls += 1

            for tweet in tweets:
                writer.write("%s;%s\n"%(tweet["id"], tweet['created_at']))
                writerDetails.write("%s;%s;%s;"%(tweet["id"], tweet['created_at'], tweet["text"]))
                for hashtag in tweet["entities"]["hashtags"]:
                    writerDetails.write("%s, "%hashtag["text"])
                writerDetails.write("\n")
            i=0
            IDs=""
            tweetCount+=100
            print("%s/65534"%tweetCount)
    else:
        IDs+=","+tweetID


print("found information of %s ids"%(successCount))
f.close()
writer.close()
writerDetails.close()