def hash_function(text):
    return sum(ord(character) for character in text)


if __name__ == '__main__':
    print(hash_function("Lorem"))
