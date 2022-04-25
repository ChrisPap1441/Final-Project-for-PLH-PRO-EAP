class Player:
    def __init__(self):
        self.highscore = 0
        self.current_word_score = 0
        self.hands_letters = [] #ta grammata pou exei sto xeri tou
        self.used_letters = [] # ta grammata pou einai na valei sto board
        self.word_letters = []
        self.word = None
        self.x_coords = []
        self.y_coords = []
        self.x_axis = True
        self.y_axis = True
        self.word_start = None
        self.word_finish = None
        self.word_axis = None
        self.first_check = None

    #taksinomoume tis listes me tis suntetagmenes
    def prepare_coords(self):
        #me selection sort proetoimazoume tis suntetagmenes
        for coord_x in range(len(self.x_coords)):
            min_coord_x = coord_x
            for j in range(coord_x + 1, len(self.x_coords)):
                if self.x_coords[min_coord_x] > self.x_coords[j]:
                    min_coord_x = j
            temp = self.x_coords[coord_x]
            self.x_coords[coord_x] = self.x_coords[min_coord_x]
            self.x_coords[min_coord_x] = temp

        for coord_y in range(len(self.y_coords)):
            min_coord_y = coord_y
            for j in range(coord_y + 1, len(self.y_coords)):
                if self.y_coords[min_coord_y] > self.y_coords[j]:
                    min_coord_y = j
            temp = self.y_coords[coord_y]   
            self.y_coords[coord_y] = self.y_coords[min_coord_y]
            self.y_coords[min_coord_y] = temp
        
        for i in self.y_coords:
            print(i)
        for i in self.x_coords:
            print(i)
        print("1 coords are ready")

    def validate_coords(self):
        for coord_x in range(1, len(self.x_coords)):
            if self.x_coords[coord_x - 1] != self.x_coords[coord_x]:
                self.x_axis = False
                break

        for coord_y in range(1, len(self.y_coords)):
            if self.y_coords[coord_y - 1] != self.y_coords[coord_y]:
                self.y_axis = False
                break

        print("2 coords are ready")
        print(self.y_axis)
        print(self.x_axis)

    def process_coords(self):
        if self.y_axis == True and self.x_axis == False:
            self.word_start = self.y_coords[0]
            self.word_finish = self.y_coords[len(self.y_coords)-1]
            self.word_axis = self.x_coords[0]
            self.first_check = True
        elif self.x_axis == True and self.y_axis == False:
            self.word_start = self.x_coords[0]
            self.word_finish = self.x_coords[len(self.x_coords)-1]
            self.word_axis = self.y_coords[0]
            self.first_check = True
        else:
            self.first_check = False
        print(self.y_coords[0])
        print(self.x_coords[0])
        print("3 coords are ready")
        print(self.word_start)
        print(self.word_axis)
        print(type(self.word_start))
        type(self.word_axis)

    def reset_values(self):
        self.hands_letters.clear()
        self.used_letters.clear()
        self.word_letters.clear()
        self.word = None
        self.x_coords.clear()
        self.y_coords.clear()
        self.x_axis = None
        self.y_axis = None
        self.word_start = None
        self.word_finish = None
        self.word_axis = None
        self.first_check = None
    