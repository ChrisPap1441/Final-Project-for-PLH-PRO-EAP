from textwrap import fill
from tkinter import *

class Board(Tk):
    def __init__(self):
        super().__init__()

        self.title("Scrabble")
        self.geometry("1520x980")
        self.configure(background="lightgrey")
        self.canvas = Canvas(self, width=1920, height=1080)
        self.canvas.pack()
        self.transfer = False
        self.transfer_letter = ""

        self.rects = {}

        self.x1 = 0 
        self.y1 = 0
        self.height = 50 
        self.width = 50

        for x in range(15):
            self.y1+=50
            self.width += 50
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
                self.rects[(f"{x},{y}")] = [tile_rect, tile_txt]
                

            self.x1= 0
            self.height= 50

        self.player_letters = {}
        self.p_x1 = 250
        self.p_y1 = 850
        self.p_height = 300
        self.p_width = 900

        test_let = ["Ε", "Χ", "Τ", "Π", "Ε", "Ο", "Υ"]

        for i in range(7):
            player_tile_rect = self.canvas.create_rectangle(self.p_x1, self.p_y1, self.p_height, self.p_width, fill="white", tags= f"{i}")
            player_tile_txt = self.canvas.create_text((self.p_x1 + self.p_height)/ 2, (self.p_y1 + self.p_width)/2, anchor='center', text=f"{test_let[i]}", tags= f"{i}")
            self.player_letters[i] = [player_tile_rect, player_tile_txt]
            self.p_x1 += 50
            self.p_height += 50


        self.canvas.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        
        if self.transfer == False:
            item1 = self.canvas.find_closest(event.x, event.y)
            tags1 = self.canvas.itemcget(item1, "tags")
            print(tags1)
            if int(tags1[0]) in self.player_letters:
                tags1 = int(tags1.replace(" current", ""))
                color = self.canvas.itemcget(self.player_letters[tags1][0], "fill")
                print(color)
                self.transfer_letter = self.canvas.itemcget(self.player_letters[tags1][1], "text")
                self.transfer = True
        else:
            item2 = self.canvas.find_closest(event.x, event.y)
            tags2 = self.canvas.itemcget(item2, "tags")
            tags2 = tags2.replace(" current", "")
            print(tags2)
            if tags2 in self.rects:
                self.canvas.itemconfigure(self.rects[tags2][1], font=("Arial", 35), anchor='center', text= self.transfer_letter)
                self.canvas.itemconfigure(self.rects[tags2][0], fill= "white")
                self.transfer = False

if __name__ == "__main__":
    board = Board()
    board.mainloop()