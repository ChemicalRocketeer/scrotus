#! /usr/bin/python

import random

twats = [
    "I have been asking Director Comey & others, from the beginning of my administration, to find the LEAKERS in the intelligence community.....",
    "...to terrorism and airline flight safety. Humanitarian reasons, plus I want Russia to greatly step up their fight against ISIS & terrorism.",
    "As President I wanted to share with Russia (at an openly scheduled W.H. meeting) which I have the absolute right to do, facts pertaining....",
    "China just agreed that the U.S. will be allowed to sell beef, and other major products, into China once again. This is REAL news!",
    "As families prepare for summer vacations in our National Parks - Democrats threaten to close them and shut down the government. Terrible!"
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
    def __init__(self, size):
        self.size = size
        self.chain = {}
        
    def __str__(self):
        strangle = str(self.size)
        for key, value in self.chain.items():
            strangle += '\n' + key + ': ' + str(value)
        return strangle

    def rassle(self, twats):
        prefix = Prefix(self.size)
        for twat in twats.split(' '):
            key = prefix.key()
            self.chain.setdefault(key, []).append(twat)
            prefix.shift(twat)

c = Chain(2)
c.rassle(twats[0])
c.rassle(twats[1])
c.rassle(twats[2])
c.rassle(twats[3])
print(c)
