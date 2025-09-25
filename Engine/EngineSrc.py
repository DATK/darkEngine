import pygame as pg
import math
from copy import deepcopy,copy
import pickle
import sys
import random
import os
import threading
import Engine.EventListInfo as EventListInfo

class MapEditorObjectsBuffer():

    def __init__(self):
        self.objects=[]
        self.images=[]
        self.textBoxes=[]

    def Serialise(self):
        for obj in self.objects:
            obj.ForSerialization()
        for obj in self.images:
            obj.ForSerialization()
        for obj in self.textBoxes:
            obj.ForSerialization()    

    def DeSerialise(self):
        for obj in self.objects:
            obj.ForDeSerialization()
            obj.AfterLoadFromFile()
        for obj in self.images:
            obj.ForDeSerialization()
            obj.AfterLoadFromFile()
        for obj in self.textBoxes:
            obj.ForDeSerialization()  
            obj.AfterLoadFromFile()  


    def deleteObj(self,obj):
        if isinstance(obj,GameObject):
            self.objects.remove(obj)
        elif isinstance(obj,ImageObject):
            self.images.remove(obj)
        elif isinstance(obj,TextBox):
            self.textBoxes.remove(obj)



    def getObjects(self):
        tmp=[]
        tmp.extend(self.objects)
        tmp.extend(self.images)
        tmp.extend(self.textBoxes)
        return tmp

    def renderObjects(self,window):
        for obj in self.objects:
            if obj.Enabled and obj.Drawing:
                obj.Colider.update(obj.Position.x,obj.Position.y,obj.Sprite.get_width(),obj.Sprite.get_height())
                window.blit(obj.Sprite,(obj.Position.x,obj.Position.y))

    def renderImages(self,window):
        for img in self.images:
            if img.Enabled and img.Drawing:
                img.Update()
                window.blit(img.Sprite,(img.Position.x,img.Position.y))
    
    def renderTextBoxes(self,window):
        for txtBox in self.textBoxes:
            if txtBox.Enabled:
                window.blit(txtBox.surf,(txtBox.Position.x,txtBox.Position.y))

    def renderAll(self,window):
        self.renderImages(window)
        self.renderTextBoxes(window)
        self.renderObjects(window)
        

    
  

