from string import ascii_uppercase

def convert_text(text):
    letters = list(ascii_uppercase)
    output = ""
    text.replace("\n", "")
    for char in text.upper():
        if char in letters:
            output += char
    return output

if __name__ == "__main__":
    print("This module is intended to be imported and should not be run directly.")
