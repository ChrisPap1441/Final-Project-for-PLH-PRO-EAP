class Word_check:
    def __init__(self):
        #Εισάγουμε τις λέξεις που περιέχει το λεξικό από το αρχείο κειμένου
        self.lexicon = open('lexicon.txt', encoding="utf8").read().splitlines()

    #Μέθοδος για τον έλεγχο της εγκυρότητας της λέξης που έχει εισάγει ο χρήστης
    def check_for_valid_word(self, word):
        for words in self.lexicon:
            if word == words:
                return True
        return False