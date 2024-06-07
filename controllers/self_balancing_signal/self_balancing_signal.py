from controller import Robot
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
# for communication over files
import socket
import json
#to automatically start the visualization 
import subprocess
import os
import signal

# Start the visualization script
visualization_process = subprocess.Popen(['python3', 'visualize_signals.py'])
# Function to generate step signal
def step_signal(t, step_time, initial_value, final_value):
    return initial_value if t < step_time else final_value

plt.clf()
# Initialize the Robot
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


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

# Define motor objects
left_motor = robot.getDevice('left_wheel')
right_motor = robot.getDevice('right_wheel')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Set initial velocity to 0
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Signal parameters
step_time = 1.0  # seconds
initial_value = 0.0  # rad/s
final_value = 2.0  # rad/s

# Set up socket communication
server_address = ('localhost', 65432)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



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
    
p=0.4
error=0
try: 
    start_time = robot.getTime()
    while robot.step(timestep) != -1:
        current_time = robot.getTime() - start_time
        
        accelValues=accel.getValues()
        # print(accelValues)
        angle=getAngle(accelValues)
        # print(angle)
        # Generate step signal for velocity
        # velocity = step_signal(current_time, step_time, initial_value, final_value)
    
        # Apply velocity to motors
        # left_motor.setVelocity(velocity)
        # right_motor.setVelocity(velocity)
        
        
        
        #Motor
        speed=p*error
        
        #controller
        if angle>2:
            error=angle
            speed=p*error
            moveForward(speed)
        elif angle<-2:
            error=angle
            speed=p*error
            moveForward(speed)
        else:
            error=0
            stop()
    
        # Get robot position
        # left_position = left_motor.getTargetPosition()
        # right_position = right_motor.getTargetPosition()
    
        # Prepare data for sending
        data = {
            'time': current_time,
            'velocity': speed,
            'tilt_angle': angle
        }
        
        
        # Send data
        sock.sendto(json.dumps(data).encode(), server_address)
      
    
        if current_time > step_time + 5:  # Run the simulation for a total of 15 seconds
            break
finally:
    # Terminate the visualization process when the simulation ends or is interrupted
    visualization_process.terminate()
    sock.close()