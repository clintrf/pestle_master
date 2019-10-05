#from sanic import Sanic
#from sanic.response import json
from flask import Flask
from flask import request

from dispenser import TestDispenser, Dispenser
import os
import atexit
from gui import Spices, Gui
# from slot_select import SLOT_SELECT

#app = Sanic()
app = Flask(__name__)

dispenser = None


@app.route('/api/ls')
async def ls():
    """List all information on what spices are available and quantities.
    """
    #return json({'spices': 'none'})
    return ''



@app.route('/api/dispense/<slot_id>/<amount>')
def dispense(slot_id = 0, amount = 0):
    """Dispense a certain amount of a certain spice.
    Args:
        slot_id (str): The ID of the slot to dispense from.
        amount (str): The amount of the spice to dispense in 1/100 grams. Must be able to cast to an int.
    """
    amount_in_grams = int(amount) / 100
    slot_id = int(slot_id)
    dispenser.dispense(slot_id, amount_in_grams)
    #return json({'data': {'slot_id': slot_id,'amount': amount_in_grams}})
    return ''

@app.route('/api/<amount>')
def test(amount = 0):
    print("testing")
    # This route could be useful for debugging by displaying all information as a web page.
    #return json({"hello": "world"})
    return ''


if __name__ == "__main__":
    print('1')
    if os.uname()[1] == 'pestle-spice-dispenser':
        dispenser = Dispenser()
        
    else:
        # This is a test running on a desktop
        dispenser = TestDispenser()

    myGui = Gui()
    if myGui.ready_to_dispense:
        dispenser.dispense(myGui.get_slot_id, myGui.get_amount_in_grams)
        myGui.dispensing_flag = False

    atexit.register(lambda: dispenser.clean_and_exit())
    app.run(host="0.0.0.0", port=8000)
