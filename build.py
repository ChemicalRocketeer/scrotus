#! /usr/bin/python

import json
import os
from markov import Chain, Prefix

twaats = [
    json.load(open('tweets/condensed_2017.json')),
    json.load(open('tweets/condensed_2016.json')),
    json.load(open('tweets/condensed_2015.json')),
    json.load(open('tweets/condensed_2014.json')),
    json.load(open('tweets/condensed_2013.json')),
    json.load(open('tweets/condensed_2012.json')),
    json.load(open('tweets/condensed_2011.json')),
    json.load(open('tweets/condensed_2010.json')),
    json.load(open('tweets/condensed_2009.json')),
]

for length in range(1, 6):
    c = Chain(size=length)
    for twats in twaats:
        for twat in twats:
            if twat['is_retweet'] or twat['text'][0:2] == '"@':
                pass
            elif twat['source'] == "Twitter for Android":
                c.rassle(u''+twat['text'])
    filename = 'chains/trumpov_' + str(length) + '.json'
    os.makedirs('chains', exist_ok=True)
    c.save(filename)
    print('wrote ' + filename)
    topK = ''
    topV = []
    for key, value in c.chain.items():
        if key.count(' ') == length - 1 and len(value) > len(topV):
            topK = key
            topV = value
    print('favorite key at length ' + str(length) + ': "' + topK + '", ' + str(len(topV)))

print('all chained up')
