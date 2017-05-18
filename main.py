#! /usr/bin/python

import random
import json

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

# a prefix is an array of one or more words
# the markov chain is keyed by space separated prefixes
class Prefix():
    def __init__(self, size):
        self.size = size
        self.prfx = []

    def __str__(self):
        return self.key()
        
    def shift(self, word):
        index = 1 if len(self.prfx) >= self.size else 0
        self.prfx = self.prfx[index:]
        self.prfx.append(word)
        
    def key(self):
        return ' '.join(self.prfx)


class Chain():
    def __init__(self, size, chain=None):
        self.size = size
        self.chain = {} if chain is None else chain
        
    def __str__(self):
        strangle = str(self.size)
        for key, value in self.chain.items():
            strangle += '\n' + key + ': ' + str(value)
        return strangle

    def rassle(self, twats):
        prefix = Prefix(self.size)
        for twat in twats.split(' '):
            if (twat != ' ' and twat != ''):
                key = prefix.key()
                self.chain.setdefault(key, []).append(twat)
                prefix.shift(twat)
            

for length in range(1, 11):
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
