class Word_check:
    def __init__(self):
        self.lexicon = open('lexicon.txt', encoding="utf8").read().splitlines()

    def check_for_valid_word(self, word):
        for words in self.lexicon:
            if word == words:
                return True
        return False

