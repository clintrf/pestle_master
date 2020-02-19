
from dispenser import TestDispenser, Dispenser
import os



if __name__ == "__main__":
    if 1 :
        dispenser = Dispenser()
        
    else:
        dispenser = TestDispenser()


    dispenser.dispense(1, 100)
     
    dispenser.clean_and_exit()

