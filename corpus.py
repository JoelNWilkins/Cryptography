import os
import random

class Corpus:
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.files = os.listdir(path)

    def __iter__(self, *args, **kwargs):
        self.count = 0
        return self

    def __next__(self, *args, **kwargs):
        self.count += 1
        if self.count <= len(self.files):
            return self.files[self.count-1]
        else:
            raise StopIteration

    def open(self, filename):
        try:
            with open(self.path+filename, "r") as f:
                text = f.read()
        except UnicodeDecodeError:
            print("Error - {}".format(filename))
            text = ""
        return text

    def random(self, *args, **kwargs):
        return random.choice(self.files)

if __name__ == "__main__":
    print("This module is intended to be imported and should not be run directly.")