class MapEditor:
    
    def __init__(self,resolutinon=(640,480),flags=pg.DOUBLEBUF):
        resolutinon=(100+resolutinon[0],180+resolutinon[1])
        self.window = pg.display.set_mode(resolutinon,flags=flags)
        self.Clock=pg.time.Clock()
        self.SceneSurface=pg.Surface((resolutinon[0]*0.6,resolutinon[1]*0.85))
        self.ObjectsListSurfaces=pg.Surface((resolutinon[0]*0.2,resolutinon[1]*0.85))
        self.ObjectsListToAddSurfaces=pg.Surface((resolutinon[0]*0.2,resolutinon[1]*0.85))
        self.ScenesListSurface=pg.Surface((resolutinon[0],resolutinon[1]*0.15))
        self.frames=60
        self.targetObject=None
        self.targetColider=None
        self.mode=1
        self.New_project=True
        self.running=True
        self.Scences={"Default": [MapEditorObjectsBuffer(),[],[],[],[]]}
        self.objects=self.Scences["Default"][0]
        self.dumpObjects=self.Scences["Default"][1]
        self.rects_dmp=self.Scences["Default"][2]
        self.rects_obj=self.Scences["Default"][3]
        self.rects_scn=self.Scences["Default"][4]  
        self.rects_scns=[]
        self.targetScene="Default"
        self.defaultFont = pg.font.SysFont('Comic Sans MS', 14)
        self.Width,self.Hiegt=self.window.get_size()

        

    def setRes(self,resolutinon=(1280,720),flags=pg.DOUBLEBUF):
        resolutinon=(100+resolutinon[0],180+resolutinon[1])
        self.window = pg.display.set_mode(resolutinon,flags=flags)
        self.SceneSurface=pg.Surface((resolutinon[0]*0.6,resolutinon[1]*0.85))
        self.ObjectsListSurfaces=pg.Surface((resolutinon[0]*0.2,resolutinon[1]*0.85))
        self.ObjectsListToAddSurfaces=pg.Surface((resolutinon[0]*0.2,resolutinon[1]*0.85))
        self.ScenesListSurface=pg.Surface((resolutinon[0],resolutinon[1]*0.15))
        self.Width,self.Hiegt=self.window.get_size()
        
    def dump(self,object):
        self.dumpObjects.append(object)
            
    def DumpObjectsUpdate(self):
        cords=[5,10]
        text=self.defaultFont.render("Объекты для добавления",1,(255,20,20))
        self.ObjectsListToAddSurfaces.blit(text,cords)
        cords[1]+=18
        for i,obj in enumerate(self.dumpObjects):
            text=self.defaultFont.render(obj.GetName()+str(i+1),1,(0,0,0))
            self.rects_dmp.append((pg.Rect(cords[0],cords[1],text.get_width(),text.get_height()),obj))
            self.ObjectsListToAddSurfaces.blit(text,cords)
            cords[1]+=18
    
    def SetTargetScene(self,scene):
        self.objects=self.Scences[scene][0]
        self.dumpObjects=self.Scences["Default"][1]
        self.rects_dmp=self.Scences["Default"][2]
        self.rects_obj=self.Scences[scene][3]
        self.rects_scn=self.Scences[scene][4]
        self.targetScene=scene
            
    def ListbjectsUpdate(self):
        cords=[5,10]
        text=self.defaultFont.render("Объекты на сцене",1,(255,20,20))
        self.ObjectsListSurfaces.blit(text,cords)
        cords[1]+=18
        for i,obj in enumerate(self.objects.getObjects()):
            text=self.defaultFont.render(obj.GetName()+str(i+1),1,(0,0,0))
            self.rects_obj.append((pg.Rect(cords[0],cords[1],text.get_width(),text.get_height()),obj))
            self.ObjectsListSurfaces.blit(text,cords)
            cords[1]+=18

    def ListScencesUpdate(self):
        cords=[5,10]
        text=self.defaultFont.render("Сцены",1,(255,20,20))
        self.ScenesListSurface.blit(text,cords)
        cords[1]+=18
        for key in self.Scences:
            text=self.defaultFont.render(key,1,(0,0,0))
            self.rects_scns.append((pg.Rect(cords[0],cords[1],text.get_width(),text.get_height()),key))
            self.ScenesListSurface.blit(text,cords)
            if cords[0]>self.Width*0.87:
                cords[0]=5
                cords[1]+=18
                continue
            cords[0]+=text.get_width()+5
        text=self.defaultFont.render("AddScene",1,(150,0,0))
        self.rects_scns.append((pg.Rect(cords[0],cords[1],text.get_width(),text.get_height()),"AddScene"))
        self.ScenesListSurface.blit(text,cords)
    
    def chekScencesRects(self,pos):
        pos=(pos[0],pos[1]-self.Hiegt*0.85)
        for rct in self.rects_scns:
            if rct[0].collidepoint(pos):
                if rct[1] == "AddScene":
                    newSceneName="Scene" + str(len(self.Scences.keys())+1)
                    self.Scences[newSceneName]=[MapEditorObjectsBuffer(),[],[],[],[]]
                    return True
                self.SetTargetScene(rct[1])
                return True
        return False
    
    def chekDumpRects(self,pos):
        pos=(pos[0]-self.Width*0.8,pos[1])
        for rct in self.rects_dmp:
            if rct[0].collidepoint(pos):
                tmp=deepcopy(rct[1])
                tmp.Start()
                tmp.Position = Vector2(10,10)
                self.addToScene(tmp)
                return True
        return False
            
    def chekObjectsRects(self,pos):
        pos=(pos[0]-self.Width*0.2,pos[1])
        for rct in self.rects_scn:
            if rct[0].collidepoint(pos):
                self.targetObject=rct[1]
                self.targetColider=rct[0]
        return False
    
    
    def addToScene(self,target_object):
        if target_object:
            if isinstance(target_object,ImageObject):
                self.rects_scn.append((pg.Rect(target_object.Position.x/3,target_object.Position.y/4,target_object.Width/3,target_object.Height/4),target_object))
                self.objects.images.append(target_object)
                return
            elif isinstance(target_object,GameObject):
                self.objects.objects.append(target_object)
                self.rects_scn.append((pg.Rect(target_object.Position.x,target_object.Position.y,target_object.Width,target_object.Height),target_object))
            elif isinstance(target_object,TextBox):
                self.objects.textBoxes.append(target_object)
                self.rects_scn.append((pg.Rect(target_object.Position.x,target_object.Position.y,target_object.Width,target_object.Height),target_object))
                
    
    def LoadProject(self,file):
        with open(file,"rb") as f:
            data_objects=pickle.load(f)
        for key in data_objects:
            data_objects[key][0].DeSerialise()
        self.Scences=data_objects
        self.SetTargetScene("Default")
        
    def SaveProject(self,file):
        for key in self.Scences:
                self.Scences[key][0].Serialise()
        with open(file,"wb") as f:
            pickle.dump(self.Scences,f)
        for key in self.Scences:
                self.Scences[key][0].DeSerialise()

    def clsSurfaces(self,*args):
        self.SceneSurface.fill(args[0])
        self.ObjectsListSurfaces.fill(args[1])
        self.ObjectsListToAddSurfaces.fill(args[2])
        self.ScenesListSurface.fill(args[3])
    
    def removeFromScene(self):
        if self.targetObject!=None:
            self.objects.deleteObj(self.targetObject)
            self.rects_scn.remove((self.targetColider,self.targetObject))
          
    def MoveObject(self):
        if self.targetObject!=None:
            pos=pg.mouse.get_pos()
            pos=(pos[0]-self.Width*0.2,pos[1])
            self.targetObject.Position=Vector2(pos[0]-self.targetObject.Width/2,pos[1]-self.targetObject.Height/2)
            self.targetColider.update(self.targetObject.Position.x,self.targetObject.Position.y,self.targetObject.Width,self.targetObject.Height)
            #print(myindex)
            
    def reSize(self):
        if self.targetObject!=None:
            pos=pg.mouse.get_pos()
            pos=(pos[0]-self.Width*0.2,pos[1])
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.targetObject.Height-=0.5
            if keys[pg.K_DOWN]:
                self.targetObject.Height+=0.5
            if keys[pg.K_RIGHT]:
                self.targetObject.Width+=0.5
            if keys[pg.K_LEFT]:
                self.targetObject.Width-=0.5
                
            if self.targetObject.Width < 1:
                self.targetObject.Width=1
            if self.targetObject.Height < 1:
                self.targetObject.Height=1
                
            self.targetObject.updateSprite()
            self.targetColider.update(self.targetObject.Position.x,self.targetObject.Position.y,self.targetObject.Width,self.targetObject.Height)
            #print(myindex)
            
    def copyMode(self):
        if self.targetObject!=None:
            pos=pg.mouse.get_pos()
            pos=(pos[0]-self.Width*0.2,pos[1])
            tmp=copy(self.targetObject)
            self.addToScene(tmp)
            self.targetObject=None
            
    def removeMode(self):
        if self.targetObject!=None:
            pos=pg.mouse.get_pos()
            pos=(pos[0]-self.Width*0.2,pos[1])
            self.removeFromScene()
            self.targetObject=None
    
    def rotateMode(self):
         if self.targetObject!=None:
            pos=pg.mouse.get_pos()
            pos=(pos[0]-self.Width*0.2,pos[1])
            posObj = self.targetObject.Position
            self.targetObject.Rotate(0.05)
            self.targetObject.Position = posObj
            self.targetColider.update(self.targetObject.Position.x,self.targetObject.Position.y,self.targetObject.Width,self.targetObject.Height)
    
    
    
    def setEditMode(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_1]:
            self.mode=1
        elif keys[pg.K_2]:
            self.mode=2
        elif keys[pg.K_3]:
            self.mode=3
        elif keys[pg.K_4]:
            self.mode=4
        if keys[pg.K_5]:
            self.mode=5
       
            
    def saveProjectForEngine(self):
        for key in self.Scences:
            self.Scences[key][0].Serialise()
        scene={}
        for key in self.Scences:
            scene[key]=[self.Scences[key][0].objects,self.Scences[key][0].images,[],self.Scences[key][0].textBoxes,True]
        with open("GameData.desfM","wb") as f:
            pickle.dump(scene,f)
        for key in self.Scences:
            self.Scences[key][0].DeSerialise()
            
    def run(self):
        self.running=True
        while self.running:
            self.window.fill((0,0,0))
            self.clsSurfaces((10,10,10),(90,90,90),(90,90,90),(150,150,150))
           
            self.setEditMode()
            
            for event in pg.event.get():
                keys=pg.key.get_pressed()
                if event.type==pg.QUIT:
                    self.running=False
                buttons=pg.mouse.get_pressed()
                if  event.type==pg.MOUSEBUTTONDOWN and buttons[0]: 
                    pos=pg.mouse.get_pos()
                    if self.chekDumpRects(pos):
                        break
                    elif self.chekObjectsRects(pos):
                        break
                    elif self.chekScencesRects(pos):
                        break
                if  event.type==pg.MOUSEBUTTONUP: 
                    self.targetObject=None
                    self.targetColider=None
                
                if keys[pg.K_LCTRL] and keys[pg.K_s] and keys[pg.K_LSHIFT] and event.type==pg.KEYDOWN:
                    self.saveProjectForEngine()
                    print("GameProject Saved")
                
                elif keys[pg.K_LCTRL] and keys[pg.K_s] and event.type==pg.KEYDOWN:
                    self.SaveProject("ProjectScene.scnf")
                    print("Project Saved")
                
                    
            self.rects_dmp.clear()        
            self.rects_obj.clear()
            self.rects_scns.clear()
            #self.rects_scn.clear()
            
            self.DumpObjectsUpdate()
            self.ListbjectsUpdate()
            self.objects.renderAll(self.SceneSurface)
            self.ListScencesUpdate()
            
            if self. mode == 1: self.MoveObject()
            if self. mode == 2: self.reSize()
            if self. mode == 3: self.copyMode()
            if self. mode == 4: self.removeMode()
            if self. mode == 5: self.rotateMode()

            self.window.blit(self.ObjectsListSurfaces,(0,0))
            self.window.blit(self.SceneSurface,(self.Width*0.2,0))
            self.window.blit(self.ObjectsListToAddSurfaces,(self.Width*0.8,0))
            self.window.blit(self.ScenesListSurface,(0,self.Hiegt*0.85))
            
            self.Clock.tick(self.frames)
            name = self.targetObject.GetName() if self.targetObject!=None else ""
            pg.display.set_caption(f"Editor dev, fps {str(int(self.Clock.get_fps()))} | TARGET SCENE {self.targetScene} | TARGET OBJECT {name} | MODE {self.mode}")
            pg.display.flip()
        return self.objects
            
