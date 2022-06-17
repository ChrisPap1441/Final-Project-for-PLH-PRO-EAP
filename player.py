class Player:
    def __init__(self):
        #Μεταβλητή με τους συνολικούς πόντους του χρήστη
        self.highscore = 0
        #Λίστα που περιέχει τους πόντους κάθε λέξης που δημιούργησε σε 1 γύρο ο χρήστης
        self.potential_points = []
        #Μεταβλητή για τον υπολογισμό των πόντων της λέξης στην τωρινή στιγμή 
        self.current_word_score = 0
        #Τα γράμματα που έχει στο χέρι του ο χρήστης 
        self.hands_letters = []
        #Τα γράμματα που έχει τοποθετήσει στο ταμπλό ο χρήστης 
        self.used_letters = []
        #Τα γράμματα που περιέχει η λέξη του χρήστη 
        self.word_letters = []
        #Λίστα που περιέχει τις συντεταγμένες για την αναίρεση κίνησης 
        self.coords_cancel = []
        #Λίστα που περιέχει τις συντεταγμένες για τα γράμματα ώστε σε περίπτωση έγκυρης λέξης
        # να θεωρούνται ύστερα τα γράμματα στα κελιά αυτά πως έχουν εισαχθεί από προηγούμενο γύρο,
        #  όταν βάσει κανόνων ο χρήστης θα πρέπει να χρησιμοποιήσει ένα από αυτά σε επόμενους γύρους
        self.previous_coords = [] 
        #Μεταβλητή για την λέξη που δημιουργήθηκε
        self.word = None
        #Λίστα για τον έλεγχο εγκυρότητας κάθε λέξης που μπορεί να έχει δημιουργηθεί σε ένα γύρο
        self.words_to_check = []
        #Λίστα με τις τιμές από τις συντεταγμένες του άξονα x
        self.x_coords = []
        #Λίστα με τις τιμές από τις συντεταγμένες του άξονα x για δευτερεύουσες λέξεις
        self.multi_words_x_coords = []
        #Λίστα με τις τιμές από τις συντεταγμένες του άξονα y
        self.y_coords = []
        #Λίστα με τις τιμές από τις συντεταγμένες του άξονα y για δευτερεύουσες λέξεις
        self.multi_words_y_coords = []
        #Μεταβλητή που έχει τιμή True αν η λέξη του χρήστη είναι οριζόντια
        self.x_axis = True
        #Μεταβλητή που έχει τιμή True αν η λέξη του χρήστη είναι κάθετη
        self.y_axis = True
        #Μεταβλητή που περιέχει την τιμή για τις συντεταγμένες που ξεκινάει η λέξη
        self.word_start = None
        #Μεταβλητή που περιέχει την τιμή για τις συντεταγμένες που τελειώνει η λέξη
        self.word_finish = None
        #Μεταβλητή που περιέχει την τιμή των συντεταγμένων του άξονα της λέξης
        self.word_axis = None
        #Μεταβλητή για αμυντικό προγραμματισμό που ελέγχει αν έχει εισάγει σε σωστή σειρά τα γράμματά του ο χρήστης
        self.first_check = None
        #Μεταβλητή για αμυντικό προγραμματισμό που ελέγχει αν ο χρήστης έχει χρησιμοποιήσει για την δημιουργία της λέξης του 
        #ένα γράμμα από το ταμπλό που είχε τοποθετηθεί από προηγούμενο γύρο
        self.second_check = None
        #Μεταβλητή για αμυντικό προγραμματισμό που ελέγχει αν οι λέξεις του χρήστη ήταν έγκυρες
        self.words_ready = True
        #Μεταβλητή μέτρησης των επιτρεπόμενων γραμμάτων προς αντικατάσταση
        self.letter_switch = 0

    #Γίνεται ταξίνόμηση των λιστών με τις συντεταγμένες
    #μέσω της χρήσης της selection sort
    def prepare_coords(self):
        #Ταξινόμηση των στοιχείων της λίστας για τον άξονα x
        for coord_x in range(len(self.x_coords)):
            min_coord_x = coord_x
            for j in range(coord_x + 1, len(self.x_coords)):
                if self.x_coords[min_coord_x] > self.x_coords[j]:
                    min_coord_x = j
            temp = self.x_coords[coord_x]
            self.x_coords[coord_x] = self.x_coords[min_coord_x]
            self.x_coords[min_coord_x] = temp

        #Ταξινόμηση των στοιχείων της λίστας για τον άξονα y
        for coord_y in range(len(self.y_coords)):
            min_coord_y = coord_y
            for j in range(coord_y + 1, len(self.y_coords)):
                if self.y_coords[min_coord_y] > self.y_coords[j]:
                    min_coord_y = j
            temp = self.y_coords[coord_y]   
            self.y_coords[coord_y] = self.y_coords[min_coord_y]
            self.y_coords[min_coord_y] = temp

    #Μέθοδος στην οποία επιβεβαιώνω τον άξονα στον οποίο βρίσκεται η λέξη
    #Κάνω προσπέλαση τις λίστες και η λίστα που οι τιμές της είναι όλες διαφορετικές
    #Τότε αφήνω την μεταβλητή του άξονα να παραμείνει True αλλιώς γίνεται False και
    #κάνω break την επανάληψη.
    #Στην περίπτωση που ο χρήστης εισάγει με λάθος τρόπο τα γράμματά του
    #τότε και οι δύο άξονες γίνονται False.
    def validate_coords(self):
        for coord_x in range(1, len(self.x_coords)):
            if self.x_coords[coord_x - 1] != self.x_coords[coord_x]:
                self.x_axis = False
                break

        for coord_y in range(1, len(self.y_coords)):
            if self.y_coords[coord_y - 1] != self.y_coords[coord_y]:
                self.y_axis = False
                break
    
    #Μέθοδος στην οποία εντοπίζω τον άξονα στον οποίο βρίσκεται η λέξη,
    #ώστε να βάλω τις ανάλογες τιμές στις μεταβλητές που θα χρησιμοποιήσω στην προσπέλαση
    #λιστών και λεξικών για την δημιουργία των λέξεων.
    #Στην περίπτωση που έχει κάνει λάθος ο χρήστης, η μεταβλητή για τον αμυντικό έλεγχο(first_check)
    #θα πάρει την τιμή False.
    def process_coords(self):
        #Στην περίπτωση που η λέξη είναι κάθετη
        if self.y_axis == True and self.x_axis == False:
            self.word_start = self.x_coords[0] #Σε ποιο σημείο του άξονα x ξεκινάει η λέξη
            self.word_finish = self.x_coords[len(self.x_coords)-1] #Σε ποιο σημείο του άξονα x τελειώνει η λέξη
            self.word_axis = self.y_coords[0] #Σε ποιο σημείο του άξονα y βρίσκεται η λέξη
            self.first_check = True #Μεταβλητή αμυντικού προγραμματισμού
        #Στην περίπτωση που η λέξη είναι οριζόντια
        elif self.x_axis == True and self.y_axis == False:
            self.word_start = self.y_coords[0] #Σε ποιο σημείο του άξονα y ξεκινάει η λέξη
            self.word_finish = self.y_coords[len(self.y_coords)-1] #Σε ποιο σημείο του άξονα y τελειώνει η λέξη
            self.word_axis = self.x_coords[0] #Σε ποιο σημείο του άξονα x βρίσκεται η λέξη
            self.first_check = True #Μεταβλητή αμυντικού προγραμματισμού
        #Στην περίπτωση που ο χρήστης έχει εισάγει με λάθος τρόπο τα γράμματα του
        else:
            self.first_check = False #Μεταβλητή αμυντικού προγραμματισμού
        
    #Μέθοδος για την προσθήκη των πόντων που μάζεψε στον τρέχοντα γύρο
    #ο χρήστης, στη μεταβλητή highscore που περιέχει τους συνολικούς του πόντους
    def add_points(self):
        for i in self.potential_points:
            self.highscore += i

    #Μέθοδος για την επαναφορά των μεταβλητών στην αρχική τους κατάσταση
    def reset_values(self):
        self.potential_points.clear()
        self.current_word_score = 0
        self.used_letters.clear()
        self.word_letters.clear()
        self.coords_cancel.clear()
        self.previous_coords.clear()
        self.word = None
        self.words_to_check.clear()
        self.x_coords.clear()
        self.multi_words_x_coords.clear()
        self.y_coords.clear()
        self.multi_words_y_coords.clear()
        self.x_axis = True
        self.y_axis = True
        self.word_start = None
        self.word_finish = None
        self.word_axis = None
        self.first_check = None
        self.second_check = None
        self.words_ready = True
    