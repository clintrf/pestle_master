
echo "running setup for python3"

echo "installing pip3"
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx

echo "installing flask for the server side"
sudo pip3 install flask

echo "installing GPIO PINs"
sudo pip3 install RPI.GPIO

echo "installing the GUI software"
sudo pip3 install guizero

echo "installing tkinter for user input from screen"
sudo apt-get install python3-tk

