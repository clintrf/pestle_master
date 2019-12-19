import os
import atexit

from app import app
from dispenser import TestDispenser, Dispenser

#export FLASK_ENV=development



dispenser = None



if __name__ == "__main__":
    
    if os.uname()[1] == 'pestle-spice-dispenser':
        print('Name is pestle-spice-dispenser')
        dispenser = TestDispenser()
        
    else:
        # This is a test running on a desktop
        print('Name is Other')
        dispenser = TestDispenser()

    

    atexit.register(lambda: dispenser.clean_and_exit())
    app.run(host="0.0.0.0", debug=True, port=5000)
