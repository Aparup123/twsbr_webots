"""self_balancing controller."""
import math

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Accelerometer

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

#Accelerometer setup
accel=robot.getDevice('accel')
accel.enable(timestep)

#Function for getting tilt angle from the Accelerometer Data
def getAngle(accelValues):
    accelX=accelValues[0]
    accelY=accelValues[1]
    accelZ=accelValues[2]

    angleParameter=accelY/math.sqrt(accelX**2+accelZ**2)
    angle=math.atan(angleParameter)
    angleDegrees=math.degrees(angle)
    return angleDegrees

#Motor setup
left_motor=robot.getDevice('left_wheel')
right_motor=robot.getDevice('right_wheel')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0)
right_motor.setVelocity(0)

#Functions for robot movement
def moveForward(speed):
    left_motor.setVelocity(speed)
    right_motor.setVelocity(speed)

def moveBackward(speed):
    left_motor.setVelocity(-speed)
    right_motor.setVelocity(-speed)

def stop():
    left_motor.setVelocity(0)
    right_motor.setVelocity(0)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    #Accelerometer 
    accelValues=accel.getValues()
    print(accelValues)
    angle=getAngle(accelValues)
    print(angle)
    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    p=1
    #Motor
    speed=3
    
    #controller
    if angle>2:
        moveForward(speed)
    elif angle<-2:
        moveBackward(speed)
    else:
        stop()
    pass

# Enter here exit cleanup code.
