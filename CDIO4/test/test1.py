from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Initialize the motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Control the motors
left_motor.run(500)
right_motor.run(500)

# Disconnect from the EV3 Brick (optional)
ev3.speaker.beep()
