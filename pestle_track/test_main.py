import os
from dispenser import TestDispenser
from dispenser import Dispenser
dispenser = None

def text_parser(filepath, separator=","):
    return_dict = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.split(separator)
            return_dict[line[0]] = line[1], line[2], line[3] 
    return return_dict

def userInput(diction, index ):
    index = str(index)
    x = int(diction[index][0])
    y = int(diction[index][1])
    amount = int(diction[index][2])
    return x,y,amount

if __name__ == "__main__":

    dispenser = Dispenser()
    #dispenser = TestDispenser()
    dispenser.calibrate_track()
    dispenser.calibrate_scale(100)

    command = text_parser("input.txt")
    x,y,amount = userInput(command,1)
    
    while((x !=3) & (y != 3)):
        for i in range(1,len(command)):
            dispenser.move(x,y)
            dispenser.dispense(amount)
            dispenser.calibrate_track()
            dispenser.calibrate_scale(100)
            x,y,amount = userInput(command, i+1)

        #x = 3
        #y = 3
        #userInput = x,y, amount

