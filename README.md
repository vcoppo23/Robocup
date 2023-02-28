# Robocup
Creates a website that takes user inputs via a ps4 controller to control the robot

## Installation:
Clone the repo into your Raspberry Pi with 
```bash
git clone https://github.com/vcoppo23/Robocup.git
```

install Flask on the Raspberry Pis with
```bash
pip3 install flask
```

install the ioexpander library
```bash
pip3 install pimoroni-ioexpaner
```
If it gives you an error, try using sudo pip3 install ... 

On the Raspberry Pi that is controlling the motors enable I2C, Run the command in the Raspberry Pi terminal
```bash
sudo raspi-config
```
Using the arrow keys, go down and select "Interfacing Options," then select "I2C" and enable it
## Usage:
SSH into both of the Raspberry Pis using "pi@*ip*" for the motor controlling Pi and "student@*ip*" for the camera controlling Pi (intert Pi's ip into the italicized ip)

Then cd into the correct directory with 

```bash
cd Robocup
```

Then check to make sure you are in the correct directory with
```bash
ls
```
You should see a file name "app.py" and a file named "motorlib.py" with 3/4 other folders

Start the flask server on the Raspberry Pi that controls the motors with
```bash
python3 -m flask run --host=0.0.0.0
```
A bunch of lines with pop up into the terminal with a few URLs, go to *pi's ip*:5000 in Google and you should see the page,
Then start the cameras on the other Pi

Visit [Camera Github](https://github.com/tmedina23/Robocup23-Cams) for more information on cameras

Refresh the Google page and the cameras will load onto the page

You can connect a ps4 controller via a wire or wirelessly to your laptop to run the robot, just make sure you are on the Google page (check by clicking onto the page) 

To make sure it is sending the controls right click onto the Google page and click "inspect", in the pop up that appears to the right go to the top right and click on "Console" (It may be throwing a lot of errors if you haven't moved the controller on the page yet, just click the "X" button and message saying along the lines of a controller being connected will appear) 

If you see the "Tread mode sent" line, you can move the the treads/flippers. To switch modes, click on the Left button on the D-Pad (the leftmost button on the controller) and a new line will appear in the Console page with "Turret Mode Sent," now you can move the turret/arm (it may take a few tries to switch, it is very finicky, your current mode is the one with the increasting number to the left of it)

### INCASE SOMETHING GOES WRONG HIT THE PS BUTTON:
That is the Stop All button, it puts the motors into a constant state of 0% power, if the motors start to jitter back and forth/stop it means it is working, this gives you time to unplug the batteries.

To get out of Stop All mode, just stop the flask servers and restart them

To stop a flask server hit "Control+C" at the same time on your keyboard while in the pi terminal

### Controls:
While in Tread Mode:
Up/Down on joysticks move treads forward/backward respectivly, the bumper/trigger move the flippers up/down respectivly

While in Turret Mode:

On Left Joystick:
Left/Right moves Turret Clockwise/Counterclockwise, Up/Down moves shoulder up/down

On Right Joystick:
Left/Right moves the wrist, Up/Down moves the elbow

Other wrist/Claw not implemented yet

### Credits:
Benilde-St. Margarets Robotics Team
2022-23
