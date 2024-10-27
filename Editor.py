from Engine.EngineSrc import MapEditor,DarkEngine,Vector2
from Objects import Player,LabBlock,Phone,Loger,gen_lab

editor=MapEditor()

editor.dump(Player())
editor.dump(Phone())
editor.dump(LabBlock())


editor.setRes()
# editor.LoadProject("ProjectScene.pkl")

editor.run() 

