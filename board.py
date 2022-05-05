import sys
sys.dont_write_bytecode = True #gia na min dimiourgite se kathe ektelesi o fakelos pycache
import random
import tkinter as tk
from PIL import ImageTk , Image
from letters_bag import Letters_bag
from word_check import Word_check
from player import Player
import special_tiles

class Board(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bag = Letters_bag()
        self.check = Word_check()
        self.computer = Player()
        self.player = Player()

        #------------window------------------#
        self.title("Scrabble")
        self.geometry("1520x980")
        self.configure(background="lightgrey")
        #-------------Canvas-----------------#
        self.canvas = tk.Canvas(self, width=800, height=910, highlightthickness = 0, background= "lightgrey")
        self.canvas.place(x=0, y= 0)
        #-----------Scrabble logo------------#
        self.logo_image = Image.open("Scrabble.png")
        self.resized_logo = self.logo_image.resize((300, 125), Image.Resampling.LANCZOS)
        self.new_logo = ImageTk.PhotoImage(self.resized_logo)
        self.logo = tk.Label(self, background= "lightgrey", image = self.new_logo, width= 500, height = 100)
        self.logo.place(x= 950, y = 50)
        #-----------Computer & Player Scores--------#
        self.highscore = tk.Label(self, background= "lightgrey", text = "SCORE", font= 55)
        self.highscore.place(x = 920, y =250)
        self.computer_score = tk.Label(self, background= "lightgrey", text = "Computer:", font= 55)
        self.computer_score.place(x = 900, y =280)
        self.computer_score_number = tk.Label(self, background= "white", borderwidth = 2, relief = "solid", text = f"{self.computer.highscore}", font= 55)
        self.computer_score_number.place(x = 1000, y =280)
        self.player_score = tk.Label(self, background= "lightgrey", text = "Player:", font= 55)
        self.player_score.place(x = 900, y =300)
        self.player_score_number = tk.Label(self, background= "white", borderwidth = 2, relief = "solid", text = f"{self.player.highscore}", font= 55)
        self.player_score_number.place(x = 1000, y =300)
        #----------Letter's Bag--------------#
        self.bag_image = Image.open("bag-of-tiles.png")
        self.resized_bag = self.bag_image.resize((200, 200), Image.Resampling.LANCZOS)
        self.new_bag = ImageTk.PhotoImage(self.resized_bag)
        self.final_bag = tk.Label(self, background= "lightgrey", image = self.new_bag, width= 200, height = 200)
        self.final_bag.place(x= 1200, y = 220)
        self.bag_letters_number = tk.Label(self, background= "white", borderwidth = 2, relief = "solid", text = f"{len(self.bag.letters_bag)}", font= 55)
        self.bag_letters_number.place(x = 1280, y =290)
        #----------Buttons--------------#
        check_word_button = tk.Button(self, text="Έλεγχος λέξης", command=self.check_word)
        check_word_button.place(x = 900, y = 500)
        discard_button = tk.Button(self, text="Πέταξε 1 γράμμα", command=self.discard_letter)
        discard_button.place(x = 900, y = 550)
        refund_button = tk.Button(self, text="Αναίρεση κίνησης", command=self.cancel_move)
        refund_button.place(x = 900, y = 600)
        pass_button = tk.Button(self, text="Πάσο", command=self.pass_round)
        pass_button.place(x = 900, y = 650)
        end_game_button = tk.Button(self, text="Τερματισμός παιχνιδιού", command=self.end_current_game)
        end_game_button.place(x = 900, y = 700)
        exit_button = tk.Button(self, text="Κλείσιμο της εφαρμογής", command=self.destroy)
        exit_button.place(x = 1300, y = 900)
        #-----------Letter's Points---------------#
        letters_points = tk.Label(self, background= "lightgrey", width=30, borderwidth = 2, relief = "solid", text = "ΠΟΝΤΟΙ\nΑ = 1        Ν = 1\nΒ = 8        Ξ = 10\nΓ = 4        Ο = 1\nΔ = 4        Π = 2\nΕ = 1        Ρ = 2\nΖ = 10        Τ = 1\nΗ = 1        Σ = 1\nΘ = 4        Υ = 2\nΙ = 1        Φ = 8\nΚ = 2        Χ = 8\nΛ = 3        Ψ = 10\nΜ = 3        Ω = 3", font= 55)
        letters_points.place(x = 1170, y = 500)
        
        self.turn = None
        self.first_round = True
        
        #metavlites gia tin metakinisi grammaton(eite sto board, eite sta grammata tou xristi)
        self.tags1 = ""
        self.tags2 = ""
        self.transfer = False
        self.transfer_letter = ""
        self.transfer_letter_temp = ""
        self.transfer_color = "white"
        
        self.rects_list = []
        #leksiko gia ta kelia tou board
        self.rects = {}

        #metavlites gia tis suntetagmenes dimiourgias ton kelion tou board
        self.x1 = 0 
        self.y1 = 0
        self.height = 50 
        self.width = 50

        #dimiourgia ton kelion tou board kai kataxorisi auton sto analogo leksiko
        for x in range(15):
            self.y1+=50
            self.width += 50
            self.rects_list.append([])
            for y in range(15):
                self.x1+=50
                self.height += 50
                if special_tiles.triple_word(x, y):
                    #keli gia leksi triplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="red", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.triple_letter(x, y):
                    #keli gia gramma triplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.double_letter(x, y):
                    #keli gia gramma diplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.double_word(x,y):
                    #keli gia leksi diplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.center(x, y):
                    #kentriko keli
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="ΑΡΧΗ", tags= f"{x},{y}")
                else:
                    #ta upoloipa klasika kelia
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fil="green", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="", tags= f"{x},{y}")
                board_tile_empty = True
                self.rects[(f"{x},{y}")] = [tile_rect, tile_txt, board_tile_empty]
                self.rects_list[x].append(" ")
                

            self.x1= 0
            self.height= 50

        #leksiko gia ta kelia tou paikti
        self.player_tiles = {}
        
        #metavlites gia tis suntetagmenes dimiourgias ton kelion tou paikti
        self.p_x1 = 250
        self.p_y1 = 850
        self.p_height = 300
        self.p_width = 900

        #dimiourgia kelion gia ta grammata tou xristi
        for i in range(7):
            player_tile_rect = self.canvas.create_rectangle(self.p_x1, self.p_y1, self.p_height, self.p_width, outline = "white", fill="black", tags= f"{i}")
            player_tile_txt = self.canvas.create_text((self.p_x1 + self.p_height)/ 2, (self.p_y1 + self.p_width)/2, anchor='center', text= "", tags= f"{i}")
            player_tile_empty = True
            self.player_tiles[f"{i}"] = [player_tile_rect, player_tile_txt, player_tile_empty]
            self.p_x1 += 50
            self.p_height += 50
              
        self.canvas.bind('<Button-1>', self.on_click)
        
    #methodos gia tin metafora tou grammatos meso tou pontikiou tou xristi
    def on_click(self, event):
        
        if self.transfer == False:
            item1 = self.canvas.find_closest(event.x, event.y)
            self.tags1 = self.canvas.itemcget(item1, "tags").replace(" current", "")
            if self.tags1 in self.player_tiles and self.player_tiles[self.tags1][2] == False:
                self.transfer_letter = self.canvas.itemcget(self.player_tiles[self.tags1][1], "text")
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], fill = "yellow")
                self.transfer = True
        else:
            item2 = self.canvas.find_closest(event.x, event.y)
            self.tags2 = self.canvas.itemcget(item2, "tags").replace(" current", "")
            #se periptosi pou o xristis thelei na allaksei tin seira ton grammaton tou
            if self.tags2 in self.player_tiles and self.player_tiles[self.tags2][2] == False:
                self.transfer_letter_temp = self.canvas.itemcget(self.player_tiles[self.tags2][1], "text")
                self.canvas.itemconfigure(self.player_tiles[self.tags2][1], text= self.transfer_letter)
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= self.transfer_letter_temp)
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], fill = self.transfer_color)
                self.transfer = False
            #se periptosi pou o xristis thelei na topothetisi gramma se keno keli sta grammata tou
            elif self.tags2 in self.player_tiles and self.player_tiles[self.tags2][2] :
                self.transfer_letter_temp = self.canvas.itemcget(self.player_tiles[self.tags2][1], "text")
                self.canvas.itemconfigure(self.player_tiles[self.tags2][1], text= self.transfer_letter)
                self.canvas.itemconfigure(self.player_tiles[self.tags2][0], outline = "black", fill = self.transfer_color)
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= self.transfer_letter_temp)
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black")
                self.player_tiles[self.tags2][2] = False
                self.player_tiles[self.tags1][2] = True
                self.transfer = False
            #se periptosi pou o xristis thelei na eisagei gramma sto board
            elif self.tags2 in self.rects and self.rects[self.tags2][2] and self.turn == 1:
                self.canvas.itemconfigure(self.rects[self.tags2][1], font=("Arial", 35), anchor='center', text= self.transfer_letter)
                self.canvas.itemconfigure(self.rects[self.tags2][0], fill= self.transfer_color )
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black")
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= "")
                self.player_tiles[self.tags1][2] = True
                self.rects[self.tags2][2] = False
                self.transfer = False
                self.player.coords_cancel.append(self.tags2)
                coords = self.tags2.split(",")
                self.player.x_coords.append(int(coords[0]))
                self.player.y_coords.append(int(coords[1]))
                self.rects_list[int(coords[0])][int(coords[1])] = self.transfer_letter
                self.player.used_letters.append(self.transfer_letter)



    #methodos gia ton elegxo tis leksis tou xristi
    def check_word(self):
        self.player.prepare_coords()
        self.player.validate_coords()
        self.player.process_coords()
        if self.player.first_check:
            #analoga me to an i leksi einai orizontia i katheti, tsekaroume ta diplana kelia gia na exoume tin olokliromeni leksi
            if self.player.y_axis:
                while self.player.word_start != 0:
                    if self.rects[f"{self.player.word_axis},{self.player.word_start - 1}"][2] == False:
                        self.player.word_start -=1
                    else:
                        break

                while self.player.word_finish != 14:
                    if self.rects[f"{self.player.word_axis},{self.player.word_finish + 1}"][2] == False:
                        self.player.word_finish +=1
                    else:
                        break

                #dimiourgoume tin leksi tou xristi
                for letter in range(self.player.word_start, self.player.word_finish+1):
                    self.player.word_letters.append(self.rects_list[letter][self.player.word_axis])
            else:
                #elegxoume se periptosi pou i leksi einai orizontia
                while self.player.word_start != 0:
                    if self.rects[f"{self.player.word_start - 1},{self.player.word_axis}"][2] == False:
                        self.player.word_start -=1
                    else:
                        break

                while self.player.word_finish != 14:
                    if self.rects[f"{self.player.word_finish + 1},{self.player.word_axis}"][2] == False:
                        self.player.word_finish +=1
                    else:
                        break
                
                #dimiourgoume tin leksi tou xristi
                for letter in range(self.player.word_start, self.player.word_finish+1):
                    self.player.word_letters.append(self.rects_list[self.player.word_axis][letter])

            if self.rects["7,7"][2] == False:
                self.player.word = "".join(self.player.word_letters)
                print(self.player.word)
                if self.check.check_for_valid_word(self.player.word):
                    self.calculate_points()
                    self.turn = 0
                else:
                    print("Word error")
                    self.remove_word()
            else:
                self.remove_word()
        else:
            self.remove_word()

    #methodos gia na paei passo o paiktis
    def pass_round(self):
        pass

    #methodos gia na kanei anairesi o paiktis
    def cancel_move(self):
        if len(self.player.coords_cancel) > 0:
            cancel_tags = self.player.coords_cancel.pop()
            cancel_coords = cancel_tags.split(",")
            cancel_x = int(cancel_coords[0])
            cancel_y = int(cancel_coords[1])
            cancel_letter = self.canvas.itemcget(self.rects[cancel_tags][1], "text")
            for i in range(7):
                if self.player_tiles[f"{i}"][2]:
                    self.player.hands_letters[i] = cancel_letter
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i])
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color)
                    self.player_tiles[f"{i}"][2] = False
                    break
            
            if special_tiles.triple_word(cancel_x, cancel_y):
                #keli gia leksi triplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="red")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("lucida ", 8), anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
            elif special_tiles.triple_letter(cancel_x, cancel_y):
                #keli gia gramma triplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="blue")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("lucida ", 8), anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
            elif special_tiles.double_letter(cancel_x, cancel_y):
                #keli gia gramma diplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light blue")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("lucida ", 8), anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
            elif special_tiles.double_word(cancel_x,cancel_y):
                #keli gia leksi diplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light pink")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("lucida ", 8), anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
            elif special_tiles.center(cancel_x, cancel_y):
                #kentriko keli
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light pink")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("lucida ", 8), anchor='center', text="ΑΡΧΗ")
                self.rects[cancel_tags][2] = True
            else:
                #ta upoloipa klasika kelia
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fil="green")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], anchor='center', text="")
                self.rects[cancel_tags][2] = True
            

    #methodos gia na petaksei ena gramma o paiktis
    def discard_letter(self):
        if self.transfer:
            self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black")
            self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= "")
            self.player_tiles[self.tags1][2] = True
            self.player.hands_letters[self.tags1] = ""
            self.transfer = False
    
    #methodos gia na teleiosei to paixnidi poy paizei o xristis
    def end_current_game(self):
        pass

    def calculate_points(self):
        word_multiplier = 1
        if self.player.x_axis:
            pos = 0
            for letter in range(self.player.word_start, self.player.word_finish+1):
                if special_tiles.triple_word(self.player.word_axis, letter):
                    word_multiplier = 3
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]]
                    pos += 1
                elif special_tiles.double_word(self.player.word_axis, letter):
                    word_multiplier = 2
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]]
                    pos += 1
                elif special_tiles.triple_letter(self.player.word_axis, letter):
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 3)
                    pos += 1
                elif special_tiles.double_letter(self.player.word_axis, letter):
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 2)
                    pos += 1
                else:
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]]
                    pos += 1
                
            self.player.highscore += (self.player.current_word_score * word_multiplier)
            self.player_score_number.configure(text = f"{self.player.highscore}")
            self.player.current_word_score = 0
        else:
            pos = 0
            for letter in range(self.player.word_start, self.player.word_finish+1):
                if special_tiles.triple_word(letter, self.player.word_axis):
                    word_multiplier = 3
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]]
                    pos += 1
                elif special_tiles.double_word(letter, self.player.word_axis):
                    word_multiplier = 2
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]]
                    pos += 1
                elif special_tiles.triple_letter(letter, self.player.word_axis):
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 3)
                    pos += 1
                elif special_tiles.double_letter(letter, self.player.word_axis):
                    self.player.current_word_score += (self.bag.letters_points[self.player.word_letters[pos]] * 2)
                    pos += 1
                else:
                    self.player.current_word_score += self.bag.letters_points[self.player.word_letters[pos]]
                    pos += 1
                
            self.player.highscore += (self.player.current_word_score * word_multiplier)
            self.player_score_number.configure(text = f"{self.player.highscore}")
            self.player.current_word_score = 0

    def remove_word(self):
        while len(self.player.coords_cancel) > 0:
            self.cancel_move()
        
        self.player.reset_values()




        
