class Player:
    def __init__(self):
        self.highscore = 0
        self.hands_letters = [] #ta grammata pou exei sto xeri tou
        self.used_letters = [] # ta grammata pou einai na valei sto board
        self.x_coords = []
        self.y_coords = []
        self.x_axis = None
        self.y_axis = None
        self.word_start = None
        self.word_finish = None

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

    def validate_coords(self):
        for coord_x in range(coord_x + 1, len(self.x_coords)):
            if self.x_coords[coord_x - 1] != self.x_coords[coord_x]:
                self.x_axis = False
                break
        self.x_axis = True

        for coord_y in range(coord_y + 1, len(self.y_coords)):
            if self.y_coords[coord_y - 1] != self.y_coords[coord_y]:
                self.y_axis = False
                break
        self.y_axis = True


    