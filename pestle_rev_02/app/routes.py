from app import app
from dispenser import TestDispenser, Dispenser


@app.route('/')
@app.route('/index')
def index():
    print("index1")
    return "Hello World!"


@app.route('/api/v1/dispense/<slot_id>/<amount>')
def dispense(slot_id = 0, amount = 0):
    """Dispense a certain amount of a certain spice.
    Args:
        slot_id (str): The ID of the slot to dispense from.
        amount (str): The amount of the spice to dispense in 1/100 grams. Must be able to cast to an int.
    """
    dispenser = Dispenser()
    print("dispencer")
    print(amount)
    amount_in_grams = int(amount) * 100
    slot_id = int(slot_id)
    dispenser.dispense(slot_id, amount_in_grams)
    #return json({'data': {'slot_id': slot_id,'amount': amount_in_grams}})
    print("in dispense loop")
    return ''

@app.route('/api/<amount>')
def test(amount = 0):
    print("testing ")
    print(amount)
    print("\r\n")
    # This route could be useful for debugging by displaying all information as a web page.
    #return json({"hello": "world"})
    return ''
