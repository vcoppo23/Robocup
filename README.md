# Robocup
Creates a website that takes user inputs via a ps4 controller to control the robot

## Installation:
install Flask on Both Raspberry Pis with
```bash
pip3 install flask
```

On the Raspberry Pi that is controlling the motors enable I2C

Run the command in the Raspberry Pi terminal
```bash
sudo raspi-config
```
Using the arrow keys, go down and select "Interfacing Options," then select "I2C" and enable it
## Usage:
SSH into both of the Raspberry Pis using "pi@*ip*" for the motor controlling Pi and "student@*ip*" for the camera controlling Pi (intert Pi's ip into the italicized ip)

Then cd into the correct directory

For the motor controlling pi put in the command
```bash
cd Robocup
```
Then check to make sure you are in the correct directory with
```bash
ls
```
You should see a file name "app.py" and a file named "motorlib.py" with 3/4 other folders

For the camera pi put in the command
```bash
cd Downloads/robo_cams
```
(something along those lines, if that doesn't work just cd into Downloads then run "ls" to get the folder name)
Check using "ls" and make sure there is an app.py file

Start the flask server on the Raspberry Pi that controls the motors with
```bash
python3 -m flask run --host=0.0.0.0
```

Then start the cameras on the other Pi with
```bash
sudo python3 app.py
```

To stop a flask server hit "Control+C" at the same time on your keybaord

### Credits:
Benilde-St. Margarets Robotics Team
2022-23
