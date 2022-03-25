from textwrap import fill
from tkinter import *
from turtle import left

class Board(Tk):
    def __init__(self):
        super().__init__()

        self.title("Scrabble")
        self.geometry("1520x980")
        self.configure(background="lightgrey")
        self.canvas = Canvas(self, width=800, height=910, highlightthickness = 0, background= "lightgrey")
        self.canvas.pack(side = "left", fill= BOTH)

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
                self.rects_list[x].append("")
                

            self.x1= 0
            self.height= 50

        #leksiko gia ta kelia tou paikti
        self.player_letters = {}
        
        #metavlites gia tis suntetagmenes dimiourgias ton kelion tou paikti
        self.p_x1 = 250
        self.p_y1 = 850
        self.p_height = 300
        self.p_width = 900

        #prosorinos pinakas me grammata tou paikti gia dokimes 
        test_let = ["Ε", "Χ", "Τ", "Π", "Ε", "Ο", "Υ"]

        #dimiourgia kelion gia ta grammata tou xristi
        for i in range(7):
            player_tile_rect = self.canvas.create_rectangle(self.p_x1, self.p_y1, self.p_height, self.p_width, outline = "black", fill="white", tags= f"{i}")
            player_tile_txt = self.canvas.create_text((self.p_x1 + self.p_height)/ 2, (self.p_y1 + self.p_width)/2, anchor='center', text=f"{test_let[i]}", tags= f"{i}")
            player_tile_empty = False
            self.player_letters[f"{i}"] = [player_tile_rect, player_tile_txt, player_tile_empty]
            self.p_x1 += 50
            self.p_height += 50


        self.canvas.bind('<Button-1>', self.on_click)
        
    #methodos gia tin metafora tou grammatos meso tou pontikiou tou xristi
    def on_click(self, event):
        
        if self.transfer == False:
            item1 = self.canvas.find_closest(event.x, event.y)
            self.tags1 = self.canvas.itemcget(item1, "tags").replace(" current", "")
            if self.tags1 in self.player_letters and self.player_letters[self.tags1][2] == False:
                self.transfer_letter = self.canvas.itemcget(self.player_letters[self.tags1][1], "text")
                self.canvas.itemconfigure(self.player_letters[self.tags1][0], fill = "yellow")
                self.transfer = True
        else:
            item2 = self.canvas.find_closest(event.x, event.y)
            self.tags2 = self.canvas.itemcget(item2, "tags").replace(" current", "")
            #se periptosi pou o xristis thelei na allaksei seira sta grammata tou
            if self.tags2 in self.player_letters and self.player_letters[self.tags2][2] == False:
                self.transfer_letter_temp = self.canvas.itemcget(self.player_letters[self.tags2][1], "text")
                self.canvas.itemconfigure(self.player_letters[self.tags2][1], text= self.transfer_letter)
                self.canvas.itemconfigure(self.player_letters[self.tags1][1], text= self.transfer_letter_temp)
                self.canvas.itemconfigure(self.player_letters[self.tags1][0], fill = self.transfer_color)
                self.transfer = False
            #se periptosi pou o xristis thelei na topothetisi gramma se keno keli sta grammata tou
            elif self.tags2 in self.player_letters and self.player_letters[self.tags2][2] == True:
                self.transfer_letter_temp = self.canvas.itemcget(self.player_letters[self.tags2][1], "text")
                self.canvas.itemconfigure(self.player_letters[self.tags2][1], text= self.transfer_letter)
                self.canvas.itemconfigure(self.player_letters[self.tags2][0], outline = "black", fill = self.transfer_color)
                self.canvas.itemconfigure(self.player_letters[self.tags1][1], text= self.transfer_letter_temp)
                self.canvas.itemconfigure(self.player_letters[self.tags1][0], outline = "white", fill = "black")
                self.player_letters[self.tags2][2] = False
                self.player_letters[self.tags1][2] = True
                self.transfer = False
            #se periptosi pou o xristis thelei na eisagei gramma sto board
            elif self.tags2 in self.rects and self.rects[self.tags2][2] == True:
                self.canvas.itemconfigure(self.rects[self.tags2][1], font=("Arial", 35), anchor='center', text= self.transfer_letter)
                self.canvas.itemconfigure(self.rects[self.tags2][0], fill= self.transfer_color )
                self.canvas.itemconfigure(self.player_letters[self.tags1][0], outline = "white", fill = "black")
                self.canvas.itemconfigure(self.player_letters[self.tags1][1], text= "")
                self.player_letters[self.tags1][2] = True
                self.rects[self.tags2][2] = False
                self.transfer = False
            #se periptosi pou xristis patisei allou(work in progress)
            else:
                self.canvas.itemconfigure(self.player_letters[self.tags1][0], fill = self.transfer_color)
                self.transfer = False

        
if __name__ == "__main__":
    board = Board()
    board.mainloop()