from enum import Enum
from guizero import App, Text, Window, PushButton
from dispenser import TestDispenser, Dispenser

# Constants used by the app
GRAMS_SALT_PER_CUP = 273
GRAMS_FLOUR_PER_CUP = 120
GRAMS_SUGAR_PER_CUP = 200

CUPS_PER_CUP = 1
HALF_CUPS_PER_CUP = 2
FOURTH_CUPS_PER_CUP = 4
EIGHTH_CUPS_PER_CUP = 8
TEASPOON_PER_CUP = 48

SALT_DISPENSING_TEXT = "Salt Dispensing"
FLOUR_DISPENSING_TEXT = "Flour Dispensing"
SUGAR_DISPENSING_TEXT = "Sugar Dispensing"


class Ingredient(Enum):
    SALT = 0
    FLOUR = 1
    SUGAR = 2


class Unit(Enum):
    CUP = 0
    HALF_CUP = 1
    FOURTH_CUP = 2
    EIGHTH_CUPS = 3
    TEASPOON = 4


class Gui(object):
    def __init__(self):
        
        self.dispenser = Dispenser()
        self.cup_number = 0
        self.half_cup_number = 0
        self.eighth_cup_number = 0
        self.teaspoon_number = 0
        self.dispensing_id = Ingredient.SALT  # Default: id is salt (0)
        self.dispensing_id_text = SALT_DISPENSING_TEXT  # Default: salt
        self.dispensing_amount = 0
        self.dispensing_flag = False
        
        self.app = App(title="Pestle Co.")
        # All code must be added in th event loop
        # START
        # Set up the option window and hide it for now
        self.option_window = Window(self.app, title="Choosing a spice")
        self.option_window.hide()  # hide this window for now
        # Set up the dispensing window and hide it for now
        self.dispensing_window = Window(self.option_window, title="Dispensing")
        self.dispensing_window.hide()  # hide this window for now
        # Set up the welcome window
        self.app.set_full_screen()
        self.welcome_message = Text(self.app, text="Pestle Co.", size=70, font="Times New Roman", color="blue")
        self.start_button = PushButton(self.app, command=self.open_option_window, text="Push to Start", width=20, height=5)
        self.start_button.text_color=(205,133,0)
        self.start_button.text_size=30

        # Option page/window set up
        # Salt button
        self.salt_button = PushButton(self.option_window, command=self.open_salt_dispensing_window, text="Salt",
                                      align="top", width=10, height=2)
        self.salt_button.text_color=(205,133,0)
        self.salt_button.text_size=20
        # Flour button
        self.flour_button = PushButton(self.option_window, command=self.open_flour_dispensing_window, text="Flour",
                                        align="top", width=10, height=2)
        self.flour_button.text_color=(205,133,0)
        self.flour_button.text_size=20
        # Sugar button
        self.sugar_button = PushButton(self.option_window, command=self.open_sugar_dispensing_window, text="Sugar",
                                        align="top", width=10, height=2)
        self.sugar_button.text_color=(205,133,0)
        self.sugar_button.text_size=20
        # Done button
        self.done_button = PushButton(self.option_window, command=self.close_option_window, text="Done", align="bottom", width=10, height=2)
        self.done_button.text_color=(205,133,0)
        self.done_button.text_size=20
    
        # Dispensing page/window set up
        self.dispensing_text = Text(self.dispensing_window, text=self.dispensing_id_text)
        self.cup_button = PushButton(self.dispensing_window, command=self.add_a_cup, text="Cup")
        self.cup_number_text = Text(self.dispensing_window, text=str(self.cup_number) + " Cups(s)")
        self.cup_button.text_color=(205,133,0)
        self.cup_button.text_size=20
        
        self.half_cup_button = PushButton(self.dispensing_window, command=self.add_a_half_cup, text="Half Cup")
        self.half_cup_number_text = Text(self.dispensing_window, text=str(self.half_cup_number) + " Half_cup(es)")
        self.half_cup_button.text_color=(205,133,0)
        self.half_cup_button.text_size=20
        
        self.eighth_cup_button = PushButton(self.dispensing_window, command=self.add_a_eighth_cup, text="Eighth_cup")
        self.eighth_cup_number_text = Text(self.dispensing_window, text=str(self.eighth_cup_number) + " Eighth_cup(es)")
        self.eighth_cup_button.text_color=(205,133,0)
        self.eighth_cup_button.text_size=20
        
        self.teaspoon_button = PushButton(self.dispensing_window, command=self.add_a_teaspoon, text="Teaspoon")
        self.teaspoon_number_text = Text(self.dispensing_window, text=str(self.teaspoon_number) + " Teaspoon(s)")
        self.teaspoon_button.text_color=(205,133,0)
        self.teaspoon_button.text_size=20
        
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

    def add_dispensing_amount(self, dispensing_id, unit):
        grams_per_cup = GRAMS_SALT_PER_CUP # default
        conversion_per_cup = CUPS_PER_CUP # default
        if dispensing_id == Ingredient.SALT:
            grams_per_cup = GRAMS_SALT_PER_CUP
        elif dispensing_id == Ingredient.FLOUR:
            grams_per_cup = GRAMS_FLOUR_PER_CUP
        elif dispensing_id == Ingredient.SUGAR:
            grams_per_cup = GRAMS_SUGAR_PER_CUP
        if unit == Unit.CUP:
            conversion_per_cup = CUPS_PER_CUP
        elif unit == Unit.HALF_CUP:
            conversion_per_cup = HALF_CUPS_PER_CUP
        elif unit == Unit.FOURTH_CUP:
            conversion_per_cup = FOURTH_CUPS_PER_CUP
        elif unit == Unit.EIGHTH_CUPS:
            conversion_per_cup = EIGHTH_CUPS_PER_CUP
        elif unit == Unit.TEASPOON:
            conversion_per_cup = TEASPOON_PER_CUP
        self.dispensing_amount += grams_per_cup/conversion_per_cup

    # Helper functions: dispensing
    def add_a_cup(self):
        self.cup_number += 1
        self.cup_number_text.clear()
        self.cup_number_text.append(str(self.cup_number) + " Cup(s)")
        self.add_dispensing_amount(self.dispensing_id, Unit.CUP)

    def add_a_half_cup(self):
        self.half_cup_number += 1
        self.half_cup_number_text.clear()
        self.half_cup_number_text.append(str(self.half_cup_number) + " Half Cup(s)")
        self.add_dispensing_amount(self.dispensing_id, Unit.HALF_CUP)

    def add_a_eighth_cup(self):
        self.eighth_cup_number += 1
        self.eighth_cup_number_text.clear()
        self.eighth_cup_number_text.append(str(self.eighth_cup_number) + " Eighth Cup(s)")
        self.add_dispensing_amount(self.dispensing_id, Unit.EIGHTH_CUPS)

    def add_a_teaspoon(self):
        self.teaspoon_number += 1
        self.teaspoon_number_text.clear()
        self.teaspoon_number_text.append(str(self.teaspoon_number) + " Teaspoon(s)")
        self.add_dispensing_amount(self.dispensing_id, Unit.TEASPOON)

    def final_dispense(self):
        print("in final")
        self.dispensing_flag = True
        self.dispenser.dispense(self.dispensing_id, self.dispensing_amount)
        self.close_dispensing_window()  # Return to the dispensing window
        # self.open_option_window()  # Return to the option window

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
        self.half_cup_number_text.append(str(self.half_cup_number) + " Half Cup(s)")
        self.eighth_cup_number = 0
        self.eighth_cup_number_text.clear()
        self.eighth_cup_number_text.append(str(self.eighth_cup_number) + " Eighth Cup(s)")
        self.teaspoon_number = 0
        self.teaspoon_number_text.clear()
        self.teaspoon_number_text.append(str(self.teaspoon_number) + " Teaspoon(s)")


# myGui = Gui()
