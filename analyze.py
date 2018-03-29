import re
from textblob import TextBlob
from collections import Counter # for counting locations
import json
import csv

global userInfo, userLocations, userTweets, sentiments

def findUserLocation():
    '''Create a dict of User locations and count how many times they appear'''
    global userInfo, userLocations
    with open('python.json') as fp:
        content = fp.readlines()
    
    for item in content:
        t = json.loads(item)
        userInfo.append(t)
        userLocations.append(t["user"]["location"])
        


''' https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/ '''
def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

''' https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/ '''
def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

def get_text_tweets():
    ''' Extract the text out of the Tweet metadata, add to global var userTweets '''
    global userInfo
    global userTweets
    for user in userInfo:
        userTweets.append(user["text"])
        #print(user["text"])
    

def printSentiments():
    ''' print out a sampling of user sentiments in each category '''
    global neutralsentiment, psentiment, nsentiment
    print("10 neutral tweets: ")
    for i in range(10):
        print(neutralsentiment[i])
        print('\n')

    print("10 positive tweets: ")
    for i in range(10):
        print(psentiment[i])
        print('\n')

    print("10 negative tweets: ")
    for i in range(10):
        print(nsentiment[i])
        print('\n')


def analyzeSentiment():
    ''' Categorize textual sentiment using textblob, categorize into lists of 
        positive (psentiment), negative (nsentiment) and neutral (neutralsentiment) 
    '''
    global userTweets
    global sentiments
    global psentiment, nsentiment, neutralsentiment
    for text in userTweets:
        sentiments[text] = get_tweet_sentiment(text)
        if sentiments[text] == 'positive':
            psentiment.append(text)
        elif sentiments[text] == 'negative':
            nsentiment.append(text)
        elif sentiments[text] == 'neutral':
            neutralsentiment.append(text)
    

if __name__ == "__main__":
    global userInfo, userLocations, userTweets, sentiments
    global psentiment, nsentiment, neutralsentiment
    
    userInfo=[]
    userLocations=[]
    userTweets=[]
    sentiments = {}

    psentiment = []
    nsentiment =[]
    neutralsentiment =[]

    findUserLocation()
    

    # obtain sentiment analysis
    get_text_tweets()
    analyzeSentiment()

    printSentiments()
    

    #print(Counter(userLocations))
  
    newd = Counter(userLocations)
    w = csv.writer(open("newOutput.csv", "w"))

    for val in userLocations:
        if val != None:
            w.writerow([val.encode('utf-8').strip()])
        else:
            w.writerow(['None'])