import sys
sys.dont_write_bytecode = True #gia na min dimiourgite se kathe ektelesi o fakelos pycache
import tkinter as tk
from PIL import ImageTk , Image


class Info(tk.Tk):
    def __init__(self):
        super().__init__()
        #-------------Ρυθμίσεις παραθύρου---------#
        self.title("Scrabble")
        self.geometry("1520x980")
        self.configure(background="lightgrey")

        #-----------Λογότυπο Scrabble------------#
        #Για να μπορέσουμε να επεξεργαστούμε το μέγεθος της εικόνας αξιοποιούμε το Image και το ImageTk
        #της βιβλιοθήκης PIL
        self.logo_image = Image.open("Scrabble.png")
        self.resized_logo = self.logo_image.resize((500, 225), Image.Resampling.LANCZOS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo = tk.Label(self, background= "lightgrey", image = self.new_logo, width= 500, height = 225)
        self.logo.place(x= 480, y = 100)
        
        #---------------Info-----------------#
        #Κείμενο με τις πληροφορίες για την λειτουργία των κουμπιών
        self.info_text = open('button_info.txt', encoding="utf8").read()
        self.info_title = tk.Label(self, background= "lightgrey", width=100, borderwidth = 2, relief = "solid", text = self.info_text, font= 55)
        self.info_title.place(x = 270, y = 350)
               
        #Αυτή η μέθοδος "καταστρέφει" το παράθυρο της αρχικής σελίδας και δημιουργεί ένα αντικείμενο της
        #κλάσης IntroPage και το εμφανίζει μέσω του mainloop.
        #Με αυτή την μέθοδο επιστρέφει ο χρήστης πίσω στην αρχική σελίδα.
        def previous_page():
            self.destroy()
            from intro_page import IntroPage
            intro = IntroPage()
            intro.mainloop()

        #----------Buttons--------------#
        #Κουμπί για την επιστροφή στην αρχική σελίδα
        previous_page_button = tk.Button(self, text="Αρχική Σελίδα", command=previous_page)
        previous_page_button.place(x = 680, y = 900)