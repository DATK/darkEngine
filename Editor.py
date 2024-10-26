from Engine.EngineSrc import MapEditor
from Objects import Player,LabBlock,Phone

editor=MapEditor()

editor.dump(Player())
editor.dump(Phone())
editor.dump(LabBlock())
editor.setRes((1920,1000))
#editor.LoadProject("ProjectScene.pkl")
editor.run()