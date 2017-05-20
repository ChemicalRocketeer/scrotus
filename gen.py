#! /usr/bin/python

import json
from markov import Chain, Prefix

chain = Chain(2, json.load(open('chains/trumpov_2.json')))
print(chain.gen())
