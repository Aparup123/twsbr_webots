import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket
import json

# Set up socket communication
server_address = ('localhost', 65432)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(server_address)

# Lists to store data
time = []
velocity = []
tilt_angle = []


# Set up the figure and subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Initialize the plots
line1, = ax1.plot([], [], label='Input Velocity')
line2, = ax2.plot([], [], label='Tilt Angle')


def init():
    
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Velocity (rad/s)')
    ax1.set_title('Input Velocity Signal')
    ax1.legend()

    
     # Adjust based on expected tilt angle range
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Tilt Angle (deg)')
    ax2.set_title('Robot Tilt Angle')
    ax2.legend()

    return line1, line2

def update(frame):
    data, _ = sock.recvfrom(1024)
    data = json.loads(data)

    time.append(data['time'])
    velocity.append(data['velocity'])
    tilt_angle.append(data['tilt_angle'])

    line1.set_data(time, velocity)
    line2.set_data(time, tilt_angle)

    ax1.relim()
    ax1.autoscale_view()

    ax2.relim()
    ax2.autoscale_view()

    return line1, line2

ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=32)

plt.tight_layout()
plt.show()
