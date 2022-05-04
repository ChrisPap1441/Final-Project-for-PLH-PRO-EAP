import random 

class Letters_bag:
    def __init__(self):
        self.letters_bag = []
        self.prepare_letters()
        self.letters_points = {}
        self.prepare_points()

    def prepare_letters(self):
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
    
    def prepare_points(self):
        for key in ["Α", "Ε", "Η", "Ι", "Ν", "Ο", "Σ", "Τ"]:
            self.letters_points[key] = 1
        for key in ["Κ", "Π", "Ρ", "Υ"]:
            self.letters_points[key] = 2
        for key in ["Λ", "Μ", "Ω"]:
            self.letters_points[key] = 3
        for key in ["Γ", "Δ"]:
            self.letters_points[key] = 4
        for key in ["Β", "Φ", "Χ"]:
            self.letters_points[key] = 8
        for key in ["Ζ", "Θ", "Ξ", "Ψ"]:
            self.letters_points[key] = 10

    def pick_letter(self):
        random.shuffle(self.letters_bag) #anakateuoume ta grammata

        if len(self.letters_bag) > 0:
            return self.letters_bag.pop()
        else:
            return "!" #exoun teleiosei ta grammata ara teleionei kai to paixnidi