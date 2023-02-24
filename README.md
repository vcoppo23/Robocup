# Robocup
Creates a website that takes user inputs via a ps4 controller to control the robot

## Installation:
Create a virtual environment with
```bash
python3 -m venv ./venv
```

Activate the virtual environment with
```bash
source venv/bin/activate
```

install Flask in the environment
```bash
pip3 install flask
```

On the Raspberry Pi enable I2C

Run the command in the raspberry pi terminal
```bash
sudo raspi-config
```
Using the arrow keys, go down and select "Interfacing Options," then select "I2C" and enable it
## Usage:
Activate the virtual environment (if not active already) with 
```bash
source venv/bin/activate
```
Then start the flask server with
```bash
pythton3 -m flask run --host=0.0.0.0
```

To stop the flask server hit "Control+C" at the same time on your keybaord

To exit the virutal environment type in the terminal
```bash
deactivate
```

### Credits:
Benilde-St. Margarets Robotics Team
2022-23
