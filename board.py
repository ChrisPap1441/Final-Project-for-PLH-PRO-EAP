import sys
sys.dont_write_bytecode = True #gia na min dimiourgite se kathe ektelesi o fakelos pycache
import random
import tkinter as tk
from PIL import ImageTk , Image
from letters_bag import Letters_bag
from word_check import Word_check
from player import Player
import special_tiles
from intro_page import IntroPage

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
        
        self.turn = random.randint(0, 1) #klirosi gia to poios tha paiksei protos
        self.first_round = True
        self.first_word = True
        
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
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.triple_letter(x, y):
                    #keli gia gramma triplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.double_letter(x, y):
                    #keli gia gramma diplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.double_word(x,y):
                    #keli gia leksi diplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif special_tiles.center(x, y):
                    #kentriko keli
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, font=("ariel", 9), anchor='center', text="ΑΡΧΗ", tags= f"{x},{y}")
                else:
                    #ta upoloipa klasika kelia
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fil="green", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="", tags= f"{x},{y}")
                board_tile_empty = True
                previous_round_letter = False
                self.rects[(f"{x},{y}")] = [tile_rect, tile_txt, board_tile_empty, previous_round_letter]
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
        
        self.main()
        #self.mainloop
        
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
                self.canvas.itemconfigure(self.rects[self.tags2][1], font=("ariel", 36), anchor='center', text= self.transfer_letter)
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
        if self.turn == 1:
            if len(self.player.x_coords) == 1 and len(self.player.y_coords) == 1:
                self.player.multi_words_x_coords =  self.player.x_coords.copy()
                self.player.multi_words_y_coords =  self.player.y_coords.copy()  

                if self.rects[f"{self.player.x_coords[0] + 1},{self.player.y_coords[0]}"][2] == False:
                    self.player.x_coords.append(self.player.x_coords[0] + 1)
                    self.player.y_coords.append(self.player.y_coords[0])
                elif self.rects[f"{self.player.x_coords[0] - 1},{self.player.y_coords[0]}"][2] == False:
                    self.player.x_coords.append(self.player.x_coords[0] - 1)
                    self.player.y_coords.append(self.player.y_coords[0])
                elif self.rects[f"{self.player.x_coords[0]},{self.player.y_coords[0] + 1}"][2] == False:
                    self.player.x_coords.append(self.player.x_coords[0])
                    self.player.y_coords.append(self.player.y_coords[0] + 1)
                elif self.rects[f"{self.player.x_coords[0]},{self.player.y_coords[0] - 1}"][2] == False:
                    self.player.x_coords.append(self.player.x_coords[0])
                    self.player.y_coords.append(self.player.y_coords[0] - 1)
            
                  
                self.player.prepare_coords()
                self.player.validate_coords()
                self.player.process_coords()
            else:
                self.player.prepare_coords()
                self.player.multi_words_x_coords =  self.player.x_coords.copy()
                self.player.multi_words_y_coords =  self.player.y_coords.copy()
                self.player.validate_coords()
                self.player.process_coords()


            if self.player.first_check:
                #analoga me to an i leksi einai orizontia i katheti, tsekaroume ta diplana kelia gia na exoume tin olokliromeni leksi
                if self.player.y_axis:
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
                        self.player.word_letters.append(self.rects_list[letter][self.player.word_axis])
                        self.player.previous_coords.append(f"{letter},{self.player.word_axis}")

                    self.player.word = "".join(self.player.word_letters)
                    self.player.words_to_check.append(self.player.word)
                    self.calculate_points()

                    if self.first_word == False:
                        self.player.word_letters.clear()
                        self.player.x_axis = True
                        self.player.y_axis = False
                        for i in range(len(self.player.multi_words_x_coords)):
                            if self.rects[f"{self.player.multi_words_x_coords[i]},{self.player.multi_words_y_coords[i] + 1}"][2] == False:
                                self.player.word_start = self.player.multi_words_y_coords[i]
                                self.player.word_finish = self.player.multi_words_y_coords[i] + 1
                                self.player.word_axis = self.player.multi_words_x_coords[i]
                            elif self.rects[f"{self.player.multi_words_x_coords[i]},{self.player.multi_words_y_coords[i] - 1}"][2] == False:
                                self.player.word_start = self.player.multi_words_y_coords[i] - 1
                                self.player.word_finish = self.player.multi_words_y_coords[i]
                                self.player.word_axis = self.player.multi_words_x_coords[i]
                            else:
                                self.player.word_start = self.player.multi_words_y_coords[i]
                                self.player.word_finish = self.player.multi_words_y_coords[i]
                                self.player.word_axis = self.player.multi_words_x_coords[i]

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
                                self.player.word_letters.append(self.rects_list[self.player.word_axis][letter])

                            self.player.word = "".join(self.player.word_letters)
                            if len(self.player.word_letters) > 1:
                                self.player.words_to_check.append(self.player.word)
                                self.calculate_points()
                            

                else:
                    #elegxoume se periptosi pou i leksi einai orizontia
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
                        self.player.word_letters.append(self.rects_list[self.player.word_axis][letter])
                        self.player.previous_coords.append(f"{self.player.word_axis},{letter}")

                    self.player.word = "".join(self.player.word_letters)
                    self.player.words_to_check.append(self.player.word)
                    self.calculate_points()
                    
                    if self.first_word == False:
                        self.player.word_letters.clear()
                        self.player.x_axis = False
                        self.player.y_axis = True
                        for i in range(len(self.player.multi_words_x_coords)):
                            if self.rects[f"{self.player.multi_words_x_coords[i] + 1},{self.player.multi_words_y_coords[i]}"][2] == False:
                                self.player.word_start = self.player.multi_words_x_coords[i]
                                self.player.word_finish = self.player.multi_words_x_coords[i] + 1
                                self.player.word_axis = self.player.multi_words_y_coords[i]
                            elif self.rects[f"{self.player.multi_words_x_coords[i] - 1},{self.player.multi_words_y_coords[i]}"][2] == False:
                                self.player.word_start = self.player.multi_words_x_coords[i] - 1
                                self.player.word_finish = self.player.multi_words_x_coords[i]
                                self.player.word_axis = self.player.multi_words_y_coords[i]
                            else:
                                self.player.word_start = self.player.multi_words_x_coords[i]
                                self.player.word_finish = self.player.multi_words_x_coords[i]
                                self.player.word_axis = self.player.multi_words_y_coords[i]
                            
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
                                self.player.word_letters.append(self.rects_list[letter][self.player.word_axis])

                            self.player.word = "".join(self.player.word_letters)
                            if len(self.player.word_letters) > 1:
                                self.player.words_to_check.append(self.player.word)
                                self.calculate_points()
                            
                if self.rects["7,7"][2] == False and self.first_word:
                    if self.check.check_for_valid_word(self.player.words_to_check[0]):
                        self.player.add_points()
                        self.turn = 0
                        for i in range(len(self.player.coords_cancel)):
                            self.rects[self.player.coords_cancel[i]][3] = True
                        self.first_word = False
                        self.player_score_number.configure(text = f"{self.player.highscore}")
                        self.player.reset_values()
                        self.main()
                    else:
                        self.remove_word()
                elif self.first_word == False:
                    for letter in self.player.previous_coords:
                        if self.rects[letter][3]:
                            self.player.second_check = True
                            break
                    if self.player.second_check:
                        for word in self.player.words_to_check:
                            if self.check.check_for_valid_word(word) == False:
                                self.player.words_ready = False
                                break
                            if self.player.words_ready:
                                self.player.add_points()
                                self.turn = 0
                                for i in range(len(self.player.coords_cancel)):
                                    self.rects[self.player.coords_cancel[i]][3] = True
                                self.player_score_number.configure(text = f"{self.player.highscore}")
                                self.player.reset_values()
                                self.main()
                            else:
                                self.remove_word()
                    else:
                        self.remove_word()
                else:
                    self.remove_word()
            else:
                self.remove_word()

    #methodos gia na paei passo o paiktis
    def pass_round(self):
        if self.turn == 1:
            self.remove_word()
            self.turn = 0
            self.main()

    #methodos gia na kanei anairesi o paiktis
    def cancel_move(self):
        if len(self.player.coords_cancel) > 0 and self.turn == 1:
            cancel_tags = self.player.coords_cancel.pop()
            self.player.x_coords.pop()
            self.player.y_coords.pop()
            cancel_coords = cancel_tags.split(",")
            cancel_x = int(cancel_coords[0])
            cancel_y = int(cancel_coords[1])
            cancel_letter = self.canvas.itemcget(self.rects[cancel_tags][1], "text")
            self.player.used_letters.pop()
            self.rects_list[cancel_x][cancel_y] = " "

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
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
                self.rects[cancel_tags][3] = False
            elif special_tiles.triple_letter(cancel_x, cancel_y):
                #keli gia gramma triplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="blue")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
                self.rects[cancel_tags][3] = False
            elif special_tiles.double_letter(cancel_x, cancel_y):
                #keli gia gramma diplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light blue")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
                self.rects[cancel_tags][3] = False
            elif special_tiles.double_word(cancel_x,cancel_y):
                #keli gia leksi diplis aksias
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light pink")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ")
                self.rects[cancel_tags][2] = True
                self.rects[cancel_tags][3] = False
            elif special_tiles.center(cancel_x, cancel_y):
                #kentriko keli
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fill="light pink")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], font=("ariel", 9), anchor='center', text="ΑΡΧΗ")
                self.rects[cancel_tags][2] = True
                self.rects[cancel_tags][3] = False
            else:
                #ta upoloipa klasika kelia
                self.canvas.itemconfigure(self.rects[cancel_tags][0], fil="green")
                self.canvas.itemconfigure(self.rects[cancel_tags][1], anchor='center', text="")
                self.rects[cancel_tags][2] = True
                self.rects[cancel_tags][3] = False
            

    #methodos gia na petaksei ena gramma o paiktis
    def discard_letter(self):
        if self.transfer and self.turn == 1:
            self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black")
            self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= "")
            self.player_tiles[self.tags1][2] = True
            self.player.hands_letters[int(self.tags1)] = ""
            self.transfer = False
    
    #methodos gia na teleiosei to paixnidi poy paizei o xristis
    def end_current_game(self):
        self.destroy()
        intro = IntroPage()
        intro.mainloop()

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

            self.player.potential_points.append(self.player.current_word_score * word_multiplier)
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
                
            self.player.potential_points.append(self.player.current_word_score * word_multiplier)
            self.player.current_word_score = 0

    def remove_word(self):
        if self.turn == 1:
            while len(self.player.coords_cancel) > 0:
                self.cancel_move()
            
            self.player.reset_values()

    def main(self):
        if self.first_round:
            for i in range(7):
                self.computer.hands_letters.append(self.bag.pick_letter())
                self.player.hands_letters.append(self.bag.pick_letter())
                self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i])
                self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color)
                self.player_tiles[f"{i}"][2] = False
                self.bag_letters_number.configure(text = f"{len(self.bag.letters_bag)}")
        self.first_round = False
        
        if self.turn == 0:
            #paizei o upologistis
            self.turn = 1
            self.main()
        else:
            #paizei o xristis
            for i in range(len(self.player_tiles)):
                if self.player_tiles[f"{i}"][2]:
                    self.player.hands_letters[i] = self.bag.pick_letter()
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i])
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color)
                    self.player_tiles[f"{i}"][2] = False
                    self.bag_letters_number.configure(text = f"{len(self.bag.letters_bag)}")
        

if __name__ == "__main__":
    board = Board()
    board.mainloop()

        