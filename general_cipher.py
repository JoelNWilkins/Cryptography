from matrix import Matrix
from text_tools import convert_text
import corpus
import score
from string import ascii_uppercase
from matplotlib import pyplot as plt
import time

class General_Cipher:
    def __init__(self, *args, **kwargs):
        if "n" in kwargs.keys():
            self.n = kwargs.pop("n")
            self.A = Matrix(random=True, shape=(self.n, self.n), m=26)
            self.B = Matrix(random=True, shape=(1, self.n), m=26)
        else:
            self.A = Matrix(args[0])
            self.B = Matrix(args[1])

        self.letters = list(ascii_uppercase)

    def encode(self, text):
        text = convert_text(text)
        output = ""
        for i in range(len(text)//self.n):
            P = Matrix([self.letters.index(text[self.n*i+x])
                        for x in range(self.n)],
                       shape=(1, self.n))
            C = ((self.A * P) + self.B) % 26
            output += "".join([self.letters[x] for x in C.column(0)])
        return output

    def decode(self, text):
        text = convert_text(text)
        output = ""
        for i in range(len(text)//self.n):
            C = Matrix([self.letters.index(text[self.n*i+x])
                        for x in range(self.n)],
                       shape=(1, self.n))
            P = (self.A.mod_inv(26) * (C - self.B)) % 26
            output += "".join([self.letters[x] for x in P.column(0)])
        return output

if __name__ == "__main__":
    c = corpus.Corpus("C:/Users/Joel/Documents/EMS/EMC/Cryptography/Books/files/")
    f = c.random()
    text = c.open(f)[:200]
    plaintext = convert_text(text)
    cipher = General_Cipher(n=5)
    start = time.time()
    ciphertext = cipher.encode(text)
    print(time.time() - start)
    print(ciphertext[:79])
    start = time.time()
    decoded = cipher.decode(ciphertext)
    print(time.time() - start)
    print(decoded[:79])

##    print(plaintext[:79])
##    print(ciphertext[:79])
##    print(score.index_of_coincidence(plaintext))
##    print(score.index_of_coincidence(ciphertext))
##    print(score.chi_squared(plaintext))
##    print(score.chi_squared(ciphertext))
    p = score.probability_dist(plaintext)
    c = score.probability_dist(ciphertext)

    width = 0.35
    
    x1 = []
    x2 = []
    y1 = []
    y2 = []
    for count, letter in enumerate(cipher.letters):
        x1.append(count - width/2)
        x2.append(count + width/2)
        y1.append(p[letter])
        y2.append(c[letter])

    plt.bar(x1, y1, width=width, color="w", edgecolor="k", hatch="////",
            label="Plaintext")
    plt.bar(x2, y2, width=width, color="w", edgecolor="k", hatch="\\\\",
            label="Ciphertext")

    plt.xlabel("Letter")
    plt.ylabel("Frequency")
    plt.title("Frequency Analysis of a General Cipher")

    plt.xticks(list(range(26)), cipher.letters)
    plt.yticks([])

    plt.legend()

    plt.show()
