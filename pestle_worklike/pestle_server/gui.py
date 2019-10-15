from enum import Enum
from guizero import App, Text, Window, PushButton
from dispenser import TestDispenser, Dispenser

# Constants used by the app
GRAMS_SALT_PER_CUP = 273
GRAMS_FLOUR_PER_CUP = 120
GRAMS_SUGAR_PER_CUP = 200
CUPS_PER_CUP = 1
HALF_CUPES_PER_CUP = 2
FOURTH_CUPES_PER_CUP = 4
EIGHTH_CUPES_PER_CUP = 8
TEASPOON_PER_CUP = 48

SALT_DISPENSING_TEXT = "Salt Dispensing"
FLOUR_DISPENSING_TEXT = "Flour Dispensing"
SUGAR_DISPENSING_TEXT = "Sugar Dispensing"

class Spices(Enum):
    SALT = 0
    FLOUR = 1
    SUGAR = 2


class Gui(object):
    def __init__(self):
        
        self.dispenser = Dispenser()
        self.cup_number = 0
        self.half_cup_number = 0
        self.eighth_cup_number = 0
        self.teaspoon_number = 0
        self.dispensing_id = Spices.SALT  # Default: id is salt (0)
        self.dispensing_id_text = SALT_DISPENSING_TEXT  # Default: salt
        self.dispensing_amount = 0
        self.dispensing_flag = False
        
        self.app = App(title="Pestle Co.")
        # All code must be added in th event loop
        # START
        self.option_window = Window(self.app, title="Choosing a spice")
        self.option_window.hide()  # hide this window for now
        self.dispensing_window = Window(self.option_window, title="Dispensing")
        self.dispensing_window.hide()  # hide this window for now
        self.app.set_full_screen()
        self.welcome_message = Text(self.app, text="Pestle Co.", size=40, font="Times New Roman", color="blue")
        self.start_button = PushButton(self.app, command=self.open_option_window, text="Push to Start", width=60, height=10s)

        # Option page
        self.salt_button = PushButton(self.option_window, command=self.open_salt_dispensing_window, text="Salt",
                                      align="top")
        self.flour_button = PushButton(self.option_window, command=self.open_flour_dispensing_window, text="Flour",
                                        align="top")
        self.sugar_button = PushButton(self.option_window, command=self.open_sugar_dispensing_window, text="Sugar",
                                        align="top")
        self.done_button = PushButton(self.option_window, command=self.close_option_window, text="Done", align="bottom")

        # Dispensing page
        self.dispensing_text = Text(self.dispensing_window, text=self.dispensing_id_text)
        self.cup_button = PushButton(self.dispensing_window, command=self.add_a_cup, text="Cup")
        self.cup_number_text = Text(self.dispensing_window, text=str(self.cup_number) + " Cups(s)")
        
        self.half_cup_button = PushButton(self.dispensing_window, command=self.add_a_half_cup, text="Half Cup")
        self.half_cup_number_text = Text(self.dispensing_window, text=str(self.half_cup_number) + " Half_cup(es)")
        
        self.eighth_cup_button = PushButton(self.dispensing_window, command=self.add_a_eighth_cup, text="Eighth_cup")
        self.eighth_cup_number_text = Text(self.dispensing_window, text=str(self.eighth_cup_number) + " Eighth_cup(es)")
        
        self.teaspoon_button = PushButton(self.dispensing_window, command=self.add_a_teaspoon, text="Teaspoon")
        self.teaspoon_number_text = Text(self.dispensing_window, text=str(self.teaspoon_number) + " Teaspoon(s)")
        
        self.dispense_button = PushButton(self.dispensing_window, command=self.final_dispense, text="Dispense",
                                          align="bottom")
        self.reset_button = PushButton(self.dispensing_window, command=self.reset_measurement, text="Reset",
                                       align="bottom")
        # STOP
        print("here")
        self.app.display()
        
        # Helper functions: windows
    def open_option_window(self):
        self.option_window.show(wait=True)
        self.option_window.set_full_screen()

    def close_option_window(self):
        self.option_window.exit_full_screen()
        self.option_window.hide()
        self.app.display()

    def open_dispensing_window(self):
        self.dispensing_window.show(wait=True)
        self.dispensing_window.set_full_screen()

    def close_dispensing_window(self):
        self.dispensing_window.exit_full_screen()
        self.dispensing_window.hide()
        self.open_option_window()

    def open_salt_dispensing_window(self):
        self.dispensing_id_text = SALT_DISPENSING_TEXT
        self.dispensing_text.clear()
        self.dispensing_text.append(self.dispensing_id_text)
        self.open_dispensing_window()

    def open_flour_dispensing_window(self):
        self.dispensing_id_text = FLOUR_DISPENSING_TEXT
        self.dispensing_text.clear()
        self.dispensing_text.append(self.dispensing_id_text)
        self.open_dispensing_window()
       
    def open_sugar_dispensing_window(self):
        self.dispensing_id_text = SUGAR_DISPENSING_TEXT
        self.dispensing_text.clear()
        self.dispensing_text.append(self.dispensing_id_text)
        self.open_dispensing_window()

    # Helper functions: dispensing
    def add_a_cup(self):
        self.cup_number += 1
        self.cup_number_text.clear()
        self.cup_number_text.append(str(self.cup_number) + " cup(s)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON/CUPS_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON/CUPS_PER_TEASPOON

    def add_a_half_cup(self):
        self.half_cup_number += 1
        self.half_cup_number_text.clear()
        self.half_cup_number_text.append(str(self.half_cup_number) + " Half_cup(es)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON/HALF_CUPES_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON/HALF_CUPES_PER_TEASPOON

    def add_a_eighth_cup(self):
        self.eighth_cup_number += 1
        self.eighth_cup_number_text.clear()
        self.eighth_cup_number_text.append(str(self.eighth_cup_number) + " Eighth_cup(es)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON/EIGHTH_CUPES_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON/EIGHTH_CUPES_PER_TEASPOON

    def add_a_teaspoon(self):
        self.teaspoon_number += 1
        self.teaspoon_number_text.clear()
        self.teaspoon_number_text.append(str(self.teaspoon_number) + " Teaspoon(es)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON

    def final_dispense(self):
        print("in final")
        self.dispensing_flag = True
        self.dispenser.dispense(self.dispensing_id, self.dispensing_amount);
        self.close_dispensing_window()  # Return to the dispensing window
        #self.open_option_window()  # Return to the option windowho

    def ready_to_dispense(self):
        return self.dispensing_flag

    def get_slot_id(self):
        return self.dispensing_id

    def get_amount_in_grams(self):
        return self.dispensing_amount

    def reset_measurement(self):
        self.cup_number = 0
        self.cup_number_text.clear()
        self.cup_number_text.append(str(self.cup_number) + " Cup(s)")
        self.half_cup_number = 0
        self.half_cup_number_text.clear()
        self.half_cup_number_text.append(str(self.half_cup_number) + " Half Cup(es)")
        self.eighth_cup_number = 0
        self.eighth_cup_number_text.clear()
        self.eighth_cup_number_text.append(str(self.eighth_cup_number) + " Eighth Cup(es)")
        self.teaspoon_number = 0
        self.teaspoon_number_text.clear()
        self.teaspoon_number_text.append(str(self.teaspoon_number) + " Teaspoon(es)")
#myGui = Gui()
