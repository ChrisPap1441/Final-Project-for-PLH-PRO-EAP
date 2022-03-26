import random 

class Letters_bag:
    def __init__(self):
        self.letters_bag = []
        self.create_letters()

    def create_letters(self):
        self.letters_bag.extend(["Ζ", "Θ", "Ξ", "Ψ", "Β", "Φ", "Χ"])
        for i in range(2):
            self.letters_bag.extend(["Γ", "Δ"])
        for i in range(3):
            self.letters_bag.extend(["Λ", "Μ", "Ω"])
        for i in range(4):
            self.letters_bag.extend(["Κ", "Π", "Υ"])
        for i in range(5):
            self.letters_bag.extend(["Ρ"])
        for i in range(6):
            self.letters_bag.extend(["Ν"])
        for i in range(7):
            self.letters_bag.extend(["Σ", "Η"])
        for i in range(8):
            self.letters_bag.extend(["Ε", "Ι", "Τ"])
        for i in range(9):
            self.letters_bag.extend(["Ο"])
        for i in range(12):
            self.letters_bag.extend(["Α"])
    
    def pick_letter(self):
        random.shuffle(self.letters_bag)

        if len(self.letters_bag) > 0:
            return self.letters_bag.pop()
        else:
            return "game over"
        
