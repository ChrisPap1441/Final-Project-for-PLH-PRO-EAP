from textwrap import fill
from tkinter import *

board = Tk()
board.title("Scrabble")
board.geometry("1520x980")
board.configure(background="lightgrey")
canvas = Canvas(board, width=1920, height=1080)
canvas.pack()

rects = {}

x1 = 0 
y1 = 0
height = 50 
width = 50

for x in range(15):
    y1+=50
    width += 50
    for y in range(15):
        x1+=50
        height += 50
        if ((x==0 and y == 0) or (x==0 and y == 7) or (x==0 and y == 14) or (x==7 and y == 0) or (x==7 and y == 14) or (x==14 and y == 0) or (x==14 and y == 7) or (x==14 and y == 14)):
            #keli gia leksi triplis aksias
            tile_rect = canvas.create_rectangle(x1, y1, height, width, fill="red")
            tile_txt = canvas.create_text((x1 + height)/ 2, (y1 + width)/2, anchor='center', text="   ΛΕΞΗ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ")
        elif((x==1 and y == 5) or (x==1 and y == 9) or (x==5 and y == 1) or (x==5 and y == 5) or (x==5 and y == 9) or (x==5 and y == 13) or (x==9 and y == 1) or (x==9 and y == 5)
            or (x==9 and y == 9) or (x==9 and y == 13) or (x==13 and y == 5) or (x==13 and y == 9)):
            #keli gia gramma triplis aksias
            tile_rect = canvas.create_rectangle(x1, y1, height, width, fill="blue")
            tile_txt = canvas.create_text((x1 + height)/ 2, (y1 + width)/2, anchor='center', text="ΓΡΑΜΜΑ\nΤΡΙΠΛΗΣ\n   ΑΞΙΑΣ")
        elif((x==0 and y == 3) or (x==0 and y == 11) or (x==2 and y == 6) or (x==2 and y == 8) or (x==3 and y == 0) or (x==3 and y == 7) or (x==3 and y == 14) or (x==6 and y == 2)
            or (x==6 and y == 6) or (x==6 and y == 8) or (x==6 and y == 12) or (x==7 and y == 3) or (x==7 and y == 11) or (x==8 and y == 2) or (x==8 and y == 6) or (x==8 and y == 8) or (x==8 and y == 12)
            or (x==11 and y == 0) or (x==11 and y == 7) or (x==11 and y == 14) or (x==12 and y == 6) or (x==12 and y == 8) or (x==14 and y == 3) or (x==14 and y == 11)):
            #keli gia gramma diplis aksias
            tile_rect = canvas.create_rectangle(x1, y1, height, width, fill="light blue")
            tile_txt = canvas.create_text((x1 + height)/ 2, (y1 + width)/2, anchor='center', text="ΓΡΑΜΜΑ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ")
        elif((x==1 and y == 1) or (x==1 and y == 13) or (x==2 and y == 2) or (x==2 and y == 12) or (x==3 and y == 3) or (x==3 and y == 11) or (x==4 and y == 4) or (x==4 and y == 10)
            or (x==10 and y == 4) or (x==10 and y == 10) or (x==11 and y == 3) or (x==11 and y == 11) or (x==12 and y == 2) or (x==12 and y == 12) or (x==13 and y == 1) or (x==13 and y == 13) ):
            #keli gia leksi diplis aksias
            tile_rect = canvas.create_rectangle(x1, y1, height, width, fill="light pink")
            tile_txt = canvas.create_text((x1 + height)/ 2, (y1 + width)/2, anchor='center', text="   ΛΕΞΗ\n ΔΙΠΛΗΣ\n   ΑΞΙΑΣ")
        elif(x==7 and y == 7):
            #kentriko keli
            tile_rect = canvas.create_rectangle(x1, y1, height, width, fill="light pink")
            tile_txt = canvas.create_text((x1 + height)/ 2, (y1 + width)/2, anchor='center', text="ΑΡΧΗ")
        else:
            #ta upoloipa klasika kelia
            tile_rect = canvas.create_rectangle(x1, y1, height, width, fil="green")
            tile_txt = canvas.create_text((x1 + height)/ 2, (y1 + width)/2, anchor='center', text="")
        rects[(x,y)] = [tile_rect, tile_txt]
        print(x1, y1, height, width)

    x1= 0
    height= 50

#dokimi gia pithani proseggisi tropopoiisis xromatos kai keimenou sto canvas/keli
#canvas.itemconfigure(rects[(1,1)][1],font=("Arial", 35), anchor='center', text=S)
#canvas.itemconfigure(rects[(1,1)][0], fill="white")

player_letters = {}
p_x1 = 250
p_y1 = 850
p_height = 300
p_width = 900

test_let = ["Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η"]

for i in range(7):
    player_tile_rect = canvas.create_rectangle(p_x1, p_y1, p_height, p_width, fill="white")
    player_tile_txt = canvas.create_text((p_x1 + p_height)/ 2, (p_y1 + p_width)/2, anchor='center', text=f"{test_let[i]}")
    player_letters[i] = [player_tile_rect, player_tile_txt]
    p_x1 += 50
    p_height += 50

board.mainloop()