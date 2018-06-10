import pickle
from string import ascii_uppercase, ascii_lowercase
from collections import Counter

global LETTERS, letters
LETTERS = list(ascii_uppercase)
letters = list(ascii_lowercase)

def chi_squared_dist(text, prob=None):
    if prob == None:
        with open("english_monograms.pkl", "rb") as f:
            prob = pickle.load(f)

    dist = {}
    freq = Counter(text)
    total = sum([freq[letter] for letter in LETTERS if letter in freq.keys()])
    for letter in LETTERS:
        if letter in freq.keys():
            observed = freq[letter]
        else:
            observed = 0
        expected = prob[letter] * total
        dist[letter] = (observed - expected)**2 / expected
    return dist

def chi_squared(text, prob=None):
    dist = chi_squared_dist(text, prob)
    return sum(dist.values())

def probability_dist(text):
    dist = {}
    freq = Counter(text)
    total = sum([freq[letter] for letter in LETTERS if letter in freq.keys()])
    for letter in LETTERS:
        if letter in freq.keys():
            dist[letter] = freq[letter] / total
        else:
            dist[letter] = 0
    return dist

def index_of_coincidence_dist(text):
    freq = Counter(text)
    total = sum([freq[letter] for letter in LETTERS if letter in freq.keys()])
    dist = {}
    for letter in LETTERS:
        dist[letter] = ((freq[letter] * (freq[letter] - 1))
                        / (total * (total - 1)))
    return dist

def index_of_coincidence(text):
    dist = index_of_coincidence_dist(text)
    return sum(dist.values())