class Sound:

    def __init__(self,filename):
        '''Only .ogg or .wav sounds'''       
        self.sound = pg.mixer.Sound(filename)

    def play(self):
        self.sound.play()

    def change_volume(self,value):
        self.sound.set_volume(value)

    def get_info(self):
        return (self.sound.get_length(),self.sound.get_volume(),self.sound.get_num_channels(),self.sound.get_raw())

    def stop(self):
        self.sound.stop()
    

class ImageLoader:
    
    def __init__(self):
        pass
    
    def load(self,image,colorkey=[False,(0,0,0)],scale=(1,1)):
        image=f"{image}"
        res= os.path.splitext(image)
        if res==".png":
            surface = pg.image.load(image).convert_alfa()
        else:
            surface = pg.image.load(image).convert()
        if colorkey[0]:
            surface.set_colorkey((colorkey[1]))
        if scale!=(1,1):
            surface=pg.transform.scale(surface,size=(surface.get_width()*scale[0],surface.get_height()*scale[1]))
        return surface
        
    def load_bits(self,image_path):
        try:
            with open(image_path, "rb") as f:
                image=f.read()
        except:
            image=None
        return image

class Animation:      ####   НЕ  ГОТОВ ################################################### anim

    def __init__(self,objSelf):
        self.animationList = []
        self.run=False
        self.delayTime = 50
        self.objSelf=objSelf

    def loadSpriteList(self,name: str,sprites: list[str]):
        self.animationList.extend(sprites)

    def play(self):
        thread=threading.Thread(target=self._play)


    def _play(self):
        while self.run:
            for sprite in self.animationList:
                self.objSelf.Sprite=sprite
                self.objSelf.updateSprite
                pg.time.delay(self.delayTime)


    def playStop(self):
        self.run=not self.run

        

