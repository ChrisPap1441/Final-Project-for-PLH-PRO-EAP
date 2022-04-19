import sys
sys.dont_write_bytecode = True #gia na min dimiourgite se kathe ektelesi o fakelos pycache
import random
import tkinter as tk
from PIL import ImageTk , Image
from letters_bag import Letters_bag
from word_check import Word_check
from player import Player


class Board(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bag = Letters_bag()
        self.check = Word_check()
        self.computer = Player()
        self.player = Player()

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
                if ((x==0 and y == 0) or (x==0 and y == 7) or (x==0 and y == 14) or (x==7 and y == 0) or (x==7 and y == 14) or (x==14 and y == 0) or (x==14 and y == 7) or (x==14 and y == 14)):
                    #keli gia leksi triplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="red", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif((x==1 and y == 5) or (x==1 and y == 9) or (x==5 and y == 1) or (x==5 and y == 5) or (x==5 and y == 9) or (x==5 and y == 13) or (x==9 and y == 1) or (x==9 and y == 5)
                    or (x==9 and y == 9) or (x==9 and y == 13) or (x==13 and y == 5) or (x==13 and y == 9)):
                    #keli gia gramma triplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif((x==0 and y == 3) or (x==0 and y == 11) or (x==2 and y == 6) or (x==2 and y == 8) or (x==3 and y == 0) or (x==3 and y == 7) or (x==3 and y == 14) or (x==6 and y == 2)
                    or (x==6 and y == 6) or (x==6 and y == 8) or (x==6 and y == 12) or (x==7 and y == 3) or (x==7 and y == 11) or (x==8 and y == 2) or (x==8 and y == 6) or (x==8 and y == 8) or (x==8 and y == 12)
                    or (x==11 and y == 0) or (x==11 and y == 7) or (x==11 and y == 14) or (x==12 and y == 6) or (x==12 and y == 8) or (x==14 and y == 3) or (x==14 and y == 11)):
                    #keli gia gramma diplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light blue", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif((x==1 and y == 1) or (x==1 and y == 13) or (x==2 and y == 2) or (x==2 and y == 12) or (x==3 and y == 3) or (x==3 and y == 11) or (x==4 and y == 4) or (x==4 and y == 10)
                    or (x==10 and y == 4) or (x==10 and y == 10) or (x==11 and y == 3) or (x==11 and y == 11) or (x==12 and y == 2) or (x==12 and y == 12) or (x==13 and y == 1) or (x==13 and y == 13) ):
                    #keli gia leksi diplis aksias
                    tile_rect = self.canvas.create_rectangle(self.x1, self.y1, self.height, self.width, fill="light pink", tags= f"{x},{y}")
                    tile_txt = self.canvas.create_text((self.x1 + self.height)/ 2, (self.y1 + self.width)/2, anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ", tags= f"{x},{y}")
                elif(x==7 and y == 7):
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

        #main
        self.turn = random.randint(0, 1) #klirosi gia to poios tha paiksei protos
        while True:
            if self.first_round:
                for i in range(7):
                    self.computer.hands_letters.append(self.bag.pick_letter())
                    self.player.hands_letters.append(self.bag.pick_letter())
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][1], anchor='center', text= self.player.hands_letters[i])
                    self.canvas.itemconfigure(self.player_tiles[f"{i}"][0], outline = "black", fill= self.transfer_color)
                    self.player_tiles[f"{i}"][2] = False
            self.first_round == False
            break
            
            # if self.turn == 0:
            #     #paizei o upologistis
            #     self.turn = 1
            # else:
            #     #paizei o xristis
            #     self.turn = 0

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
            elif self.tags2 in self.rects and self.rects[self.tags2][2]:
                self.canvas.itemconfigure(self.rects[self.tags2][1], font=("Arial", 35), anchor='center', text= self.transfer_letter)
                self.canvas.itemconfigure(self.rects[self.tags2][0], fill= self.transfer_color )
                self.canvas.itemconfigure(self.player_tiles[self.tags1][0], outline = "white", fill = "black")
                self.canvas.itemconfigure(self.player_tiles[self.tags1][1], text= "")
                self.player_tiles[self.tags1][2] = True
                self.rects[self.tags2][2] = False
                self.transfer = False



    #methodos gia ton elegxo tis leksis tou xristi
    def check_word(self):
        self.player.prepare_coords()
        self.player.validate_coords()
        if self.player.first_check:
            #analoga me to an i leksi einai orizontia i katheti, tsekaroume ta diplana kelia gia na exoume tin olokliromeni leksi
            if self.y_axis:
                while self.player.word_start != -1:
                    if self.rects[f"{self.player.word_axis},{self.player.word_start - 1}"][2] == False:
                        self.player.word_start -=1
                    else:
                        break

                while self.player.word_start != 15:
                    if self.rects[f"{self.player.word_axis},{self.player.word_start + 1}"][2] == False:
                        self.player.word_start +=1
                    else:
                        break

                #dimiourgoume tin leksi tou xristi
                for letter in range(self.word_start, self.word_finish+1):
                    self.word_letters.append(self.rects_list[letter][self.word_axis])
            else:
                #elegxoume se periptosi pou i leksi einai orizontia
                while self.player.word_start != -1:
                    if self.rects[f"{self.player.word_start - 1},{self.player.word_axis}"][2] == False:
                        self.player.word_start -=1
                    else:
                        break

                while self.player.word_start != 15:
                    if self.rects[f"{self.player.word_start + 1},{self.player.word_axis}"][2] == False:
                        self.player.word_start +=1
                    else:
                        break

                #dimiourgoume tin leksi tou xristi
                for letter in range(self.word_start, self.word_finish+1):
                    self.player.word_letters.append(self.rects_list[self.word_axis][letter])

            if self.rects["7,7"][2] == False:
                self.player.word = "".join(self.player.word_letters)
                if self.check.check_for_valid_word(self.player.word):
                    pass
            else:
                self.player.reset_values()
        else:
            self.player.reset_values()
        
        


        
if __name__ == "__main__":
    board = Board()
    board.mainloop()