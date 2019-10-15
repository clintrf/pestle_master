from enum import Enum
from guizero import App, Text, Window, PushButton
from dispenser import TestDispenser, Dispenser

# Constants used by the app
GRAMS_SALT_PER_TEASPOON = 5.69
GRAMS_PEPPER_PER_TEASPOON = 2.1
SMIDGENS_PER_TEASPOON = 32
PINCHES_PER_TEASPOON = 16
DASHES_PER_TEASPOON = 8
SALT_DISPENSING_TEXT = "Salt Dispensing"
PEPPER_DISPENSING_TEXT = "Pepper Dispensing"


class Spices(Enum):
    SALT = 0
    PEPPER = 1


class Gui(object):
    def __init__(self):
        
        self.dispenser = Dispenser()
        self.smidgen_number = 0
        self.pinch_number = 0
        self.dash_number = 0
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
        self.start_button = PushButton(self.app, command=self.open_option_window, text="Push to Start")

        # Option page
        self.salt_button = PushButton(self.option_window, command=self.open_salt_dispensing_window, text="Salt",
                                      align="top")
        self.pepper_button = PushButton(self.option_window, command=self.open_pepper_dispensing_window, text="Pepper",
                                        align="top")
        self.done_button = PushButton(self.option_window, command=self.close_option_window, text="Done", align="bottom")

        # Dispensing page
        self.dispensing_text = Text(self.dispensing_window, text=self.dispensing_id_text)
        self.smidgen_button = PushButton(self.dispensing_window, command=self.add_a_smidgen, text="Smidgen")
        self.smidgen_number_text = Text(self.dispensing_window, text=str(self.smidgen_number) + " Smidgen(s)")
        self.pinch_button = PushButton(self.dispensing_window, command=self.add_a_pinch, text="Pinch")
        self.pinch_number_text = Text(self.dispensing_window, text=str(self.pinch_number) + " Pinch(es)")
        self.dash_button = PushButton(self.dispensing_window, command=self.add_a_dash, text="Dash")
        self.dash_number_text = Text(self.dispensing_window, text=str(self.dash_number) + " Dash(es)")
        self.teaspoon_button = PushButton(self.dispensing_window, command=self.add_a_teaspoon, text="Teaspoon")
        self.teaspoon_number_text = Text(self.dispensing_window, text=str(self.teaspoon_number) + " Teaspoon(s)")
        self.dispense_button = PushButton(self.dispensing_window, command=self.final_dispense, text="Dispense",
                                          align="bottom")
        self.reset_button = PushButton(self.dispensing_window, command=self.reset_measurement, text="Reset",
                                       align="bottom")
        # STOP
        print("here")
        self.app.display()
        print("here1")
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

    def open_pepper_dispensing_window(self):
        print("in pep")
        self.dispensing_id_text = PEPPER_DISPENSING_TEXT
        self.dispensing_text.clear()
        self.dispensing_text.append(self.dispensing_id_text)
        self.open_dispensing_window()

    # Helper functions: dispensing
    def add_a_smidgen(self):
        self.smidgen_number += 1
        self.smidgen_number_text.clear()
        self.smidgen_number_text.append(str(self.smidgen_number) + " Smidgen(s)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON/SMIDGENS_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON/SMIDGENS_PER_TEASPOON

    def add_a_pinch(self):
        self.pinch_number += 1
        self.pinch_number_text.clear()
        self.pinch_number_text.append(str(self.pinch_number) + " Pinch(es)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON/PINCHES_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON/PINCHES_PER_TEASPOON

    def add_a_dash(self):
        self.dash_number += 1
        self.dash_number_text.clear()
        self.dash_number_text.append(str(self.dash_number) + " Dash(es)")
        self.dispensing_amount += GRAMS_SALT_PER_TEASPOON/DASHES_PER_TEASPOON if self.dispensing_id == Spices.SALT \
            else GRAMS_PEPPER_PER_TEASPOON/DASHES_PER_TEASPOON

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
        self.smidgen_number = 0
        self.smidgen_number_text.clear()
        self.smidgen_number_text.append(str(self.smidgen_number) + " Smidgen(s)")
        self.pinch_number = 0
        self.pinch_number_text.clear()
        self.pinch_number_text.append(str(self.pinch_number) + " Pinch(es)")
        self.dash_number = 0
        self.dash_number_text.clear()
        self.dash_number_text.append(str(self.dash_number) + " Dash(es)")
        self.teaspoon_number = 0
        self.teaspoon_number_text.clear()
        self.teaspoon_number_text.append(str(self.teaspoon_number) + " Teaspoon(es)")
#myGui = Gui()