class Vector2:
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def normalise(self):
        if self.x != 0 or self.y !=0:
            inv_length = 1/(math.sqrt((self.x**2+self.y**2)))
            self.x *= inv_length
            self.y *= inv_length
            
    def getRandomDir(self):
        tmpX=random.randint(1,10)/10
        tmpY=random.randint(1,10)/10
        self.x=random.randint(-1,1)+tmpX
        self.y=random.randint(-1,1)+tmpY
    
    def nulling(self):
        self.x,self.y=0,0
    
    @staticmethod
    def GetRandomVector(xy_lim=(0,0,1000,1000)):
        x=random.randint(xy_lim[0],xy_lim[2])
        y=random.randint(xy_lim[1],xy_lim[3])
        return Vector2(x,y)
        
    
    def update(self,x: float,y: float):
        self.x=x
        self.y=y
    
    def updateWithVector(self,Vector):
        self.x,self.y=Vector.x,Vector.y
    
    def get_Difference(self,vecotr):
        return math.sqrt((self.x-vecotr.x)**2+(self.y-vecotr.y)**2)
    
    def __add__(self,other): 
        if isinstance(other,Vector2):
            x=self.x+other.x
            y=self.y+other.y
            return Vector2(x,y)
        elif isinstance(other,(float,int)):
            x=self.x+other
            y=self.y-other
            return Vector2(x,y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
    
    
    def __sub__(self,other):
        if isinstance(other,Vector2):
            x=self.x-other.x
            y=self.y-other.y
            return Vector2(x,y)
        elif isinstance(other,(float,int)):  
            x=self.x-other
            y=self.y-other
            return Vector2(x,y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
    
    def __mul__(self,other):
        if isinstance(other,Vector2):
            x=self.x*other.x
            y=self.y*other.y
            return Vector2(x,y)
        elif isinstance(other,(float,int)):
            x=self.x*other
            y=self.y*other
            return Vector2(x,y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
    
    def __div__(self,other):
        if isinstance(other,Vector2):
            x=self.x/other.x
            y=self.y/other.y
            return Vector2(x,y)
        elif isinstance(other,(float,int)):
            x=self.x/other
            y=self.y/other
            return Vector2(x,y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
        
    def __eq__(self, other):
        if isinstance(other,Vector2):
            if self.x==other.x and self.y==other.y:
                return True
        else:
            raise ArithmeticError("Правый операнд должен быть Vector2")

    def __str__(self):
        return f"({round(self.x,2)},{round(self.y,2)})"
    
class TextBox:

    def __init__(self,startPosition=Vector2(0,0),text="TextBox", aligin = "center",size=(5,5),font = 'Comic Sans MS',fontSize = 20, textColor = (255,0,0), alpha = 255,backColor=(0,0,0), delPhone=True):
        self.Width,self.Height=size
        self.surf = pg.Surface((self.Width,self.Height))
        self.Enabled=True
        self.colorSurf=backColor
        self.fontSize=fontSize
        self.Position = startPosition
        self.alpha=alpha
        self.text = text
        self.align = aligin
        self.font = pg.font.SysFont(font, self.fontSize)
        self.color = textColor
        self.surf.set_alpha(self.alpha)
        self.surf.fill(self.colorSurf)
        if delPhone:
            self.surf.set_colorkey(self.colorSurf)
        DarkEngine.LoadTextBox(self)
    

    def Start(self):
        self.render()
        return
    
    def ForSerialization(self):
        self.surf=pg.surfarray.array3d(self.surf)

        
    def ForDeSerialization(self):
        self.surf=pg.surfarray.make_surface(self.surf)

    def AfterLoadFromFile(self):
        return
    
    def LoadBack(self,image):
        self.surf= image
    
    def render(self):
        self.surf.fill(self.colorSurf)
        renderText = self.font.render(self.text,True,self.color)
        if self.align == "center":
            self.surf.blit(renderText,(self.Width/2-renderText.get_width()/2,self.Height/2-renderText.get_height()/2))
        elif self.align == "right":
            self.surf.blit(renderText,(self.Width-renderText.get_width(),self.Height/2-renderText.get_height()/2))
        elif self.align=="left":
            self.surf.blit(renderText,(0,self.Height/2-renderText.get_height()/2))



class ImageObject:
    
    def __init__(self,startPosition=Vector2(0,0)):
        self.Width=0
        self.Height=0
        self.Enabled=True
        self.Drawing=True
        self.ImageName="default image"
        self.angle=0
        self.Position = startPosition
        DarkEngine.LoadImage(self)
        
    def Load_Image(self,img: pg.Surface):
       self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
    
    def ColorImage(self,color):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Sprite.fill(color)
    
    def ForSerialization(self):
        self.Sprite=pg.surfarray.array3d(self.Sprite)
        
    def ForDeSerialization(self):
        self.Sprite=pg.surfarray.make_surface(self.Sprite)
    
    def GetName(self):
        return self.ImageName
    
    def Rotate(self,angle):
        self.angle+=angle
        self.Sprite=pg.transform.rotate(self.Sprite,self.angle)
    
    def Update(self):
        return
    
    def AfterLoadFromFile(self):
            return
    
    def Start(self):
        return 
    
    def updateSprite(self):
        self.Sprite=pg.transform.scale(self.Sprite,(self.Width,self.Height))

    
class GameObject:
    
    def __init__(self,startPosition=Vector2(0,0)):
        self.Width=0
        self.Height=0
        self.Enabled=True
        self.angle=0
        self.Position = startPosition
        self.Colider=pg.Rect(-1000,-1000,-1000,-1000)
        self.ColiderChek=False
        self.Drawing=False
        self.CanGarbage=True
        self.hasSprite=False
        self.GameObjectName="default object"
        DarkEngine.LoadObject(self)
        if DarkEngine.Running:
            self.Start()
          
    def OnGarbage(self):
        return

    def Resize(self,newWidth,newHight):
        self.Width = newWidth
        self.Height = newHight
        self.updateSprite()

    def Rotate(self,angle):
        self.angle+=angle


    def Set_Sprite(self,img):
        self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
        self.Colider.update(self.Sprite.get_rect(topleft=(self.Position.x,self.Position.y)))
        self.Drawing=True
        self.hasSprite=True
    
    def AddSelfColider(self):
        DarkEngine.LoadColider(self.Colider)
        self.ColiderChek=True
        
    def updateSprite(self):
        self.Sprite=pg.transform.scale(self.Sprite,(self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
    
    def Load_Sprite(self,color=(0,0,0)):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Sprite.fill(color)
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
        self.hasSprite=True
    
    def Start(self):
        return 
    
    def ForSerialization(self):
        if self.hasSprite:
            self.Sprite=pg.surfarray.array3d(self.Sprite)

    def ForDeSerialization(self):
        if self.hasSprite:
            self.Sprite=pg.surfarray.make_surface(self.Sprite)

    def AfterLoadFromFile(self):
        return
    
    def MovePosition(self,NewPosition: Vector2):
        self.Position.updateWithVector(NewPosition)
    
    def OnColliderCurrent(self,object):
        return False
    
    def GetName(self):
        return self.GameObjectName
    
    def Update(self):
        return

class GameObjectsGroup():

    def __init__(self,objects: list,startPositin = Vector2(0,0)):
        self.objects = objects
        self.Position = startPositin
        self.Colider=pg.Rect(-1000,-1000,-1000,-1000)
        self.ColiderChek=False
        self.Drawing=False
        self.Enabled=True
        self.angle=0
        self.Enabled=True
        self.CanGarbage=True
        self.hasSprite=False
        self.GameObjectName="default object"
        DarkEngine.LoadObject(self)

 



class CustomEvent:

    def __init__(self,function=None):
        self.event = pg.USEREVENT + DarkEngine.customeventsKoef
        self.function = function
        self.eventObject = pg.event.Event(self.event)
        DarkEngine.customeventsKoef += 1
        DarkEngine.AddEvent(self)
        
    def AddEventInQueue(self):
        pg.event.post(self.eventObject)

    def SetTimer(self,time: float):
        pg.time.set_timer(self.event,time)

    def StopTimer(self):
        pg.time.set_timer(self.event,0)
        

class Event():
    
    def __init__(self,type=pg.MOUSEBUTTONUP,function=None):
        self.event = type
        self.function = function
        DarkEngine.AddEvent(self)

    @staticmethod  
    def getEventsList():
        return EventListInfo.evnts



class DarkEngineLoop:
    
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 512)
        pg.init()
        self.flags = pg.DOUBLEBUF | pg.HWSURFACE
        self.window = pg.display.set_mode((1280,720),self.flags)
        self.Clock = pg.time.Clock()
        self.fps_max=240
        self.fps_now=144
        self.deltaTime=0
        self.ColiderListBuffer=[]
        self.GarbageList=[]
        self.IsInput=False
        self.InputText=""
        self.Running=True
        self.Scripts={}
        self.barrier=threading.Barrier(3)
        self.keys=pg.key.get_pressed()
        self.Scences={}
        self.AddScene("Default")
        self.LoadScene("Default")
        self.GarbageLimit = 150
        self.scriptPauseTime=200
        self.windowSize=self.window.get_size()
        self.defaultFont = pg.font.SysFont('Comic Sans MS', 25)
        self.TargetColiderFunction=self.ColiderChek_WithBufferOther
        self.customeventsKoef = 1
        self.eventList=[]
        

    
    def basicEvents(self):
        quitGame = Event(pg.QUIT,self.ExitEvent)
        self.startSceneEvent = CustomEvent(self.StopStartSceneEvent)
        self.startSceneEvent.SetTimer(2000)
        
        
    def ClearGarbage(self):
        self.GarbageList.clear()        
    
    def AddEvent(self,event):
        self.eventList.append(event)

    def LoadScene(self,scene):
        if scene in self.Scences:
            self.objects=self.Scences[scene][0]
            self.images=self.Scences[scene][1]
            self.coliderList=self.Scences[scene][2]   
            self.textBoxes=self.Scences[scene][3]
            self.targetScene=scene  
            self.changeScene=True

    def AddScene(self,scene_name):
        if scene_name not in self.Scences:
            self.Scences[scene_name] = [[],[],[],[],False]

    def addScript(self,name,function,enabled):
        self.Scripts[name]=[function,enabled]

    def onOffScript(self,name):
        self.Scripts[name][1]=not self.Scripts[name][1]
    
    def removeScript(self,name):
        del self.Scripts[name]
    
    def ClearColiderBufer(self):
        self.ColiderListBuffer.clear()
        
    def LoadObject(self,obj: object):
        self.objects.append(obj)

    def LoadTextBox(self,textBox: TextBox):
        self.textBoxes.append(textBox)

    def LoadImage(self,img):
        self.images.append(img)
        
    def LoadColider(self,rect):
        self.coliderList.append(rect)

    def setGarbageLimit(self,limit: int):
        self.GarbageLimit=limit

    def Set_icon(self,image):
        pg.display.set_icon(image)

    def Set_frame(self, fps):
        self.fps_max = fps
    
    def Set_caption(self,caption):
        pg.display.set_caption(caption)
    
    def Set_resolution(self,res,fullsceen=False):
        if fullsceen:
            self.flags = pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE
        self.window=pg.display.set_mode(res,self.flags)
        self.windowSize=self.window.get_size()
    
    def Set_resolutionCustom(self,res,flags):
        self.flags=flags
        self.window=pg.display.set_mode(res,self.flags)
        self.windowSize=self.window.get_size()
    
    def ExitEvent(self):
        self.Running = False
        self.barrier.abort()

    def StopStartSceneEvent(self):
        self.startSceneEvent.StopTimer()
        self.LoadScene(self.NextScene)

    def GarbageStore(self,obj):
        if not obj.CanGarbage:
            return True
        if -100<obj.Position.x<self.windowSize[0]+100 and -100<obj.Position.y<self.windowSize[1]+100:
            return True
        if self.GarbageLimit > 0 and  len(self.GarbageList) > self.GarbageLimit:
            self.GarbageList.clear()
        self.GarbageList.append(obj)
        self.objects.remove(obj)
        obj.Enabled=False
        if obj.Colider in self.coliderList:
            self.coliderList.remove(obj.Colider)
        obj.OnGarbage()
        return False
        
    def RemoveFromGarbage(self,obj: GameObject):
        if obj in self.GarbageList:
            obj.Enabled=True
            self.objects.append(obj)
            if obj.ColiderChek: self.coliderList.append(obj.Colider)
            self.GarbageList.remove(obj)
    
    def AddToGarbage(self,obj):
        if self.GarbageLimit > 0 and  len(self.GarbageList) > self.GarbageLimit:
            self.GarbageList.clear()
        self.GarbageList.append(obj)
        obj.Enabled=False
        if obj.Colider in self.coliderList:
            self.coliderList.remove(obj.Colider)
        obj.OnGarbage()
        self.objects.remove(obj)
    
    def InputStart(self):
        self.IsInput=True
    
    def InputStop(self):
        self.IsInput=False
        return self.InputText
    
    def InputClear(self):
        self.InputText=""

    def InputGet(self):
        return self.InputText
    
    def InputDelLast(self):
        self.InputText=self.InputText[0:len(self.InputText)-1]
    
    def startScene(self):
        self.AddScene("StartScene")
        self.LoadScene("StartScene")
        text="PyEngine"
        maintext = TextBox(Vector2(self.window.get_size()[0]/2-self.window.get_size()[0]*0.25,self.window.get_size()[1]/2-self.window.get_size()[1]*0.25),text=text,size=(self.window.get_size()[0]*0.5,self.window.get_size()[1]*0.5),textColor=(210,210,210),fontSize=80)
        maintext.render()
        pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))

    def LoadSceneFromFile(self,file):
        if os.path.splitext(file)[1]!=".desfM":
            return
        with open(file,"rb") as f:
            data = pickle.load(f)
        for key in data:
            for objList in data[key]:
                if objList==True:
                    break
                for obj in objList:
                    obj.ForDeSerialization()
                    obj.AfterLoadFromFile()
        self.Scences=data
        self.LoadScene("Default")

        
    
    def ColiderChek_WithBuffer(self,obj: GameObject):
        if obj in self.ColiderListBuffer:
            self.ColiderListBuffer.remove(obj)
            return
        self.ColiderListBuffer.append(obj)
        rect=obj.Colider.collidelistall(self.coliderList)
        myindex=self.coliderList.index(obj.Colider) 
        rect.remove(myindex)
        if rect!=[]:
            for i in rect:                                      # BAAD
                if obj.OnColliderCurrent(self.objects[i]):
                    self.objects[i].OnColliderCurrent(obj)
                    self.ColiderListBuffer.append(self.objects[i])
                    break
                if self.objects[i] in self.ColiderListBuffer:
                    self.ColiderListBuffer.remove(self.objects[i])
                    continue
                self.objects[i].OnColliderCurrent(obj)
                self.ColiderListBuffer.append(self.objects[i])
                    
                                        
    def ColiderChek_WithBufferOther(self,obj):
        if obj in self.ColiderListBuffer:
            self.ColiderListBuffer.remove(obj)
            return
        self.ColiderListBuffer.append(obj)
        for colider in self.objects:
            if colider==obj:
                continue
            # if colider in self.ColiderListBuffer:        # GOOD
            #     self.ColiderListBuffer.remove(colider)
            #     continue
            if not colider.ColiderChek:
                continue
            if obj.Colider.colliderect(colider.Colider):
                if obj.OnColliderCurrent(colider):
                    colider.OnColliderCurrent(obj)
                    break
                colider.OnColliderCurrent(obj)
                self.ColiderListBuffer.append(colider)

                
    def Set_WithBufferColiderChek(self):
        self.TargetColiderFunction=self.ColiderChek_WithBuffer
        self.ColiderListBuffer.clear()
    
    
   
    def Set_WithBufferColiderChekOther(self):
        self.TargetColiderFunction=self.ColiderChek_WithBufferOther
        self.ColiderListBuffer.clear()

        
    def renderObjects(self):
        for obj in self.objects:
            if obj.Enabled and obj.Drawing and self.GarbageStore(obj):
                sprite = pg.transform.rotate(obj.Sprite,obj.angle)
                obj.Colider.update(obj.Sprite.get_rect(center=(obj.Position.x,obj.Position.y)))
                rect = sprite.get_rect(center = obj.Colider.center)
                #pg.draw.rect(self.window,(250,25,123),obj.s)
                self.window.blit(sprite, rect)

    def renderImages(self):
        for img in self.images:
            if img.Enabled and img.Drawing:
                img.Update()
                self.window.blit(img.Sprite,(img.Position.x,img.Position.y))
    
    def renderTextBoxes(self):
        for txtBox in self.textBoxes:
            if txtBox.Enabled:
                self.window.blit(txtBox.surf,(txtBox.Position.x,txtBox.Position.y))

    def ThreadUpdateObjects(self):
        while self.Running:
            self.barrier.wait()
            for obj in self.objects:
                if obj.Enabled:
                    obj.Update()
    
    def ThreadCollidersObjectsHandler(self):
        while self.Running:
            self.barrier.wait()
            for obj in self.objects:
                if obj.Enabled and obj.ColiderChek:
                    self.TargetColiderFunction(obj)

    def ThreadScriptsRun(self):
        while self.Running:
            for key in self.Scripts:
                if self.Scripts[key][1]:
                    try:
                        self.Scripts[key][0]()
                    except Exception as ex:
                        print(f"Script {key} has Exception as {ex}")
            pg.time.delay(self.scriptPauseTime)

    def EventHandler(self):
        for event in pg.event.get():
            for cstevnet in self.eventList:
                if event.type == cstevnet.event:  
                    cstevnet.function()
            if self.IsInput and event.type==pg.KEYDOWN:
                if pg.key.get_pressed()[pg.K_BACKSPACE]:
                    self.InputDelLast()
                    continue
                elif pg.key.get_pressed()[pg.K_RETURN]:
                    continue
                self.InputText+=event.unicode
    
    def InitialiesObject(self):
        if not self.Scences[self.targetScene][4]:
            for img in self.images:
                img.Start()
            for obj in self.objects:
                obj.Start()
            for txtb in self.textBoxes:
                txtb.Start()
            self.Scences[self.targetScene][4] = True


    def run(self):
        self.Running=True
        self.NextScene=self.targetScene
        self.startScene() 
        threads = [threading.Thread(target=self.ThreadUpdateObjects,daemon=True), \
                                 threading.Thread(target=self.ThreadCollidersObjectsHandler,daemon=True), \
                                 threading.Thread(target=self.ThreadScriptsRun,daemon=True)] 
       

        [thread.start() for thread in threads]

        self.InitialiesObject()

        self.basicEvents()

        while self.Running:
            self.InitialiesObject()
            self.keys=pg.key.get_pressed()
           # self.deltaTime=self.Clock.get_time()/10
            self.window.fill((0,0,0))

            self.EventHandler()
            self.barrier.wait()
            self.renderImages()
            self.renderObjects()
            self.renderTextBoxes()
  
            
            text=self.defaultFont.render(str(int(self.Clock.get_fps())),True,(255,255,255))############# TMP ПОТОМ УДАЛИТЬ
            self.window.blit(text,(0,0))   
                                                            ############# TMP ПОТОМ УДАЛИТЬ
            

            self.deltaTime  = self.Clock.tick(self.fps_max) * 0.1
            pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))
        [thread.join() for thread in threads]
        sys.exit()


DarkEngine = DarkEngineLoop()
