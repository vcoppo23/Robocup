# Robocup
Creates a website that takes user inputs via a ps4 controller to control the robot

## Installation:
Clone the repo into your Raspberry Pi with 
```bash
git clone https://github.com/vcoppo23/Robocup.git
```

install requirements.txt on the Raspberry Pis with
```bash
pip3 install -r requirements.txt
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

Start the flask_socketIO server on the Raspberry Pi that controls the motors with
```bash
python3 app.py
```
A bunch of lines with pop up into the terminal with a few URLs, go to *pi's ip*:5000 in Google and you should see the page,
Then start the cameras on the other Pi

Visit [Camera Github](https://github.com/tmedina23/Robocup23-Cams) for more information on cameras

Refresh the Google page and the cameras will load onto the page

You can connect a ps4 controller via a wire or wirelessly to your laptop to run the robot, just make sure you are on the Google page (check by clicking onto the page) 

To make sure it is sending the controls right click onto the Google page and click "inspect", in the pop up that appears to the right go to the top right and click on "Console" (It may be throwing a lot of errors if you haven't moved the controller on the page yet, just click the "X" button and message saying along the lines of a controller being connected will appear) 

### Emergency Shutdown:
When giving no input to the controller, all motors are set to 0% power. 

Closing out of the google page will submit a "Disconnect" message to server which turns on shutdown mode and sets motors to 0% power.

If the controller disconnects, motor power is set to 0%.

### Controls:
#### Tread Mode:
Up/Down on joysticks move treads forward/backward, the bumpers/triggers move the flippers up/down

#### Turret Mode:
On Left Joystick: Left/Right moves Turret Clockwise/Counterclockwise, Up/Down moves shoulder up/down

On Right Joystick: Left/Right moves the wrist, Up/Down moves the elbow

Other wrist/Claw not implemented yet

#### Control Description:
"No Input": No controller inputs are being read

"Tread Mode": Controller is reading inputs in tread mode

"Turret Mode": Controller is reading inputs in turret mode

#### Switch Mode:
Click on Left D-Pad button (Leftmost button on controller), if it registers the input, "toggled" will appear

### Credits:
Benilde-St. Margarets Robotics Team
2022-23
