#! /usr/bin/python

import random

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

    # rassles the tweets to build a markov chain
    def rassle(self, twat):
        prefix = Prefix(self.size)
        for word in twat.split(' '):
            if (word != ' ' and word != ''):
                key = prefix.key()
                self.chain.setdefault(key, []).append(word)
                prefix.shift(word)

    # generates a tweet from the markov chain
    def gen(self, words):
        tweet = []
        prefix = Prefix(self.size)
        for i in range(0, words):
            key = prefix.key()
            if not key in self.chain:
                break
            word = random.choice(self.chain[key])
            tweet.append(word)
            prefix.shift(word)
        return ' '.join(tweet)

if __name__ == "__main__":
    import json
    chain = Chain(2, json.load(open('trumpov_2.json')))
    print(chain.gen(random.choice(range(4, 13))))
