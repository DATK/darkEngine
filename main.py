from Engine.EngineSrc import DarkEngine, CustomEvent,Event
from objects import *
from settings import RESOLUTION,FULLSCREEN,CAPTION,FRAME
import random as r






DarkEngine.Set_caption(CAPTION)
DarkEngine.Set_resolution(RESOLUTION,FULLSCREEN)
DarkEngine.Set_frame(FRAME)

# M = Map(size=58,startPos=(1.5,9))



#DarkEngine.Set_WithBufferColiderChek()
DarkEngine.run()

