import logging
import os

from dispenser import TestDispenser, Dispenser
import os

from flask import Flask
from ~/.local/lib/python2.7/site-packages/flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']
STATUSPROTIEN = ['protien','protien powder']
STATUSCHIA = ['chia','seed', 'seeds', 'chia seeds']
STATUSLEMONADE = ['lemonade','lemon', 'fresco']
STATUSSHAKE = ['shake','post workout']

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('GpioIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    if 1 :
        dispenser = Dispenser()
        
    else:
        dispenser = TestDispenser()
        
    if status in STATUSON:
        return statement('turning {} Pestle Home'.format(status))
    elif status in STATUSOFF:
        return statement('turning {} Pestle Home'.format(status))
    elif status in STATUSPROTIEN:
        dispenser.dispense(0, 3)
        dispenser.clean_and_exit()
        return statement('dispensing {} from Pestle Home'.format(status))
    elif status in STATUSCHIA:
        dispenser.move(1)
        dispenser.dispense(1, 3)
        dispenser.calibrate_track()
        dispenser.clean_and_exit()
        return statement('dispensing {} from Pestle Home'.format(status))
    elif status in STATUSLEMONADE:
        dispenser.dispense(0, 3)
        dispenser.clean_and_exit()
        return statement('dispensing {} from Pestle Home'.format(status))
    elif status in STATUSSHAKE:
        dispenser.dispense(0, 3)
        dispenser.move(1)
        dispenser.dispense(1, 3)
        dispenser.calibrate_track()
        dispenser.clean_and_exit()
        return statement('dispensing {} from Pestle Home'.format(status))
    else:
        return statement('Sorry {} is not possible Right now'.format(status))
    
    
 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
