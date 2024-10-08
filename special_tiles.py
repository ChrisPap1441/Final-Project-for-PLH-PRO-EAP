#Μέθοδος για τα κελιά λέξεων τριπλής αξίας του ταμπλό 
def triple_word(x, y):
    return ((x==0 and y == 0) or (x==0 and y == 7) or (x==0 and y == 14) or (x==7 and y == 0) or (x==7 and y == 14) or (x==14 and y == 0) or (x==14 and y == 7) or (x==14 and y == 14))

#Μέθοδος για τα κελιά γραμμάτων τριπλής αξίας του ταμπλό 
def triple_letter(x, y):
    return ((x==1 and y == 5) or (x==1 and y == 9) or (x==5 and y == 1) or (x==5 and y == 5) or (x==5 and y == 9) or (x==5 and y == 13) or (x==9 and y == 1) or (x==9 and y == 5)
                    or (x==9 and y == 9) or (x==9 and y == 13) or (x==13 and y == 5) or (x==13 and y == 9))

#Μέθοδος για τα κελιά γραμμάτων διπλής αξίας του ταμπλό 
def double_letter(x, y):
    return ((x==0 and y == 3) or (x==0 and y == 11) or (x==2 and y == 6) or (x==2 and y == 8) or (x==3 and y == 0) or (x==3 and y == 7) or (x==3 and y == 14) or (x==6 and y == 2)
                    or (x==6 and y == 6) or (x==6 and y == 8) or (x==6 and y == 12) or (x==7 and y == 3) or (x==7 and y == 11) or (x==8 and y == 2) or (x==8 and y == 6) or (x==8 and y == 8) or (x==8 and y == 12)
                    or (x==11 and y == 0) or (x==11 and y == 7) or (x==11 and y == 14) or (x==12 and y == 6) or (x==12 and y == 8) or (x==14 and y == 3) or (x==14 and y == 11))

#Μέθοδος για τα κελιά λέξεων διπλής αξίας του ταμπλό 
def double_word(x, y):
    return ((x==1 and y == 1) or (x==1 and y == 13) or (x==2 and y == 2) or (x==2 and y == 12) or (x==3 and y == 3) or (x==3 and y == 11) or (x==4 and y == 4) or (x==4 and y == 10)
                    or (x==10 and y == 4) or (x==10 and y == 10) or (x==11 and y == 3) or (x==11 and y == 11) or (x==12 and y == 2) or (x==12 and y == 12) or (x==13 and y == 1) or (x==13 and y == 13))

#Μέθοδος για το κεντρικό κελί του ταμπλό        
def center(x, y):
    return (x==7 and y == 7)