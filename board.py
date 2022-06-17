import sys
sys.dont_write_bytecode = True #Για να μην δημιουργείται σε κάθε εκτέλεση ο φάκελος pycache
import random
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk , Image
from letters_bag import Letters_bag
from word_check import Word_check
from player import Player
import special_tiles


class Board(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bag = Letters_bag() #Αντικείμενο της κλάσης Letter_bag
        self.check = Word_check() #Αντικείμενο της κλάσης Word_check
        self.computer = Player() #Αντικείμενο της κλάσης Player
        self.player = Player() #Αντικείμενο της κλάσης Player

        #--------Ρυθμίσεις παραθύρου---------#
        self.title("Scrabble")
        self.geometry("1520x980")
        self.configure(background="lightgrey")

        #-------------Canvas-----------------#
        self.canvas = tk.Canvas(self, width=800, height=910, highlightthickness = 0, background= "lightgrey")
        self.canvas.place(x=0, y= 0)

        #-----------Λογότυπο Scrabble------------#
        #Για να μπορέσω να επεξεργαστώ το μέγεθος της εικόνας αξιοποιώ το Image και το ImageTk
        #της βιβλιοθήκης PIL
        self.logo_image = Image.open("Scrabble.png")
        self.resized_logo = self.logo_image.resize((300, 125), Image.Resampling.LANCZOS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo = tk.Label(self, background= "lightgrey", image = self.new_logo, width= 500, height = 100)
        self.logo.place(x= 950, y = 50)

        #-----------Computer & Player Scores--------#
        #Σχεδιασμός για δείξω το σκορ ανάμεσα στον χρήστη και τον υπολογιστή
        self.highscore = tk.Label(self, background= "lightgrey", text = "SCORE", font= 55)
        self.highscore.place(x = 920, y =250)
        self.computer_score = tk.Label(self, background= "lightgrey", text = "Computer:", font= 55)
        self.computer_score.place(x = 900, y =280)
        #Το σκορ του υπολογιστή
        self.computer_score_number = tk.Label(self, background= "white", borderwidth = 2, relief = "solid", text = f"{self.computer.highscore}", font= 55)
        self.computer_score_number.place(x = 1000, y =280)
        self.player_score = tk.Label(self, background= "lightgrey", text = "Player:", font= 55)
        self.player_score.place(x = 900, y =300)
        #Το σκορ του χρήστη
        self.player_score_number = tk.Label(self, background= "white", borderwidth = 2, relief = "solid", text = f"{self.player.highscore}", font= 55)
        self.player_score_number.place(x = 1000, y =300)

        #----------Letter's Bag--------------#
        #Για να μπορέσω να επεξεργαστώ το μέγεθος της εικόνας αξιοποιώ το Image και το ImageTk
        #της βιβλιοθήκης PIL
        self.bag_image = Image.open("bag-of-tiles.png")
        self.resized_bag = self.bag_image.resize((200, 200), Image.Resampling.LANCZOS)
        self.new_bag = ImageTk.PhotoImage(self.resized_bag)
        self.final_bag = tk.Label(self, background= "lightgrey", image = self.new_bag, width= 200, height = 200)
        self.final_bag.place(x= 1200, y = 220)
        #Εμφανίζω τον αριθμών των γραμμάτων που υπάρχουν στην κληρωτίδα
        self.bag_letters_number = tk.Label(self, background= "white", borderwidth = 2, relief = "solid", text = f"{len(self.bag.letters_bag)}", font= 55)
        self.bag_letters_number.place(x = 1280, y =290)

        #----------Buttons--------------#
        #Κουμπί για τον έλεγχο της λέξης
        check_word_button = tk.Button(self, text="Έλεγχος λέξης", command=self.check_word)
        check_word_button.place(x = 900, y = 500)
        #Κουμπί για να πετάξει γράμμα ο χρήστης
        discard_button = tk.Button(self, text="Αντικατέστησε 1 γράμμα", command=self.switch_letter)
        discard_button.place(x = 900, y = 550)
        #Κουμπί για την αναίρεση κίνησης
        refund_button = tk.Button(self, text="Αναίρεση κίνησης", command=self.cancel_move)
        refund_button.place(x = 900, y = 600)
        #Κουμπί για να πάει Πάσο
        pass_button = tk.Button(self, text="Πάσο", command=self.pass_round)
        pass_button.place(x = 900, y = 650)
        #Κουμπί τερματισμού παιχνιδιού
        end_game_button = tk.Button(self, text="Τερματισμός παιχνιδιού", command=self.end_current_game)
        end_game_button.place(x = 900, y = 700)
        #Κουμπί τερματισμού της εφαρμογής
        exit_button = tk.Button(self, text="Κλείσιμο της εφαρμογής", command=self.destroy)
        exit_button.place(x = 1300, y = 900)

        #-----------Letter's Points---------------#
        #Σχεδιασμός για την παρουσίαση των πόντως κάθε γράμματος
        self.letter_points = open('letter_points.txt', encoding="utf8").read()
        letters_points = tk.Label(self, background= "lightgrey", width=30, borderwidth = 2, relief = "solid", text = self.letter_points, font= 55)
        letters_points.place(x = 1170, y = 500)
        
        self.turn = random.randint(0, 1) #Κλήρωση για το ποιος θα παίξει πρώτος
        self.first_round = True #Μεταβλητή ελέγχου για το αν βρισκόμαστε στον πρώτο γύρο
        self.first_word = True #Μεταβλητή ελέγχου για το αν η λέξη που θα εισαχθεί είναι η πρώτη του παιχνιδιού
        
        #Μεταβλητές για την μετακίνηση γραμμάτων είτε στο ταμπλό είτε μεταξύ των κελιών του χρήστη
        self.tags1 = "" #Μεταβλητή για να αποθηκευτούν οι συντεταγμένες από το κελί του χρήστη το οποίο παίρνω το γράμμα
        self.tags2 = "" #Μεταβλητή για να αποθηκευτούν οι συντεταγμένες από το κελί στο οποίο θέλω να μεταφέρω το γράμμα(είτε στο ταμπλό είτε για αλλαγή στα χέρια του χρήστη)
        self.transfer = False  #Μεταβλητή ελέγχου για το αν βρισκόμαστε σε διαδικασία μεταφοράς γράμματος
        self.transfer_letter = "" #Μεταβλητή αποθήκευσης του γράμματος που θα μεταφέρω
        self.transfer_letter_temp = "" #Μεταβλητή προσωρινής αποθήκευσης γράμματος για όταν θέλω να αλλάξω θέση στα γράμματα του χρήστη
        self.transfer_color = "white" #Μεταβλητή για μετατροπή κελιών σε χρώμα άσπρο, όταν αυτά θα περιέχουν γράμματα
        
        self.rects_list = [] #Λίστα 15x15 του ταμπλό για προσπέλαση και πρόσβαση στα γράμματα της λέξης του χρήστη
        self.rects = {} #Λεξικό 15x15 για εύκολη πρόσβαση στα κελιά για τροποποιήσεις(με κλειδιά τις συντεταγμένες και τιμές τα κελιά)

        #Μεταβλητές για τις συντεταγμένες του καμβά που θα δημιουργηθούν τα κελιά του ταμπλό
        self.x1 = 0 
        self.y1 = 0
        self.height = 50 
        self.width = 50

        #Με εμφωλευμένη επανάληψη δημιουργώ το λεξικό και την λίστα για το ταμπλό που είναι 15x15
        for x in range(15):
            #Αξιοποιώ και τροποποιώ τις μεταβλητές για τις συντεταγμένες ώστε να σχεδιαστούν τα κελιά του ταμπλό στο κατάλληλο σημείο του καμβά
            self.y1+=50
            self.width += 50
            self.rects_list.append([])
            for y in range(15):
                self.x1+=50
                self.height += 50
                #Χρησιμοποιώ το module special_tiles για αμυντικό έλεγχο, ώστε να γίνει η αντίστοιχη σχεδίαση του κελιού
                #Στο tile_rect αποθηκεύω τις τιμές του τετραγώνου που ζωγραφίστηκε στον καμβά
                #Στο tile_txt αποθηκεύω τις τιμές του κειμένου που τοποθετήσαμε πάνω στο τετράγωνο του καμβά
                #Και οι 2 μεταβλητές έχουν τις συντεταγμένες ως τιμή στην παράμετρο tags ώστε να είναι "συνδεδεμένες" μεταξύ τους
                if special_tiles.triple_word(x, y): #Κελί για λέξη τριπλής αξίας
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="red", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.triple_letter(x, y): #Κελί για γράμμα τριπλής αξίας
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.double_letter(x, y): #Κελί για γράμμα διπλής αξίας
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.double_word(x,y): #Κελί για λέξη διπλής αξίας
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.center(x, y): #Κεντρικό κελί
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="ΑΡΧΗ", tags= f"{x},{y}")
                else:
                    #Κλασικά κελιά του ταμπλό
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fil="green", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="", tags= f"{x},{y}")
                board_tile_empty = True #Μεταβλητή για το αν το κελί ΔΕΝ περιέχει γράμμα
                previous_round_letter = False #Μεταβλητή για το αν το συγκεκριμένο γράμμα είχε τοποθετηθεί από προηγούμενο γύρο
                #Λεξικό όπου χρησιμοποιώ για κλειδί τις συντεταγμένες για να αποθηκεύσω σε τιμές τις μεταβλητές που χρειαζόμαστε για κάθε κελί
                self.rects[(f"{x},{y}")] = [tile_rect, tile_txt, board_tile_empty, previous_round_letter]
                #Η λίστα περιέχει στα κελιά της κενό το οποίο θα αντικαθίσταται με το γράμμα του χρήστη όταν εισάγεται,
                #για πιο εύκολη προσπέλαση κατά την δημιουργία της λέξης.
                self.rects_list[x].append(" ")
            
            #Αξιοποιώ και τροποποιώ τις μεταβλητές για τις συντεταγμένες ώστε να σχεδιαστούν τα κελιά του ταμπλό στο κατάλληλο σημείο του καμβά
            self.x1= 0
            self.height= 50

        self.player_tiles = {} #Λεξικό για τα κελιά του χρήστη
        
        #Μεταβλητές για τις συντεταγμένες του καμβά στον οποίο θα σχεδιαστούν τα κελιά του χρήστη
        self.p_x1 = 250
        self.p_y1 = 850
        self.p_height = 300
        self.p_width = 900

        #Με επανάληψη δημιουργώ το λεξικό για τον σχεδιασμό των 7 κελιών του χρήστη
        for i in range(7):
            #Στο tile_rect αποθηκεύω τις τιμές του τετραγώνου που ζωγραφίστηκε στον καμβά
            #Στο tile_txt αποθηκεύω τις τιμές του κειμένου που τοποθετήσαμε πάνω στο τετράγωνο του καμβά
            #Και οι 2 μεταβλητές έχουν τις συντεταγμένες ως τιμή στην παράμετρο tags ώστε να είναι "συνδεδεμένες" μεταξύ τους
            player_tile_rect = self.canvas.create_rectangle(self.p_x1, self.p_y1, self.p_height, self.p_width, outline = "white", fill="black", tags= f"{i}")
            player_tile_txt = self.canvas.create_text((self.p_x1 + self.p_height)/ 2, (self.p_y1 + self.p_width)/2, anchor='center', text= "", tags= f"{i}")
            player_tile_empty = True #Μεταβλητή για το αν το κελί ΔΕΝ περιέχει γράμμα
            #Λεξικό όπου χρησιμοποιώ για κλειδί τις συντεταγμένες για να αποθηκεύσω σε τιμές τις μεταβλητές που χρειαζόμαστε για κάθε κελί
            self.player_tiles[f"{i}"] = [player_tile_rect, player_tile_txt, player_tile_empty]
            #Αξιοποιώ και τροποποιώ τις μεταβλητές για τις συντεταγμένες ώστε να σχεδιαστούν τα κελιά του ταμπλό στο κατάλληλο σημείο του καμβά
            self.p_x1 += 50
            self.p_height += 50
        
        #Κάνω bind το αριστερό κουμπί του ποντικιού, το οπόιο όταν κάνει κλικ με αυτό ο χρήστης
        # πάνω στον καμβά, καλείται η μέθοδος on_click      
        self.canvas.bind('<Button-1>', self.on_click)
        
        #Καλώ την μέθοδο main
        self.main()
        
    #Μέθοδος για την μεταφορά του γράμματος μέσω του ποντικιού του χρήστη
    #Η μέθοδος αυτή λειτουργεί ως εξής. Πρώτα κάνει κλικ στο γράμμα της επιλογής του και μετά ξανά κάνει κλικ είτε 
    # στο ταμπλό είτε σε άλλο γράμμα στο χέρι του για να τα αλλάξει θέση μεταξύ τους.
    def on_click(self, event):
        
        if self.transfer == False: #Με αυτή την μεταβλητή ελέγχω αν υπάρχει ήδη επιλεγμένο γράμμα έτοιμο προς μετακίνηση
            item1 = self.canvas.find_closest(event.x, event.y) #Εντοπίζω μέσω του κέρσορα το πιο κοντινό αντικείμενο(κελί) στον καμβά
            self.tags1 = self.canvas.itemcget(item1, "tags").replace(" current", "") #Από το αντικείμενο παίρνω τις συντεταγμένες που είναι αποθηκευμένες στο tags
            if self.tags1 in self.player_tiles and self.player_tiles[self.tags1][2] == False:#Από την στιγμή που τώρα ξεκινάει η διαδικασία, ελέγχω αν έγινε κλικ σε γράμμα του χρήστη
                self.transfer_letter = self.canvas.itemcget(self.player_tiles[self.tags1][1], "text")#Αποθηκεύω το γράμμα που υπάρχει στο κελί του χρήστη από το λεξικό
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], fill = "yellow")#Αλλάζω το χρώμα από άσπρο σε κίτρινο στο λεξικό για το επιλεγμένο γράμμα
                self.transfer = True #Αλλάζω την τιμή σε True, αφού πλέον έχει ξεκινήσει η διαδικασία μεταφοράς του γράμματος
        else: #Υπάρχει ήδη επιλεγμένο γράμμα έτοιμο προς μετακίνηση
            item2 = self.canvas.find_closest(event.x, event.y) #Εντοπίζω μέσω του κέρσορα το πιο κοντινό (δεύτερο)αντικείμενο(κελί) στον καμβά
            self.tags2 = self.canvas.itemcget(item2, "tags").replace(" current", "") #Από το αντικείμενο παίρνω τις συντεταγμένες που είναι αποθηκευμένες στο tags
            #Σε περίπτωση που ο χρήστης θέλει να αλλάξει την σειρά των γραμμάτων που κρατάει
            if self.tags2 in self.player_tiles and self.player_tiles[self.tags2][2] == False: #Ελέγχω αν έχει γίνει κλικ σε κελί του χρήστη που περιέχει γράμμα
                self.transfer_letter_temp = self.canvas.itemcget(self.player_tiles[self.tags2][1], "text") #Αποθήκευση του γράμματος σε προσωρινή μεταβλήτ για την μεταφορά
                self.canvas.itemconfigure(self.player_tiles[self.tags2][1], text= self.transfer_letter) #Γίνεται η αλλαγή γράμματος στο ένα από τα δύο κελιά
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= self.transfer_letter_temp) #Γίνεται η αλλαγή γράμματος στο ένα από τα δύο κελιά
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], fill = self.transfer_color) #Το επιλεγμένο κελί που ήταν κίτρινο, ξανά γίνεται άσπρο αφού δεν είναι επιλεγμένο πλέον
                self.transfer = False #Αλλάζω την τιμή σε False αφού πλέον τελείωσε η διαδικασία μεταφοράς του γράμματος
            #Σε περίπτωση που ο χρήστης θέλει να αλλάξει την σειρά των γραμμάτων του σε κενό κελί του
            elif self.tags2 in self.player_tiles and self.player_tiles[self.tags2][2] : #Ελέγχω αν έχει γίνει κλικ σε κελί του χρήστη που ΔΕΝ περιέχει γράμμα
                self.transfer_letter_temp = self.canvas.itemcget(self.player_tiles[self.tags2][1], "text") #Αποθήκευση του γράμματος σε προσωρινή μεταβλήτ για την μεταφορά
                self.canvas.itemconfigure(self.player_tiles[self.tags2][1], text= self.transfer_letter) #Αλλάζω το text σε ""(κενό) αφού δεν θα περιέχει γράμμα
                self.canvas.itemconfigure(self.player_tiles[self.tags2][0], outline = "black", fill = self.transfer_color) #Το κενό κελί που ήταν μαύρο χρώμα, γίνεται άσπρο
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= self.transfer_letter_temp) #Αντικαθιστώ το "" με το γράμμα στο νέο κελί που θα το περιέχει
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black") #Το νέο πλέον κενό κελί, από άσπρο χρώμα γίνεται μαύρο
                self.player_tiles[self.tags2][2] = False #Αλλάζει η τιμή σε False αφού πλέον το κελί περιέχει γράμμα
                self.player_tiles[self.tags1][2] = True #Αλλάζει η τιμή σε True αφού πλέον το κελί ΔΕΝ περιέχει γράμμα
                self.transfer = False #Αλλάζω την τιμή σε False αφού πλέον τελείωσε η διαδικασία μεταφοράς του γράμματος
            #Σε περίπτωση που ο χρήστης τοποθετεί γράμμα στο ταμπλό
            elif self.tags2 in self.rects and self.rects[self.tags2][2] and self.turn == 1:#Ελέγχω αν έγινε κλικ σε άδειο κελί του ταμπλό και αν είναι ο γύρος του χρήστη
                self.canvas.itemconfigure(self.rects[self.tags2][1], font=("ariel", 36), anchor='center', text= self.transfer_letter) #Μεταφέρω το γράμμα στο κελί του ταμπλό
                self.canvas.itemconfigure(self.rects[self.tags2][0], fill= self.transfer_color ) #Αλλάζω το κελί του ταμπλό σε άσπρο χρώμα
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black") #Το κελί του χρήστη στο οποίο ήταν το γράμμα γίνεται μαύρο
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= "") #Αφαιρώ το γράμμα από το κελί του χρήστη στο οποίο βρισκόταν πριν
                self.player_tiles[self.tags1][2] = True #Αλλάζει η τιμή σε True αφού πλέον το κελί ΔΕΝ περιέχει γράμμα
                self.rects[self.tags2][2] = False #Αλλάζει η τιμή σε False αφού πλέον το κελί περιέχει γράμμα
                self.transfer = False #Αλλάζω την τιμή σε False αφού πλέον τελείωσε η διαδικασία μεταφοράς του γράμματος
                self.player.coords_cancel.append(self.tags2) #Αποθηκεύω τις συντεταγμένες του γεμάτου πλέον κελιού του ταμπλό, στην λίστα που υπάρχει για αναίρεση κινήσεων
                coords = self.tags2.split(",") # Χωρίζω τις συντεταγμένες του κελιού του ταμπλό
                self.player.x_coords.append(int(coords[0])) #Αποθηκεύω την τιμή του άξονα x
                self.player.y_coords.append(int(coords[1])) #Αποθηκεύω την τιμή του άξονα y
                self.rects_list[int(coords[0])][int(coords[1])] = self.transfer_letter #Στην λίστα 15x15 που έχω για προσπέλαση, αντικαθιστώ το κενό με το γράμμα του χρήστη στην ανάλογη θέση
                self.player.used_letters.append(self.transfer_letter) #Αποθηκεύω το γράμμα στην λίστα που υπάρχει για τα γράμματα του τρέχοντα γύρου



    #Μέθοδος για την εγκυρότητα της λέξης που εισήγαγε ο χρήστης
    def check_word(self):
        if self.turn == 1: #Έλεγχος για το αν είναι ο γύρος που παίζει ο χρήστης
            if len(self.player.x_coords) == 1 and len(self.player.y_coords) == 1: #Ελέγχω την περίπτωση που ο χρήστης χρησιμοποιεί μόνο 1 γράμμα για δημιουργία λέξης
                self.player.multi_words_x_coords =  self.player.x_coords.copy() #Αντιγράφω τα περιεχόμενα(συντεταγμένες άξονα x) χωρίς όμως να είναι συνδεδεμένα μεταξύ τους
                self.player.multi_words_y_coords =  self.player.y_coords.copy()  #Αντιγράφω τα περιεχόμενα(συντεταγμένες άξονα y) χωρίς όμως να είναι συνδεδεμένα μεταξύ τους

                #Αναζητώ σε διπλανά κελιά, για τυχόν γράμματα που έχει γειτνίαση το γράμμα του χρήστη, ώστε να προσθέσω συντεταγμένες στις λίστες
                # επειδή οι υπάρχουσες μεθόδοι στην κλάση player, χρειάζονται 2 τιμές τουλάχιστον σε κάθε λίστα για να γίνει η προετοιμασία.
                # Περισσότερα σχόλια πάνω σε αυτό, στην κλάση player σε κάθε μέθοδο της.
                if self.rects[f"{self.player.x_coords[0] + 1},{self.player.y_coords[0]}"][2] == False:#Έλεγχος σε περίπτωση που υπάρχει γράμμα κάτω από το γράμμα του χρήστη
                    self.player.x_coords.append(self.player.x_coords[0] + 1) #Αποθηκεύω την τιμή του άξονα x
                    self.player.y_coords.append(self.player.y_coords[0]) #Αποθηκεύω την τιμή του άξονα y
                elif self.rects[f"{self.player.x_coords[0] - 1},{self.player.y_coords[0]}"][2] == False:#Έλεγχος σε περίπτωση που υπάρχει γράμμα πάνω από το γράμμα του χρήστη
                    self.player.x_coords.append(self.player.x_coords[0] - 1) #Αποθηκεύω την τιμή του άξονα x
                    self.player.y_coords.append(self.player.y_coords[0]) #Αποθηκεύω την τιμή του άξονα y
                elif self.rects[f"{self.player.x_coords[0]},{self.player.y_coords[0] + 1}"][2] == False:#Έλεγχος σε περίπτωση που υπάρχει γράμμα δεξιά από το γράμμα του χρήστη
                    self.player.x_coords.append(self.player.x_coords[0]) #Αποθηκεύω την τιμή του άξονα x
                    self.player.y_coords.append(self.player.y_coords[0] + 1) #Αποθηκεύω την τιμή του άξονα y
                elif self.rects[f"{self.player.x_coords[0]},{self.player.y_coords[0] - 1}"][2] == False:#Έλεγχος σε περίπτωση που υπάρχει γράμμα αριστερά από το γράμμα του χρήστη
                    self.player.x_coords.append(self.player.x_coords[0]) #Αποθηκεύω την τιμή του άξονα x
                    self.player.y_coords.append(self.player.y_coords[0] - 1) #Αποθηκεύω την τιμή του άξονα y
            
                  
                self.player.prepare_coords() #Γίνεται ταξίνόμηση των λιστών με τις συντεταγμένες
                self.player.validate_coords() #Επιβεβαιώνω τον άξονα στον οποίο βρίσκεται η λέξη
                self.player.process_coords() #Εντοπίζω τον άξονα στον οποίο βρίσκεται η λέξη
            else:
                self.player.prepare_coords() #Γίνεται ταξίνόμηση των λιστών με τις συντεταγμένες
                self.player.multi_words_x_coords =  self.player.x_coords.copy() #Αντιγράφω τα περιεχόμενα(συντεταγμένες άξονα x) χωρίς όμως να είναι συνδεδεμένα μεταξύ τους
                self.player.multi_words_y_coords =  self.player.y_coords.copy() #Αντιγράφω τα περιεχόμενα(συντεταγμένες άξονα y) χωρίς όμως να είναι συνδεδεμένα μεταξύ τους
                self.player.validate_coords() #Επιβεβαιώνω τον άξονα στον οποίο βρίσκεται η λέξη
                self.player.process_coords() #Εντοπίζω τον άξονα στον οποίο βρίσκεται η λέξη


            if self.player.first_check: #Αμυντικός προγραμματισμός για το αν έχει τοποθετήσει σωστά τα γράμματά του ο χρήστης
                #Ανάλογα με το αν η λέξη είναι οριζόντια ή κάθετη, κάνω προσπέλαση τα διπλανά κελιά για να έχω πρόσβαση σε όλα τα γράμματα της λέξης
                if self.player.y_axis: #Σε περίπτωση που η λέξη είναι κάθετη

                    #Κάνω προσπέλαση προς τα πάνω μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                    while self.player.word_start != 0:
                        if self.rects[f"{self.player.word_start - 1},{self.player.word_axis}"][2] == False: #Ελέγχω αν το πάνω κελί περιέχει γράμμα
                            self.player.word_start -=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα x, στην οποία ξεκινάει η λέξη
                        else: #Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                            break
                    
                    #Κάνω προσπέλαση προς τα κάτω μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                    while self.player.word_finish != 14:
                        if self.rects[f"{self.player.word_finish + 1},{self.player.word_axis}"][2] == False: #Ελέγχω αν το κάτω κελί περιέχει γράμμα
                            self.player.word_finish +=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα x, στην οποία τελειώνει η λέξη
                        else:#Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                            break

                    #Δημιουργώ την λέξη του χρήστη
                    for letter in range(self.player.word_start, self.player.word_finish+1): #Παίρνω τις τιμές του άξονα στον οποίο κινείται η λέξη
                        #Προσθέτω στην λίστα ένα ένα τα γράμματα της λέξης κατά την διάρκεια  της επανάληψης
                        self.player.word_letters.append(self.rects_list[letter][self.player.word_axis])
                        #Αποθήκευση των συντεταγμένων των γραμμάτων που εισήγαγε ο χρήστης σε αυτόν τον γύρο, ώστε μετά το τέλος ενός έγκυρου γύρου
                        #αυτά τα γράμματα θα μπορούν να χρησιμοποιηθούν ως γράμματα προηγούμενου γύρου για την δημιουργία λέξης, βάσει κανόνων
                        self.player.previous_coords.append(f"{letter},{self.player.word_axis}")

                    self.player.word = "".join(self.player.word_letters) #Ενώνω τα γράμματα για την δημιουργία της λέξης
                    self.player.words_to_check.append(self.player.word) #Εισάγω την λέξη στην λίστα αποθήκευσης λέξεων του τρέχοντα γύρου(που θα γίνει έλεγχος εγκυρότητάς τους)
                    self.calculate_points() #Γίνεται υπολογισμός των πόντων της λέξης, χωρίς όμως να προστεθούν ακόμη στο συνολικό σκορ του χρήστη

                    #Σε περίπτωση που δεν είναι η πρώτη λέξη του παιχνιδιού, πρέπει να ελέγξω αν τα γράμματα που τοποθέτησε ο χρήστης
                    #έχουν γειτνίαση με άλλα γράμματα από προηγούμενους γύρους
                    if self.first_word == False:
                        self.player.word_letters.clear() #Προετοιμάζω την λίστα για τα γράμματα πιθανών έξτρα λέξεων
                        self.player.x_axis = True #Αλλαγή του άξονα στον οποίο θα κάνω προσπέλαση
                        self.player.y_axis = False #Αλλαγή του άξονα στον οποίο θα κάνω προσπέλαση
                        
                        #Γίνεται προσπέλαση σε κάθε γράμμα που τοποθέτησε ο χρήστης για να εντοπίσω τυχόν γειτνίαση με άλλα γράμματα
                        for i in range(len(self.player.multi_words_x_coords)):
                            if self.rects[f"{self.player.multi_words_x_coords[i]},{self.player.multi_words_y_coords[i] + 1}"][2] == False: #Έλεγχος σε περίπτωση που υπάρχει γράμμα δεξιά από το γράμμα του χρήστη
                                self.player.word_start = self.player.multi_words_y_coords[i] #Ορίζω νέα τιμή στην οποία ξεκινάει η λέξη
                                self.player.word_finish = self.player.multi_words_y_coords[i] + 1  #Ορίζω νέα τιμή στην οποία τελειώνει η λέξη
                                self.player.word_axis = self.player.multi_words_x_coords[i] #Ορίζω την τιμή του νέου άξονα που θα κινηθώ
                            elif self.rects[f"{self.player.multi_words_x_coords[i]},{self.player.multi_words_y_coords[i] - 1}"][2] == False: #Έλεγχος σε περίπτωση που υπάρχει γράμμα αριστερά από το γράμμα του χρήστη
                                self.player.word_start = self.player.multi_words_y_coords[i] - 1  #Ορίζω νέα τιμή στην οποία ξεκινάει η λέξη
                                self.player.word_finish = self.player.multi_words_y_coords[i] #Ορίζω νέα τιμή στην οποία τελειώνει η λέξη
                                self.player.word_axis = self.player.multi_words_x_coords[i] #Ορίζω την τιμή του νέου άξονα που θα κινηθώ
                            else: #Σε περίπτωση που δεν υπάρχει γειτνίαση
                                self.player.word_start = self.player.multi_words_y_coords[i] #Η τιμή είναι αυτή του γράμματος του χρήστη
                                self.player.word_finish = self.player.multi_words_y_coords[i] #Η τιμή είναι αυτή του γράμματος του χρήστη
                                self.player.word_axis = self.player.multi_words_x_coords[i] #Η τιμή είναι αυτή του γράμματος του χρήστη

                            #Κάνω προσπέλαση προς τα αριστερά μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                            while self.player.word_start != 0:
                                if self.rects[f"{self.player.word_axis},{self.player.word_start - 1}"][2] == False: #Ελέγχω αν το αριστερό κελί περιέχει γράμμα
                                    self.player.word_start -=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα y, στην οποία αρχίζει η λέξη
                                else: #Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                                    break
                            
                            #Κάνω προσπέλαση προς τα δεξιά μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                            while self.player.word_finish != 14:
                                if self.rects[f"{self.player.word_axis},{self.player.word_finish + 1}"][2] == False: #Ελέγχω αν το δεξί κελί περιέχει γράμμα
                                    self.player.word_finish +=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα y, στην οποία τελειώνει η λέξη
                                else: #Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                                    break

                            #Δημιουργώ την λέξη του χρήστη
                            for letter in range(self.player.word_start, self.player.word_finish+1): #Παίρνω τις τιμές του άξονα στον οποίο κινείται η λέξη
                                #Προσθέτω στην λίστα ένα ένα τα γράμματα της λέξης κατά την διάρκεια  της επανάληψης
                                self.player.word_letters.append(self.rects_list[self.player.word_axis][letter])

                            self.player.word = "".join(self.player.word_letters) #Ενώνω τα γράμματα για την δημιουργία της λέξης
                            if len(self.player.word_letters) > 1: #Αν τα γράμματα είναι πάνω από ένα. Δηλαδή υπήρχε γειτνίαση
                                self.player.words_to_check.append(self.player.word) #Εισάγω την λέξη στην λίστα αποθήκευσης λέξεων του τρέχοντα γύρου(που θα γίνει έλεγχος εγκυρότητάς τους)
                                self.calculate_points() #Γίνεται υπολογισμός των πόντων της λέξης, χωρίς όμως να προστεθούν ακόμη στο συνολικό σκορ του χρήστη
                            
                            self.player.word_letters.clear() #Προετοιμασία της λίστας γραμμάτων για την επόμενη επανάληψη
                            
                #Ανάλογα με το αν η λέξη είναι οριζόντια ή κάθετη, κάνω προσπέλαση τα διπλανά κελιά για να έχω πρόσβαση σε όλα τα γράμματα της λέξης
                else: #Σε περίπτωση που η λέξη είναι οριζόντια

                    #Κάνω προσπέλαση προς τα αριστερά μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                    while self.player.word_start != 0:
                        if self.rects[f"{self.player.word_axis},{self.player.word_start - 1}"][2] == False: #Ελέγχω αν το αριστερό κελί περιέχει γράμμα
                            self.player.word_start -=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα y, στην οποία ξεκινάει η λέξη
                        else:#Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                            break
                    
                    #Κάνω προσπέλαση προς τα δεξιά μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                    while self.player.word_finish != 14:
                        if self.rects[f"{self.player.word_axis},{self.player.word_finish + 1}"][2] == False: #Ελέγχω αν το δεξί κελί περιέχει γράμμα
                            self.player.word_finish +=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα y, στην οποία τελειώνει η λέξη
                        else:#Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                            break

                    #Δημιουργώ την λέξη του χρήστη
                    for letter in range(self.player.word_start, self.player.word_finish+1): #Παίρνω τις τιμές του άξονα στον οποίο κινείται η λέξη
                        #Προσθέτω στην λίστα ένα ένα τα γράμματα της λέξης κατά την διάρκεια  της επανάληψης
                        self.player.word_letters.append(self.rects_list[self.player.word_axis][letter])
                        #Αποθήκευση των συντεταγμένων των γραμμάτων που εισήγαγε ο χρήστης σε αυτόν τον γύρο, ώστε μετά το τέλος ενός έγκυρου γύρου
                        #αυτά τα γράμματα θα μπορούν να χρησιμοποιηθούν ως γράμματα προηγούμενου γύρου για την δημιουργία λέξης, βάσει κανόνων
                        self.player.previous_coords.append(f"{self.player.word_axis},{letter}")

                    self.player.word = "".join(self.player.word_letters) #Ενώνω τα γράμματα για την δημιουργία της λέξης
                    self.player.words_to_check.append(self.player.word) #Εισάγω την λέξη στην λίστα αποθήκευσης λέξεων του τρέχοντα γύρου(που θα γίνει έλεγχος εγκυρότητάς τους)
                    self.calculate_points() #Γίνεται υπολογισμός των πόντων της λέξης, χωρίς όμως να προστεθούν ακόμη στο συνολικό σκορ του χρήστη
                    
                    #Σε περίπτωση που δεν είναι η πρώτη λέξη του παιχνιδιού, πρέπει να ελέγξω αν τα γράμματα που τοποθέτησε ο χρήστης
                    #έχουν γειτνίαση με άλλα γράμματα από προηγούμενους γύρους
                    if self.first_word == False:
                        self.player.word_letters.clear() #Προετοιμάζω την λίστα για τα γράμματα πιθανών έξτρα λέξεων
                        self.player.x_axis = False #Αλλαγή του άξονα στον οποίο θα κάνω προσπέλαση
                        self.player.y_axis = True #Αλλαγή του άξονα στον οποίο θα κάνω προσπέλαση

                        #Γίνεται προσπέλαση σε κάθε γράμμα που τοποθέτησε ο χρήστης για να εντοπίσω τυχόν γειτνίαση με άλλα γράμματα
                        for i in range(len(self.player.multi_words_x_coords)):
                            if self.rects[f"{self.player.multi_words_x_coords[i] + 1},{self.player.multi_words_y_coords[i]}"][2] == False: #Έλεγχος σε περίπτωση που υπάρχει γράμμα πάνω από το γράμμα του χρήστη
                                self.player.word_start = self.player.multi_words_x_coords[i] #Ορίζω νέα τιμή στην οποία ξεκινάει η λέξη
                                self.player.word_finish = self.player.multi_words_x_coords[i] + 1  #Ορίζω νέα τιμή στην οποία τελειώνει η λέξη
                                self.player.word_axis = self.player.multi_words_y_coords[i]  #Ορίζω την τιμή του νέου άξονα που θα κινηθώ
                            elif self.rects[f"{self.player.multi_words_x_coords[i] - 1},{self.player.multi_words_y_coords[i]}"][2] == False: #Έλεγχος σε περίπτωση που υπάρχει γράμμα κάτω από το γράμμα του χρήστη
                                self.player.word_start = self.player.multi_words_x_coords[i] - 1 #Ορίζω νέα τιμή στην οποία ξεκινάει η λέξη
                                self.player.word_finish = self.player.multi_words_x_coords[i]  #Ορίζω νέα τιμή στην οποία τελειώνει η λέξη
                                self.player.word_axis = self.player.multi_words_y_coords[i]  #Ορίζω την τιμή του νέου άξονα που θα κινηθώ
                            else: #Σε περίπτωση που δεν υπάρχει γειτνίαση
                                self.player.word_start = self.player.multi_words_x_coords[i] #Η τιμή είναι αυτή του γράμματος του χρήστη
                                self.player.word_finish = self.player.multi_words_x_coords[i] #Η τιμή είναι αυτή του γράμματος του χρήστη
                                self.player.word_axis = self.player.multi_words_y_coords[i] #Η τιμή είναι αυτή του γράμματος του χρήστη
                            

                            #Κάνω προσπέλαση προς τα πάνω μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                            while self.player.word_start != 0:
                                if self.rects[f"{self.player.word_start - 1},{self.player.word_axis}"][2] == False: #Ελέγχω αν το πάνω κελί περιέχει γράμμα
                                    self.player.word_start -=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα x, στην οποία αρχίζει η λέξη
                                else: #Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                                    break

                            #Κάνω προσπέλαση προς τα κάτω μέχρι να βρώ άδειο κελί από γράμμα ή να φτάσω στην άκρη του ταμπλό
                            while self.player.word_finish != 14:
                                if self.rects[f"{self.player.word_finish + 1},{self.player.word_axis}"][2] == False: #Ελέγχω αν το κάτω κελί περιέχει γράμμα
                                    self.player.word_finish +=1 #Άμα περιέχει τότε αλλάζει η τιμή του άξονα x, στην οποία τελειώνει η λέξη
                                else: #Αν κατά την διάρκεια πέσω σε άδειο κελί τότε βγαίνω από την επανάληψη
                                    break
                            
                            
                            #Δημιουργώ την λέξη του χρήστη
                            for letter in range(self.player.word_start, self.player.word_finish+1): #Παίρνω τις τιμές του άξονα στον οποίο κινείται η λέξη
                                #Προσθέτω στην λίστα ένα ένα τα γράμματα της λέξης κατά την διάρκεια  της επανάληψης
                                self.player.word_letters.append(self.rects_list[letter][self.player.word_axis])

                            self.player.word = "".join(self.player.word_letters) #Ενώνω τα γράμματα για την δημιουργία της λέξης
                            if len(self.player.word_letters) > 1:  #Αν τα γράμματα είναι πάνω από ένα. Δηλαδή υπήρχε γειτνίαση
                                self.player.words_to_check.append(self.player.word) #Εισάγω την λέξη στην λίστα αποθήκευσης λέξεων του τρέχοντα γύρου(που θα γίνει έλεγχος εγκυρότητάς τους)
                                self.calculate_points() #Γίνεται υπολογισμός των πόντων της λέξης, χωρίς όμως να προστεθούν ακόμη στο συνολικό σκορ του χρήστη

                            self.player.word_letters.clear() #Προετοιμασία της λίστας γραμμάτων για την επόμενη επανάληψη
                            
                if self.rects["7,7"][2] == False and self.first_word: #Ελέγχω αν το κεντρικό κελί έχει γράμμα βάσει κανόνων και άμα είμαστε στην πρώτη λέξη του παιχνιδιού
                    if self.check.check_for_valid_word(self.player.words_to_check[0]): #Ελέγχω την εγκυρότητα της πρώτης λέξης του παιχνιδιού
                        self.player.add_points() #Σε περίπτωση που ήταν έγκυρη η λέξη, προσθέτω τους πόντους στο συνολικό σκορ του χρήστη
                        self.turn = 0 #Αλλάζει η τιμή ώστε στον επόμενο γύρο να παίξει ο υπολογιστής
                        for i in range(len(self.player.coords_cancel)): #Κάνω προσπέλαση τις συντεταγμένες των γραμμάτων που τοποθέτησε ο χρήστης για να αλλάξω την τιμή τους στο λεξικό
                            #Αυτά τα γράμματα πλέον θεωρούνται γράμματα προηγούμενου γύρου που βάσει κανόνων ο χρήστης πρέπει να χρησιμοποιήσει 1 από αυτά για την δημιουργία της λέξης του
                            self.rects[self.player.coords_cancel[i]][3] = True 
                        self.first_word = False #Παίρνει την τιμή False αφού πλέον δεν βρισκόμαστε στην πρώτη λέξη του παιχνιδιού
                        self.player_score_number.configure(text = f"{self.player.highscore}") #Ενημερώνω το κείμενο που δείχνει το σκορ του χρήστη
                        self.player.reset_values() #Επαναφέρω τις τιμές των μεταβλητών στις αρχικές τους τιμές, για να είναι έτοιμες για τον επόμενο γύρο
                        self.player.letter_switch = 0 #Επαναφέρω την τιμή των επιτρεπόμενων επιστροφών γραμμάτων στην κληρωτίδα
                        self.main() #Καλώ την main
                    else: #Σε περίπτωση μη έγκυρης λέξης
                        self.remove_word() #Επιστρέφονται τα γράμματα πίσω στα χέρια του χρήστη
                elif self.first_word == False: #Στην περίπτωση όπου έχω περάσει τον πρώτο γύρο και βρισκόμαστε στις επόμενες λέξεις
                    for letter in self.player.previous_coords: #Κάνω προσπέλαση τα κελιά των γραμμάτων της λέξης του χρήστη
                        if self.rects[letter][3]: #Αν κάποιο από αυτά, είναι τοποθετημένα στο ταμπλό από τον προηγούμενο γύρο
                            self.player.second_check = True #Τότε παίρνει την τιμή True και γίνεται break
                            break
                    if self.player.second_check: #Αν έχει την τιμή True
                        for word in self.player.words_to_check: #Τότε κάνω προσπέλαση όλες τις λέξεις που δημιουργήθηκαν από γειτνίαση
                            if self.check.check_for_valid_word(word) == False: #Αν κάποια από αυτές δεν είναι έγκυρες
                                self.player.words_ready = False #Τότε παίρνει την τιμή False και γίνεται break
                                break
                            if self.player.words_ready: #Αν όλες οι λέξεις είναι έγκυρες
                                self.player.add_points() #Προσθέτω τους πόντους στο συνολικό σκορ του χρήστη
                                self.turn = 0 #Αλλάζει η τιμή ώστε στον επόμενο γύρο να παίξει ο υπολογιστής
                                for i in range(len(self.player.coords_cancel)): #Κάνω προσπέλαση τις συντεταγμένες των γραμμάτων που τοποθέτησε ο χρήστης για να αλλάξω την τιμή τους στο λεξικό
                                    #Αυτά τα γράμματα πλέον θεωρούνται γράμματα προηγούμενου γύρου που βάσει κανόνων ο χρήστης πρέπει να χρησιμοποιήσει 1 από αυτά για την δημιουργία της λέξης του
                                    self.rects[self.player.coords_cancel[i]][3] = True
                                self.player_score_number.configure(text = f"{self.player.highscore}") #Ενημερώνω το κείμενο που δείχνει το σκορ του χρήστη
                                self.player.reset_values() #Επαναφέρω τις τιμές των μεταβλητών στις αρχικές τους τιμές, για να είναι έτοιμες για τον επόμενο γύρο
                                self.player.letter_switch = 0 #Επαναφέρω την τιμή των επιτρεπόμενων επιστροφών γραμμάτων στην κληρωτίδα
                                self.main() #Καλώ την main
                            else:
                                self.remove_word() #Επιστρέφονται τα γράμματα πίσω στα χέρια του χρήστη
                    else:
                        self.remove_word() #Επιστρέφονται τα γράμματα πίσω στα χέρια του χρήστη
                else:
                    self.remove_word() #Επιστρέφονται τα γράμματα πίσω στα χέρια του χρήστη
            else:
                self.remove_word() #Επιστρέφονται τα γράμματα πίσω στα χέρια του χρήστη

    #Μέθοδος για να πάει πάσο ο χρήστης
    def pass_round(self):
        if self.turn == 1: #Ελέγχω αν είναι ο γύρος του χρήστη
            self.remove_word() #Επιστρέφω στα χέρια του χρήστη τυχόν ξεχασμένα γράμματα που είναι ακόμη τοποθετημένα στο ταμπλό και επαναφέρω τις τιμές των μεταβλητών
            self.player.letter_switch = 0 #Επαναφέρω την τιμή των επιτρεπόμενων επιστροφών γραμμάτων στην κληρωτίδα
            self.turn = 0 #Αλλάζω την τιμή σε 0, για να είναι η σειρά του υπολογιστή στον επόμενο γύρο
            self.main() #Καλώ την main

    #Μέθοδος για να κάνει αναίρεση την τελευταία κίνησή του ο χρήστης
    def cancel_move(self):
        if len(self.player.coords_cancel) > 0 and self.turn == 1: #Ελέγχω για το αν η λίστα που υπάρχει για την αναίρεση περιέχει μέσα τιμές και αν είναι ο γύρος του χρήστη
            cancel_tags = self.player.coords_cancel.pop() #Παίρνω την τελευταία τιμή από την λίστα συντεταγμένων(δηλαδή την τελευταία κίνηση που έκανε ο χρήστης)
            self.player.x_coords.pop() #Αφαιρώ από τις συντεταγμένες την τελευταία τιμή
            self.player.y_coords.pop() #Αφαιρώ από τις συντεταγμένες την τελευταία τιμή
            cancel_coords = cancel_tags.split(",") #Χωρίζω τις συντεταγμένες
            cancel_x = int(cancel_coords[0]) #Αποθηκεύω την τιμή για τον άξονα x
            cancel_y = int(cancel_coords[1]) #Αποθηκεύω την τιμή για τον άξονα y
            cancel_letter = self.canvas.itemcget(self.rects[cancel_tags][1], "text") #Αποθηκεύω το γράμμα που ήταν τοποθετημένο στο κελί του ταμπλό που έγινε η ανάιρεση
            self.player.used_letters.pop() #Αφαιρώ το γράμμα από την λίστα που κρατάει τα γράμματα που χρησιμοποιεί ο χρήστης στον τρέχον γύρο
            self.rects_list[cancel_x][cancel_y] = " " #Αντικαθιστώ το γράμμα με " "(κενό) στην λίστα που υπάρχει για την προσπέλαση των γραμμάτων

            #Με επανάληψη κάνω προσπέλαση των 7 κελιών με τα γράμματα του χρήστη
            for i in range(7):
                if self.player_tiles[f"{i}"][2]: #Σε περίπτωση που το κελί είναι άδειο(δεν περιέχει γράμμα)
                    self.player.hands_letters[i] = cancel_letter #Τοποθετώ στην "κενή" θέση στην λίστα για τα γράμματα του χρήστη το γράμμα που έγινε αναίρεση
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i]) #Τοποθετώ το γράμμα και στο ανάλογο κενό κελί του καμβά
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color) #Αλλάζω το χρώμα του κελιού στον καμβά από μαύρο σε άσπρο 
                    self.player_tiles[f"{i}"][2] = False #Βάζω την τιμή False, αφού πλέον το κελί δεν είναι πλέον χωρίς λέξη
                    break #Σπάω την επανάληψη αφού βρέθηκε κενή θέση για το γράμμα
            
            #Χρησιμοποιώ το module special_tiles για αμυντικό έλεγχο, ώστε να γίνει η αντίστοιχη σχεδίαση στην επαναφορά της αρχικής κατάστασης του κελιού
            if special_tiles.triple_word(cancel_x, cancel_y): #Κελί για λέξη τριπλής αξίας
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="red") #Στο tile_rect επαναφέρω το ανάλογο χρώμα
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ") #Στο tile_txt επαναφέρω το κείμενο που είχε το ειδικό κελί
                self.rects[cancel_tags][2] = True #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
                self.rects[cancel_tags][3] = False #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
            elif special_tiles.triple_letter(cancel_x, cancel_y): #Κελί για γράμμα τριπλής αξίας
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="blue") #Στο tile_rect επαναφέρω το ανάλογο χρώμα
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ") #Στο tile_txt επαναφέρω το κείμενο που είχε το ειδικό κελί
                self.rects[cancel_tags][2] = True #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
                self.rects[cancel_tags][3] = False #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
            elif special_tiles.double_letter(cancel_x, cancel_y): #Κελί για γράμμα διπλής αξίας
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light blue") #Στο tile_rect επαναφέρω το ανάλογο χρώμα
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ") #Στο tile_txt επαναφέρω το κείμενο που είχε το ειδικό κελί
                self.rects[cancel_tags][2] = True #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
                self.rects[cancel_tags][3] = False #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
            elif special_tiles.double_word(cancel_x,cancel_y): #Κελί για λέξη διπλής αξίας
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light pink") #Στο tile_rect επαναφέρω το ανάλογο χρώμα
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ") #Στο tile_txt επαναφέρω το κείμενο που είχε το ειδικό κελί
                self.rects[cancel_tags][2] = True #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
                self.rects[cancel_tags][3] = False #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
            elif special_tiles.center(cancel_x, cancel_y): #Κεντρικό κελί
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light pink") #Στο tile_rect επαναφέρω το ανάλογο χρώμα
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="ΑΡΧΗ") #Στο tile_txt επαναφέρω το κείμενο που είχε το ειδικό κελί
                self.rects[cancel_tags][2] = True #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
                self.rects[cancel_tags][3] = False #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
            else:
                #Κλασικά κελιά του ταμπλό
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fil="green") #Στο tile_rect επαναφέρω το ανάλογο χρώμα
                self.canvas.itemconfigure(self.rects[cancel_tags][1], anchor='center', text="") #Στο tile_txt επαναφέρω το "" στο κείμενο που είχε το κλασικό κελί
                self.rects[cancel_tags][2] = True #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
                self.rects[cancel_tags][3] = False #Επαναφέρω την τιμή στην αρχική κατάσταση μετά την αναίρεση
            

    #Μέθοδος για επιστροφή γράμματος του παίκτη στην κληρωτίδα και αντικατάστασή του με ένα καινούργιο γράμμα
    def switch_letter(self):
        if self.transfer and self.turn == 1: #Έλεγχος για το αν έχει επιλεγεί γράμμα και αν είναι ο γύρος που παίζει ο χρήστης
            if self.player.letter_switch < 3: #Eλέγχω αν έχει ξεπεραστεί το επιτρεπόμενο όριο αντικατάστασης γραμμάτων
                self.transfer_letter_temp = self.canvas.itemcget(self.player_tiles[self.tags1][1], "text")
                self.player.hands_letters[int(self.tags1)] = self.bag.pick_letter()
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= self.player.hands_letters[int(self.tags1)])
                self.bag.letters_bag.append(self.transfer_letter_temp)
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], fill = self.transfer_color) #Το επιλεγμένο κελί που ήταν κίτρινο, ξανά γίνεται άσπρο αφού δεν είναι επιλεγμένο πλέον
                self.transfer = False #Αλλάζω την τιμή σε False αφού πλέον τελείωσε η διαδικασία αντικατάστασης του γράμματος
                self.player.letter_switch += 1 #Αυξάνω την τιμή κατά 1
            else: #Σε περίπτωση που έχει ξεπεραστεί το όριο
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], fill = self.transfer_color) #Το επιλεγμένο κελί που ήταν κίτρινο, ξανά γίνεται άσπρο αφού δεν είναι επιλεγμένο πλέον
                self.transfer = False #Αλλάζω την τιμή σε False αφού ακυρώθηκε η διαδικασία αντικατάστασης του γράμματος
                messagebox.showinfo(title=None, message= "Μέχρι 3 φορές επιτρέπεται να αντικαταστήσεις ένα γράμμα!") #Μήνυμα προς τον χρήστη ότι πλέον δεν μπορεί να αντικαταστήσει άλλα γράμματα
    
    #Μέθοδος για να τερματίσει το παιχνίδι που παίζει ο χρήστης
    def end_current_game(self):
        self.destroy() #Καταστρέφω το παράθυρο
        from intro_page import IntroPage #Κάνω import την intro_page
        intro = IntroPage() #Δημιουργώ αντικείμενο της κλάσης IntroPage
        intro.mainloop() #Εμφανίζω τα γραφικά της αρχικής σελίδας όπου έπιστρέφει ο χρήστης

    #Μέθοδος για τον υπολογισμό των πόντων κάθε λέξης
    def calculate_points(self):
        word_multiplier = 1 #Η μεταβλητή ξεκινάει με την τιμή 1 αλλά τροποποιείται στις περιπτώσεις που η λέξη έχει διπλάσια ή τριπλάσια αξία. 

        if self.player.x_axis: #Σε περίπτωση που η λέξη είναι οριζόντια
            pos = 0 #Μεταβλητή που θα χρησιμοποιηθεί ως δείκτης για την προσπέλαση των γραμμάτων 
            for letter in range(self.player.word_start, self.player.word_finish+1): #Παίρνω τις τιμές του άξονα στον οποίο κινείται η λέξη
                #Χρησιμοποιώ το module special_tiles για να ελέγξω αν το γράμμα είναι τοποθετημένο σε ειδικό κελί ή σε κλασικό
                if special_tiles.triple_word(self.player.word_axis, letter): #Σε περίπτωση που το κελί είναι για λέξη τριπλής αξίας
                    word_multiplier = 3 #Αλλάζω την τιμή του πολλαπλασιαστή λέξης σε 3
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]] #Παίρνω την αξία του γράμματος και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                elif special_tiles.double_word(self.player.word_axis, letter): #Σε περίπτωση που το κελί είναι για λέξη διπλής αξίας
                    word_multiplier = 2 #Αλλάζω την τιμή του πολλαπλασιαστή λέξης σε 2
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]] #Παίρνω την αξία του γράμματος και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                elif special_tiles.triple_letter(self.player.word_axis, letter): #Σε περίπτωση που το κελί είναι για γράμμα τριπλής αξίας
                    #Παίρνω την αξία του γράμματος, την πολλαπλασιάζω με το 3 και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 3) 
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                elif special_tiles.double_letter(self.player.word_axis, letter): #Σε περίπτωση που το κελί είναι για γράμμα διπλής αξίας
                    #Παίρνω την αξία του γράμματος, την πολλαπλασιάζω με το 2 και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 2) 
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                else: #Σε περίπτωση που το κελί είναι κλασικό
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]] #Παίρνω την αξία του γράμματος και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    pos += 1 #Αυξάνω τον δείκτη κατά 1

            #Χρησιμοποιώ τον πολλαπλασιαστή στο σκορ της τρέχουσας λέξης και την προσθέτω στην λίστα για τους πόντους που θα πάρει ο χρήστης
            #αν αποδειχτεί η εγκυρότητα της λέξης(ή των λέξεων)
            self.player.potential_points.append(self.player.current_word_score * word_multiplier) 
            self.player.current_word_score = 0 #Προετοιμάζω την μεταβλητή για την επόμενη λέξη

        else: #Σε περίπτωση που η λέξη είναι κάθετη
            pos = 0 #Μεταβλητή που θα χρησιμοποιηθεί για την προσπέλαση των γραμμάτων 
            for letter in range(self.player.word_start, self.player.word_finish+1): #Παίρνω τις τιμές του άξονα στον οποίο κινείται η λέξη
                #Χρησιμοποιώ το module special_tiles για να ελέγξω αν το γράμμα είναι τοποθετημένο σε ειδικό κελί ή σε κλασικό
                if special_tiles.triple_word(letter, self.player.word_axis): #Σε περίπτωση που το κελί είναι για λέξη τριπλής αξίας
                    word_multiplier = 3 #Αλλάζω την τιμή του πολλαπλασιαστή λέξης σε 3
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]] #Παίρνω την αξία του γράμματος και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                elif special_tiles.double_word(letter, self.player.word_axis): #Σε περίπτωση που το κελί είναι για λέξη διπλής αξίας
                    word_multiplier = 2 #Αλλάζω την τιμή του πολλαπλασιαστή λέξης σε 2
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]] #Παίρνω την αξία του γράμματος και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                elif special_tiles.triple_letter(letter, self.player.word_axis): #Σε περίπτωση που το κελί είναι για γράμμα τριπλής αξίας
                    #Παίρνω την αξία του γράμματος, την πολλαπλασιάζω με το 3 και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 3) 
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                elif special_tiles.double_letter(letter, self.player.word_axis): #Σε περίπτωση που το κελί είναι για γράμμα διπλής αξίας
                    #Παίρνω την αξία του γράμματος, την πολλαπλασιάζω με το 2 και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 2) 
                    pos += 1 #Αυξάνω τον δείκτη κατά 1
                else: #Σε περίπτωση που το κελί είναι κλασικό
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]] #Παίρνω την αξία του γράμματος και την προσθέτω στη μεταβλητή για το σκορ της τρέχουσας λέξης
                    pos += 1 #Αυξάνω τον δείκτη κατά 1

            #Χρησιμοποιώ τον πολλαπλασιαστή στο σκορ της τρέχουσας λέξης και την προσθέτω στην λίστα για τους πόντους που θα πάρει ο χρήστης
            #αν αποδειχτεί η εγκυρότητα της λέξης(ή των λέξεων)    
            self.player.potential_points.append(self.player.current_word_score * word_multiplier)
            self.player.current_word_score = 0 #Προετοιμάζω την μεταβλητή για την επόμενη λέξη

    #Με την μέθοδο αυτή επιστρέφονται τα γράμματα που τοποθέτησε ο χρήστης στον τρέχοντα γύρο
    #με το να αξιοποιώ την μέθοδο cancel_move που υπάρχει για την αναίρεση κίνησης
    def remove_word(self):
        if self.turn == 1: #Στην περίπτωση που παίζει ο χρήστης
            while len(self.player.coords_cancel) > 0: #Όσο η λίστα που έχω για να αναιρώ κινήσεις, έχει στοιχεία μέσα της
                self.cancel_move() #Τότε καλώ την cancel_move για να επιστραφεί γράμμα που είναι τοποθετημένο στο ταμπλό στα χέρια του χρήστη
            
            self.player.reset_values() #Επαναφέρω τις μεταβλητές στις αρχικές τους τιμές

    #Μέθοδος main
    def main(self):
        #Ελέγχω αν το παιχνίδι είναι στον πρώτο γύρο, ώστε γνωρίζω αν θα μοιράσω τα πρώτα 7 γράμματα στον χρήστη και στον υπολογιστή
        # ή αν χρειάζεται να αναπληρώσω τα γράμματα που χρησιμοποιήθηκαν.
        if self.first_round: #Στη περίπτωση που είναι ο πρώτος γύρος
            for i in range(7): #Με επανάληψη κάνω προσπέλαση των 7 θέσεων για τα γράμματα του χρήστη και του υπολογιστή
                self.computer.hands_letters.append(self.bag.pick_letter()) #Δίνω γράμμα από την κληρωτίδα στην λίστα γραμμάτων του υπολογιστή
                self.player.hands_letters.append(self.bag.pick_letter()) #Δίνω γράμμα από την κληρωτίδα στην λίστα γραμμάτων του χρήστη
                self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i]) #Τροποποιώ το αντίστοιχο κελί ώστε να πάρει το αντίστοιχο γράμμα
                self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color) #Αλλάζω το χρώμα σε άσπρο στο αντίστοιχο κελί, αφού πλέον περιέχει γράμμα
                self.player_tiles[f"{i}"][2] = False #Αλλάζω την τιμή σε False, αφού πλέον το αντίστοιχο κελί περιέχει γράμμα
                self.bag_letters_number.configure(text = f"{len(self.bag.letters_bag)}") #Ενημερώνω τον αριθμό που εμφανίζει το πλήθος γραμμάτων που απομένουν στην κληρωτίδα
        self.first_round = False #Μοίρασα τα πρώτα γράμματα, οπότε παίρνει την τιμή False
        
        if self.turn == 0: #Σε περίπτωση που έχει πάρει την τιμή 0, παίζει ο υπολογιστής
            self.turn = 1 #Αλλάζει η τιμή σε 1 για να παίξει στον επόμενο γύρο ο χρήστης
            self.main() #Καλώ την main
        else: #Αλλιώς σε περίπτωση που έχει πάρει την τιμή 1, παίζει ο χρήστης
            #Με επανάληψη κάνω προσπέλαση των 7 κελιών με τα γράμματα του χρήστη
            for i in range(len(self.player_tiles)):
                if self.player_tiles[f"{i}"][2]: #Σε περίπτωση που το κελί είναι άδειο(δεν περιέχει γράμμα)
                    self.player.hands_letters[i] = self.bag.pick_letter() #Δίνω νέο γράμμα από την κληρωτίδα στην "κενή" θέση της λίστας που βρέθηκε
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i])#Τοποθετώ στην "κενή" θέση στην λίστα για τα γράμματα του χρήστη το νέο γράμμα
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color) #Αλλάζω το χρώμα του κελιού στον καμβά από μαύρο σε άσπρο 
                    self.player_tiles[f"{i}"][2] = False #Βάζω την τιμή False, αφού πλέον το κελί δεν είναι πλέον χωρίς λέξη
                    self.bag_letters_number.configure(text = f"{len(self.bag.letters_bag)}") #Ενημερώνω τον αριθμό που εμφανίζει το πλήθος γραμμάτων που απομένουν στην κληρωτίδα