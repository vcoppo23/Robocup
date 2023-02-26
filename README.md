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
Start the flask server on the Raspberry Pi that controls the motors with
```bash
pythton3 -m flask run --host=0.0.0.0
```

Start the cameras on the other Pi with
```bash
sudo python3 app.py
```

To stop a flask server hit "Control+C" at the same time on your keybaord

### Credits:
Benilde-St. Margarets Robotics Team
2022-23
