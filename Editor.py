from Engine.EngineSrc import MapEditor
from Objects import Player,LabBlock,Phone

editor=MapEditor()

editor.dump(Player())
editor.dump(Phone())
editor.dump(LabBlock())


editor.setRes((1100,600))
editor.LoadProject("ProjectScene.scnf")

editor.run() 

