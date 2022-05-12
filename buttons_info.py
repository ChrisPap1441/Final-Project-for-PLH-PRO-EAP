import sys
sys.dont_write_bytecode = True #gia na min dimiourgite se kathe ektelesi o fakelos pycache
import tkinter as tk
from PIL import ImageTk , Image


class Info(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scrabble")
        self.geometry("1520x980")
        self.configure(background="lightgrey")

        #-----------Scrabble logo------------#
        self.logo_image = Image.open("Scrabble.png")
        self.resized_logo = self.logo_image.resize((500, 225), Image.Resampling.LANCZOS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo = tk.Label(self, background= "lightgrey", image = self.new_logo, width= 500, height = 225)
        self.logo.place(x= 480, y = 150)
        #---------------Info-----------------#
        self.info_title = tk.Label(self, background= "lightgrey", width=100, borderwidth = 2, relief = "solid",
             text = "ΤΑ ΚΟΥΜΠΙΑ ΤΟΥ ΠΑΙΧΝΙΔΙΟΥ\n\nΈλεγχος λέξης:\nΜε αυτό το κουμπί ο παίκτης ελέγχει την λέξη που έχει δημιουργήσει, αφού πρώτα εισάγει όλα τα γράμματα στο ταμπλό. \nΣε περίπτωση που η λέξη είναι έγκυρη ενημερώνεται το σκορ του παίχτη και τελειώνει ο γύρος. \nΣε περίπτωση που η λέξη δεν είναι έγκυρη, τότε επιστρέφονται τα γράμματα πίσω στον παίκτη.\n\nΠέταξε ένα γράμμα:\n Με αυτό το κουμπί ο παίκτης μπορεί να διώξει ένα γράμμα από το χέρι του. \nΕπιλέγει πρώτα το γράμμα που θέλει να διώξει με το ποντίκι, μόλις το γράμμα αλλάξει χρώμα από άσπρο σε κίτρινο, \nαυτό σημαίνει πως είναι επιλεγμένο, ύστερα ο παίκτης πατάει το κουμπί και το γράμμα διώχνεται.\n\nΑναίρεση κίνησης:\nΜε αυτό το κουμπί ο παίκτης παίρνει πίσω το πιο πρόσφατο γράμμα που έχει εισάγει, πατώντας συνεχόμενα το κουμπί, \nμπορεί να πάρει πίσω όλα τα γράμματα που έχει εισάγει στον τρέχοντα γύρο.\n\nΠάσο:\nΜε αυτό το κουμπί ο παίκτης επιλέγει να μην αξιοποιήσει τον γύρο του. \nΣε περίπτωση που έχει εισάγει κάποια γράμματα στο ταμπλό στον τρέχοντα γύρο, του επιστρέφονται.\n\nΤερματισμός παιχνιδιού:\nΜε αυτο το κουμπί ο παίκτης τερματίζει το τρέχον παιχνίδι και επιστρέφει στην αρχική σελίδα.\n\nΚλείσιμο της εφαρμογής:\nΜε αυτό το κουμπί ο παίκτης τερματίζει την εφαρμογή.", font= 55)
        self.info_title.place(x = 270, y = 400)
        
        

        def previous_page():
            self.destroy()
            from intro_page import IntroPage
            intro = IntroPage()
            intro.mainloop()

        #----------Buttons--------------#
        previous_page_button = tk.Button(self, text="Αρχική Σελίδα", command=previous_page)
        previous_page_button.place(x = 680, y = 900)