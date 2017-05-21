#! /usr/bin/python

import random
import re
import json

class Prefix():
    def __init__(self, size=1, prefix=None):
        if prefix is None:
            self.size = size
            self.prfx = []
        else:
            self.size = prefix.size
            self.prfx = prefix.prfx[:]

    def __str__(self):
        return self.key()

    def shift(self, word):
        index = 1 if len(self.prfx) >= self.size else 0
        self.prfx = self.prfx[index:]
        self.prfx.append(word)

    def key(self):
        return ' '.join(self.prfx)

# these have spaces, so they cannot end up in the chain organically.
END_WORD = '< END >'
L_QUOTE = '< LQ >'
R_QUOTE = '< RQ >'
# punctuation is removed from words, so if it's there it means it's a "punctuation word".
RE_PUNCT = re.compile(r'[;!()]|[:.,](?=\s|$)')
RE_L_QUOTE = re.compile(r'(")\S')
RE_R_QUOTE = re.compile(r'\S(")')
RE_HTTP = re.compile(r'https?://\S+\.\S+', re.IGNORECASE)

# what = 'whatever...'
# punk = RE_PUNCT.search(what)
# print(punk)
# print(what[:punk.start()])
# print(what[punk.start():punk.end()])
# print(what[punk.end():])
# print(what[:punk.start()] + ' ' + what[punk.start():punk.end()] + ' ' + what[punk.end():])

class Chain():
    def __init__(self, source=None, size=2):
        if source:
            self.size = source['size']
            self.chain = source['chain']
        else:
            self.size = size
            self.chain = {}

    def __str__(self):
        return json.dumps(self.raw(), indent=2)

    def raw(self):
        return { 'size': self.size, 'chain': self.chain }

    def save(self, filename, pretty=False):
        indent = 2 if pretty else 0
        json.dump(self.raw(), open(filename, 'w'), indent=indent)



    # rassles the tweets to build a markov chain
    def rassle(self, twat):
        prefix = Prefix(self.size)

        # space separate the punctuation
        def split_punks(s):
            punk = RE_PUNCT.search(s)
            if punk:
                return s[:punk.start()] + ' ' + s[punk.start():punk.end()] + ' ' + split_punks(s[punk.end():])
            else:
                return s

        twat = split_punks(twat)
        for word in twat.split(' '):
            if (word != ' ' and word != ''):
                key = prefix.key()
                self.chain.setdefault(key, []).append(word)
                prefix.shift(word)
        self.chain[key].append(END_WORD)

    # generates a tweet from the markov chain
    def gen(self, words):
        tweet = []
        prefix = Prefix(self.size)
        for i in range(0, words):
            key = prefix.key()
            if key not in self.chain:
                break
            word = random.choice(self.chain[key])
            if word == END_WORD:
                break
            tweet.append(word)
            prefix.shift(word)
        # join the words together, eliminating spaces in front of punctuation
        if len(tweet) == 0:
            return ''
        stweet = tweet[0]
        nospace = False
        for word in tweet[1:]:
            if nospace:
                stweet += word
                nospace = False
            elif word == '(':
                stweet += ' ('
                nospace = True
            elif RE_PUNCT.match(word):
                stweet += word
            else:
                stweet += ' ' + word
        # closeparens = 0
        # openparens = 0
        # for char in stweet:
        #     if char == '(':
        #         closeparens = closeparens + 1
        #     elif char == ')':
        #         if closeparens <= 0:
        #             openparens += 1
        #         else:
        #             closeparens = closeparens - 1
        # stweet = stweet + ')' * closeparens
        # stweet = '(' * openparens + stweet
        return stweet

if __name__ == "__main__":
    chain = Chain(json.load(open('chains/trumpov_2.json')))
    for i in range(0, 50):
        json.dump([chain.gen(1000) for i  in range(0, 50)], open('testing.json', 'w'), indent=2)
