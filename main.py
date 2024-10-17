import zmq
import sys
from ctypes import CDLL
from os import path

# Initialize ZMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.PULL)

# Bind socket to the specified port
try:
    socket.bind("tcp://*:12345")
    print("ZMQ: Bound to tcp://*:12345")
except zmq.ZMQError as e:
    print(f"ZMQ Error during binding: {e}")
    sys.exit(1)

# GhubMouse class to interface with the DLL
class GhubMouse:
    def __init__(self):
        self.basedir = path.dirname(path.abspath(__file__))
        self.dlldir = path.join(self.basedir, 'ghub_mouse.dll')
        self.gm = CDLL(self.dlldir)
        self.mouse_open = self.gm.mouse_open()
    def mouse_xy(self, x, y):
        if self.mouse_open:
            self.gm.moveR(x, y)
    def mouse_down(self, key=1):
        if self.mouse_open:
            self.gm.press(key)
    def mouse_up(self):
        if self.mouse_open:
            return self.gm.release()

try:
    gHub = GhubMouse()
except Exception as e:
    print(f"Failed to initialize GhubMouse: {e}")
    sys.exit(1)

def move_crosshair(x, y):
    gHub.mouse_xy(int(x), int(y))

def click():
    gHub.mouse_down()
    gHub.mouse_up()
# Main loop to receive messages and move the crosshair
gHub.mouse_xy(10, 10)
try:
    print("Waiting for incoming messages...")
    while True:
        
        message = socket.recv_string()
        # print(message)
        if message == "click":
            click()
        else:
            x, y = map(int, message.split(','))
            # print(message)
            move_crosshair(x, y)
except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Exiting...")
finally:
    socket.close()
    context.term()
    sys.exit()


