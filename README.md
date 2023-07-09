# Robocup
Creates a website that takes user inputs via a ps4 controller to control the robot

Note: This is for when the raspberry pis are connected to an ethernet switch and then to the laptop

## Installation:
# Laptop
Download and install DHCP Server, and follow [This tutorial](https://youtu.be/oM2zVD9rL8I) to get things set up. (Note: When using DHCP with your raspberry pi's, they won't have internet, so download and install all required dependencies on them beforehand).

# Motor Controller Pi
Clone the repo into your Raspberry Pi with 
```bash
git clone https://github.com/vcoppo23/Robocup.git
```

install requirements.txt on the Raspberry Pis with
```bash
pip3 install -r requirements.txt
```
If it gives you an error, try using sudo pip3 install ... 

There might also be other installs not listed in the requirements.txt file, just read the error code and install what it lists.

Next, enable I2C, Run the command in the Raspberry Pi terminal
```bash
sudo raspi-config
```
Using the arrow keys, go down and select "Interfacing Options," then select "I2C" and enable it

# Camera Pi
Visit [Camera Github](https://github.com/tmedina23/Robocup23-Cams) for more information on cameras

Clone the above Repo into the Pi, plug in your 4 cameras, and run with "sudo python app.py." You can visit the cameras by putting the pi's address into your web browser. 

## Usage:
Run the camera pi and the motor controlling pi. If everything is correct you will be able to visit the flask server created by the motor controlling pi (192.168.1.X if you followed the above tutorial) and see all 4 cameras. Next, inspect the page and view the console, when you connect your controller it will start reading inputs and will tell you which mode you are in. 

### Emergency Shutdown:
There is a big red button, if you click it, it will send 0% power to motors (not recommended).

Instead, it is recommended that you hold down the options button on the controller which sets all motor values in your current mode to 0% while held down. Use this button until the E-Stop is used or the batteries are unplugged and/or off. 

## Controls:
### Tread Mode:
Up/Down on joysticks move treads forward/backward.

Bumpers/Triggers move front flippers up/down.

Up D-pad and triangle/Down-Dpad and X move back flippers up/down.

### Turret Mode:
Bumpers turn the turret

Up/Down On Left Joystick moves the shoulder

Up/Down On Right Joystick moves the elbow

Up/Down D-Pad moves the forearm

Triangle/X move the wrist

Triggers open/close the claw

### Inspect Console Description:
"No Input": No controller inputs are being read

"Tread Mode": Sending tread mode inputs

"Turret Mode": Sending turret mode inputs

"toggled": Switched between the 2 modes

### Switch Mode:
Click on the Left D-Pad button, if it registers the input, "toggled" will appear.

NOTE: Be careful not to fat finger the toggle button while giving inputs, as if you switch the motor will continue to run. To make it stop, just switch back.

## Credits:
Benilde-St. Margarets Robotics Team
2022-23
