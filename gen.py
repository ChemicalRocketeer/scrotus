#! /usr/bin/python

import json
import tweepy
import html
from markov import Chain, Prefix

# secret.json is: {
#   twitter: {
#     key, keysecret, token, tokensecret
#   }
# }
secret = json.load(open('secret.json'))['twitter']

auth = tweepy.OAuthHandler(secret['key'], secret['keysecret'])
auth.set_access_token(secret['token'], secret['tokensecret'])

twitter = tweepy.API(auth)

dedupe = json.load(open('dedupe.json')) or {}

try:
    chain = Chain(json.load(open('chains/trumpov_2.json')))
    post = None
    i = 0
    while (not post) or (post in dedupe):
        post = chain.gen(1000)
        i += 1
        if i >= 20:
            raise Exception('too many duplicates')
    twitter.update_status(html.unescape(post))
    dedupe[post] = True
    json.dump(dedupe, open('dedupe.json', 'w'))
    print('success')
except Exception as ex:
    print('failed')
    print(ex)
