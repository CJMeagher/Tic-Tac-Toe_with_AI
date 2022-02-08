def translate(**kwargs):
    for word in words:
        print(word, ":", words[word])


words = {
    "mother": "madre",
    "father": "padre",
    "grandmother": "abuela",
    "grandfather": "abuelo",
}

translate(**words)
