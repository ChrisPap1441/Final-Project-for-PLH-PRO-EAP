import sys
sys.dont_write_bytecode = True #gia na min dimiourgite se kathe ektelesi o fakelos pycache
import tkinter as tk
from PIL import ImageTk , Image


class IntroPage(tk.Tk):
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

        def start_game():
            self.destroy()
            from board import Board
            board = Board()
            board.mainloop()

        def show_buttons_info():
            self.destroy()
            from buttons_info import Info
            button_info = Info()
            button_info.mainloop()

        def game_rules():
            self.destroy()
            from game_rules import Rules
            rules_info = Rules()
            rules_info.mainloop()

        #----------Buttons--------------#
        new_game = tk.Button(self, text="Νέο Παιχνίδι", command=start_game)
        new_game.place(x = 700, y = 550)
        controls_button = tk.Button(self, text="Κουμπιά Παιχνιδιού", command=show_buttons_info)
        controls_button.place(x = 680, y = 600)
        game_rules_button = tk.Button(self, text="Κανόνες Παιχνιδιού", command=game_rules)
        game_rules_button.place(x = 681, y = 650)
        exit_button = tk.Button(self, text="Έξοδος", command=self.destroy)
        exit_button.place(x = 715, y = 700)


if __name__ == "__main__":
    intro = IntroPage()
    intro.mainloop()