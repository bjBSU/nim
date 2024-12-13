import sys, os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

os.environ['RETICO'] = 'retico-core'
os.environ['RETICOV'] = 'retico-vision'
os.environ['MISTY'] = 'retico-mistyrobot'
os.environ['MISTYSUB'] = 'mistypy'
os.environ['CLIP'] = 'retico-clip'
os.environ['YOLOV8'] = 'retico-yolov8'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['MISTY'])
sys.path.append(os.environ['MISTYSUB'])
sys.path.append(os.environ['YOLOV8'])


from retico_core import *
from retico_core.debug import DebugModule
from retico_mistyrobot.misty_camera import MistyCameraModule
from mistypy.Robot import Robot
from retico_vision import ExtractObjectsModule
from retico_yolov8 import Yolov8
from retico_nim import NimModule

ip = "192.168.0.101"
robot = Robot(ip)
webcam = MistyCameraModule(ip)
debug = DebugModule()  
vision = ExtractObjectsModule(save=True)
nim = NimModule(ip)
yolo = Yolov8()

webcam.subscribe(yolo)
yolo.subscribe(vision)
vision.subscribe(nim)
nim.subscribe(debug)

webcam.run()
yolo.run()
vision.run()
nim.run()
debug.run() 

robot.move_head(pitch=100)
print("running now!")
input()

webcam.stop()  
yolo.stop()
vision.stop()
nim.stop()
debug.stop()  