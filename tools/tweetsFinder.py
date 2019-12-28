# WIP: Add a new tool to search for tweets given a bunch of keywords or hashtags, 
# at the moment it can obtain at most 1800 tweets, should check for the rate limit on twitter API
import time
from twython import Twython

APP_KEY = "6Chp62aRA6ivZxvadDgoldlD5"
APP_SECRET = "7tRqt6Z3FFgLeu2T7bucIRku6ti80H3BZh0UXmDj9YQdJUoXwO"
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

writer = open("../captured/chileSearch3.csv", 'w+')
writerDetails = open("../captured/chileSearch3-details.csv", 'w+')

res = twitter.search(q='#terremoto #chile #erremoto #sismo #', result_type='mixed', count=100, lang='es', include_entities='true')

minID = 9999999999999999999999
tweetsAmount = 4000
foundTweets = 0

while True:
# for i in range(18):
    foundTweets += len(res["statuses"])
    # print(i, "size:", len(res["statuses"]))
    for tweet in res["statuses"]:
        if int(tweet["id"]) < minID:
            minID = int(tweet["id"])
        writer.write("%s;%s\n"%(tweet["id"], tweet['created_at']))

        writerDetails.write("%s;%s;%s;"%(tweet["id"], tweet['created_at'], tweet["text"].strip().replace('\n', ' ')))
        for hashtag in tweet["entities"]["hashtags"]:
            writerDetails.write("%s, "%hashtag["text"].strip().replace('\n', ' '))
        writerDetails.write("\n")

        print(tweet["id"])
    res = twitter.search(q='#terremoto, Chile, Terremoto, sismo', count=100, max_id=minID, lang='es', include_entities='true')

    if foundTweets >= tweetsAmount:
        break
    print("Sleeping 15 mins")
    time.sleep(60*15)
    print("Awakening")
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
writer.close()
writerDetails.close()