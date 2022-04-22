from tkinter import *
from PIL import ImageTk , Image

window = Tk()
window.title("Scrabble")
window.geometry("1520x980")
window.configure(background="lightgrey")

#-----------Scrabble logo------------#
window.logo_image = Image.open("Scrabble.png")
window.resized_logo = window.logo_image.resize((500, 225), Image.Resampling.LANCZOS)
window.new_logo = ImageTk.PhotoImage(window.resized_logo)
window.logo = Label(window, background= "lightgrey", image = window.new_logo, width= 500, height = 225)
window.logo.place(x= 480, y = 150)

def start_game():
    window.destroy()
    import board.py

def show_buttons_info():
    pass

def game_rules():
    pass

#----------Buttons--------------#
new_game = Button(window, text="Νέο Παιχνίδι", command=start_game)
new_game.place(x = 700, y = 550)
controls_button = Button(window, text="Κουμπιά Παιχνιδιού", command=show_buttons_info)
controls_button.place(x = 680, y = 600)
game_rules_button = Button(window, text="Κανόνες Παιχνιδιού", command=game_rules)
game_rules_button.place(x = 681, y = 650)
exit_button = Button(window, text="Έξοδος", command=window.destroy)
exit_button.place(x = 715, y = 700)



window.mainloop()