#! /usr/bin/python

import json
from markov import Chain, Prefix

twaats = [
    json.load(open('condensed_2017.json')),
    json.load(open('condensed_2016.json')),
    json.load(open('condensed_2015.json')),
    json.load(open('condensed_2014.json')),
    json.load(open('condensed_2013.json')),
    json.load(open('condensed_2012.json')),
    json.load(open('condensed_2011.json')),
    json.load(open('condensed_2010.json')),
    json.load(open('condensed_2009.json')),
]

for length in range(1, 8):
    c = Chain(length)
    for twats in twaats:
        for twat in twats:
            c.rassle(twat['text'])
    filename = 'trumpov_' + str(length) + '.json'
    json.dump(c.chain, open(filename, 'w'), indent=2)
    print('wrote ' + filename)
    topK = ''
    topV = []
    for key, value in c.chain.items():
        if key.count(' ') == length - 1 and len(value) > len(topV):
            topK = key
            topV = value
    print('favorite key at length ' + str(length) + ': "' + topK + '", ' + str(len(topV)))

print('all chained up')
