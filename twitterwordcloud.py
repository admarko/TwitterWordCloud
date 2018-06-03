#  Twitter Word Cloud
#  CMSC 23210: Usable Security & Privacy
#  Problem Set 5, Question 2
#  Created by Alex Markowitz on 5/11/18.

import pprint                           # Data Pretty Printer
import time                             # for time handling
import tweepy                           # twitter parsing
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Twitter API keys
consumer_key = 'Oi9h0A02ZOXMIDzoXsy6sWwHl'
consumer_secret = 'Hh8dBjAP8KTGB2n7gg845WvOXSjm4MlAHntrxbu5DnhTmI8ysi'
access_token = '959207976199483393-0AOwXscYZyRqLvEToTb8xeHqZP69g8F'
access_secret = 'wbcqyeOGWvamz0nO0HaRIzcMs6r8yyEzWvLBV75PxjzKS'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
pp = pprint.PrettyPrinter(indent=4);



# Global Variables
tweets = {}
words = {}

keywords = ['internet security', 'internet privacy', 'technological security', \
            'technological privacy', 'internet rights', 'cybersecurity', \
            'cyberprivacy', 'information security', 'information privacy', \
            'computer security', 'computer privacy']

stop_words = ['the', 'to', 'and', 'of', 'a', 'for', 'is', 'of', 'in', 'on', \
                '', 'with', 'your', 'from', 'that', 'are', 'amp', 'this', 'it' \
                'by', 'as', 'at', 'we', 'an', 'not', 'be']

class StreamListener(StreamListener):
    def on_status(self, status):
        if "RT" not in status.text:
            if status.user.screen_name in tweets:
                tweets[status.user.screen_name].append(status.text)
            else:
                tweets[status.user.screen_name] = [status.text]

    def on_error(self, status):
        print(status)

def parse_tweets():
    global words
    with open("final_output.txt") as f:
        tokens = f.read().split()
    wordarr = ([ token.translate(string.punctuation).lower() for token in tokens ])
    wordarr = [''.join(c for c in s if c not in string.punctuation) for s in wordarr]
    for word in wordarr:
        if word in stop_words:
            wordarr.remove(word)
        elif word in words:
            words[word] += 1
        else:
            words[word] = 1
    words = sorted((v,k) for (k,v) in words.items())
    words.sort(reverse=True)
    pp.pprint(words)


def main():
    myStream = Stream(auth, StreamListener())
    start_time = time.time()
    end_time = start_time + 60*60*8 # 8 hours in seconds
    while (time.time() < end_time):
        try:
            myStream.filter(track=keywords, languages=["en"], async=True)
        except tweepy.error.TweepError:
            print (" Twiiter API error: Too many tweet requests");
        except tweepy.TweepError as e:
            print(" Twitter API error: " + str(e))
    parse_tweets()

main();