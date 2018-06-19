from collections import Counter

def ngrams(n, text, grams={}):
    for i in range(len(text)-n):
        gram = text[i:i+n]
        if gram in grams.keys():
            grams[gram] += 1
        else:
            grams[gram] = 1
    return grams

def most_common(n, grams):
    freq = Counter(grams.values())
    values = set(grams.values())
    output = []
    for i in range(n):
        value = max(values)
        values.remove(value)
        output.extend([gram for gram in grams.keys() if grams[gram] == value])
    return output

if __name__ == "__main__":
    print("This module is intended to be imported and should not be run directly.")