if __name__ == "__main__":
    board = Board()
    board.turn = random.randint(0, 1) #klirosi gia to poios tha paiksei protos
    while True:
        if board.first_round:
            for i in range(7):
                board.computer.hands_letters.append(board.bag.pick_letter())
                board.player.hands_letters.append(board.bag.pick_letter())
                board.canvas.itemconfigure(board.player_tiles[f"{i}"][1], anchor='center', text= board.player.hands_letters[i])
                board.canvas.itemconfigure(board.player_tiles[f"{i}"][0], outline = "black", fill= board.transfer_color)
                board.player_tiles[f"{i}"][2] = False
                board.bag_letters_number.configure(text = f"{len(board.bag.letters_bag)}")
        board.first_round == False
        
        if board.turn == 0:
            #paizei o upologistis
            board.turn = 1
        else:
            #paizei o xristis
            if len(board.player_tiles) < 7:
                for i in range(len(board.player_tiles)):
                    if board.player_tiles[f"{i}"][2]:
                        board.player.hands_letters[i] = board.bag.pick_letter()
                        board.canvas.itemconfigure(board.player_tiles[f"{i}"][1], anchor='center', text= board.player.hands_letters[i])
                        board.canvas.itemconfigure(board.player_tiles[f"{i}"][0], outline = "black", fill= board.transfer_color)
                        board.player_tiles[f"{i}"][2] = False
        
        board.mainloop()

        