import pygame as pg
import math
from copy import deepcopy,copy
import pickle
import sys
import random
import os
import numpy as np


class MapEditor:
    
    def __init__(self,resolutinon=(640,480),flags=pg.DOUBLEBUF):
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
        self.Scences={"Default": [[],[],[],[],[],[]]}
        self.objects=self.Scences["Default"][0]
        self.images=self.Scences["Default"][1]
        self.dumpObjects=self.Scences["Default"][2]
        self.rects_dmp=self.Scences["Default"][3]
        self.rects_obj=self.Scences["Default"][4]
        self.rects_scn=self.Scences["Default"][5]
        self.rects_scns=[]
        self.targetScene="Default"
        self.defaultFont = pg.font.SysFont('Comic Sans MS', 14)
        self.Width,self.Hiegt=self.window.get_size()
        

    def setRes(self,resolutinon=(1280,720),flags=pg.DOUBLEBUF):
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
        for i,obj in enumerate(self.dumpObjects):
            text=self.defaultFont.render(obj.GetName()+str(i+1),1,(0,0,0))
            self.rects_dmp.append((pg.Rect(cords[0],cords[1],text.get_width(),text.get_height()),obj))
            self.ObjectsListToAddSurfaces.blit(text,cords)
            cords[1]+=18
    
    def SetTargetScene(self,scene):
        self.objects=self.Scences[scene][0]
        self.images=self.Scences[scene][1]
        self.dumpObjects=self.Scences["Default"][2]
        self.rects_dmp=self.Scences["Default"][3]
        self.rects_obj=self.Scences[scene][4]
        self.rects_scn=self.Scences[scene][5]
        self.targetScene=scene
            
    def ListbjectsUpdate(self):
        cords=[5,10]
        for i,obj in enumerate(self.objects):
            text=self.defaultFont.render(obj.GetName()+str(i+1),1,(0,0,0))
            self.rects_obj.append((pg.Rect(cords[0],cords[1],text.get_width(),text.get_height()),obj))
            self.ObjectsListSurfaces.blit(text,cords)
            cords[1]+=18
    
    def ListScencesUpdate(self):
        cords=[5,10]
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
                    self.Scences[newSceneName]=[[],[],[],[],[],[]]
                    return True
                self.SetTargetScene(rct[1])
                return True
        return False
    
    def chekDumpRects(self,pos):
        pos=(pos[0]-self.Width*0.8,pos[1])
        for rct in self.rects_dmp:
            if rct[0].collidepoint(pos):
                tmp=deepcopy(rct[1])
                tmp.Awake()
                self.addToScene(tmp)
                return True
        return False
            
    def chekObjectsRects(self,pos):
        pos=(pos[0]-self.Width*0.2,pos[1])
        for rct in self.rects_scn:
            if rct[0].collidepoint(pos):
                self.targetObject=rct[1]
                self.targetColider=rct[0]
                return True
        return False
    
    
    def addToScene(self,target_object):
        if target_object:
            if isinstance(target_object,ImageObject):
                self.images.append(target_object)
                return
            self.objects.append(target_object)
            self.rects_scn.append((pg.Rect(target_object.Position.x,target_object.Position.y,target_object.Width,target_object.Height),target_object))
    
    def LoadProject(self,file):
        self.objects=[]
        self.images=[]
        self.dumpObjects=[]
        self.rects_dmp=[]
        self.rects_obj=[]
        self.rects_scn=[]
        with open(file,"rb") as f:
            data_objects=pickle.load(f)
        for key in data_objects:
            for obj in data_objects[key][0]:
                obj.ToReadFile()
            for img in data_objects[key][1]:
                img.ToReadFile()
        self.Scences=data_objects
        self.SetTargetScene("Default")
        self.New_project=False
        
    def SaveProject(self,file):
        for key in self.Scences:
            for obj in self.Scences[key][0]:
                obj.ToWriteFile()
            for img in self.Scences[key][1]:
                img.ToWriteFile()
        with open(file,"wb") as f:
            pickle.dump(self.Scences,f)
        for key in self.Scences:
            for obj in self.Scences[key][0]:
                obj.ToReadFile()
            for img in self.Scences[key][1]:
                img.ToReadFile()

    def clsSurfaces(self,*args):
        self.SceneSurface.fill(args[0])
        self.ObjectsListSurfaces.fill(args[1])
        self.ObjectsListToAddSurfaces.fill(args[2])
        self.ScenesListSurface.fill(args[3])
    
    def removeFromScene(self):
        if self.targetObject!=None:
            self.objects.remove(self.targetObject)
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
    
    def ObjectDrawer(self):
        for img in self.images:
            if img.Enabled:
                    if img.Drawing:
                        self.SceneSurface.blit(img.Sprite,(img.Position.x,img.Position.y))
        
        for obj in self.objects:
                if obj.Enabled:
                    if obj.Drawing:
                        self.SceneSurface.blit(obj.Sprite,(obj.Position.x,obj.Position.y))
    
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
            print(self.targetScene)
       
            
    def saveProjectForEngine(self):
        for key in self.Scences:
            for obj in self.Scences[key][0]:
                obj.ToWriteFile()
            for img in self.Scences[key][1]:
                img.ToWriteFile()
        scene={}
        for key in self.Scences:
            scene[key]=[self.Scences[key][0],self.Scences[key][1],[]]
        with open("ToEnineGameData.pkl","wb") as f:
            pickle.dump(scene,f)
        for key in self.Scences:
            for obj in self.Scences[key][0]:
                obj.ToReadFile()
            for img in self.Scences[key][1]:
                img.ToReadFile()
            
    def run(self):
        self.running=True
        if self.New_project:
            for obj in self.objects:
                obj.Awake()
        while self.running:
            self.window.fill((0,0,0))
            self.clsSurfaces((10,10,10),(90,90,90),(90,90,90),(150,150,150))
            
            self.setEditMode()
            
            for event in pg.event.get():
                keys=pg.key.get_pressed()
                if event.type==pg.QUIT:
                    self.running=False
                if  event.type==pg.MOUSEBUTTONDOWN: 
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
                    self.SaveProject("ProjectScene.pkl")
                    print("Project Saved")
                
                    
            self.rects_dmp.clear()        
            self.rects_obj.clear()
            self.rects_scns.clear()
            #self.rects_scn.clear()
            
            self.DumpObjectsUpdate()
            self.ListbjectsUpdate()
            self.ObjectDrawer()
            self.ListScencesUpdate()
            
            if self. mode == 1: self.MoveObject()
            if self. mode == 2: self.reSize()
            if self. mode == 3: self.copyMode()
            if self. mode == 4: self.removeMode()

            self.window.blit(self.ObjectsListSurfaces,(0,0))
            self.window.blit(self.SceneSurface,(self.Width*0.2,0))
            self.window.blit(self.ObjectsListToAddSurfaces,(self.Width*0.8,0))
            self.window.blit(self.ScenesListSurface,(0,self.Hiegt*0.85))
            
            self.Clock.tick(self.frames)
            pg.display.set_caption(f"Editor dev, fps {str(int(self.Clock.get_fps()))}")
            pg.display.flip()
        return self.objects
            
    
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
    
    @property
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
    

class ImageObject:
    
    def __init__(self,startPosition=(0,0)):
        self.Width=0
        self.Height=0
        self.Enabled=True
        self.Drawing=True
        self.ImageName="default image"
        self.Position = Vector2(startPosition[0],startPosition[1])
        DarkEngine.LoadImage(self)
        
    def Load_Image(self,img: pg.Surface):
       self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
    
    def ColorImage(self,color):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Sprite.fill(color)
    
    def ToWriteFile(self):
        self.Sprite=pg.surfarray.array3d(self.Sprite)
        
    def ToReadFile(self):
        self.Sprite=pg.surfarray.make_surface(self.Sprite)
    
    def GetName(self):
        return self.ImageName
    
    def Update(self):
        if self.Drawing:
            DarkEngine.window.blit(self.Sprite,(self.Position.x,self.Position.y))
    
    def Awake(self):
        return
    
    def Start(self):
        return 
    
    def updateSprite(self):
        self.Sprite=pg.transform.scale(self.Sprite,(self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())

    
class GameObject:
    
    
    def __init__(self,startPosition=(0,0)):
        self.Width=0
        self.Height=0
        self.Enabled=True
        self.Position = Vector2(startPosition[0],startPosition[1])
        self.Colider=pg.Rect(-1000,-1000,-1000,-1000)
        self.ColiderChek=False
        self.Drawing=False
        self.CanGarbage=True
        self.hasSprite=False
        self.GameObjectName="default object"
        DarkEngine.LoadObject(self)
          
    def OnGarbage(self):
        return
    
    def Rotation(self,angle):
        self.Sprite=pg.transform.rotate(self.Sprite,angle)
    
    def Set_Sprite(self,img):
        self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
        self.hasSprite=True
    
    def AddSelfColider(self):
        DarkEngine.LoadColider(self.Colider)
        self.ColiderChek=True
        
    def updateSprite(self):
        self.Sprite=pg.transform.scale(self.Sprite,(self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
    
    def Load_Sprite(self):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
        self.hasSprite=True
    
    def Start(self):
        return 
    
    def Awake(self):
        return
    
    def ToWriteFile(self):
        if self.hasSprite:
            self.Sprite=pg.surfarray.array3d(self.Sprite)

        
    def ToReadFile(self):
        if self.hasSprite:
            self.Sprite=pg.surfarray.make_surface(self.Sprite)
    
    def MovePosition(self,NewPosition: Vector2):
        self.Position.updateWithVector(NewPosition)
    
    def OnColliderCurrent(self,object):
        return False
    
    def GetName(self):
        return self.GameObjectName
    
    def Update(self):
        if self.Drawing:
            #self.Colider=pg.Rect(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
            self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
            DarkEngine.window.blit(self.Sprite,(self.Position.x,self.Position.y))
               

class DarkEngineLoop:
    
    def __init__(self):
        pg.init()
        self.flags = pg.DOUBLEBUF 
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
        self.keys=pg.key.get_pressed()
        self.Scences={"Default":[[],[],[]]}
        self.objects=self.Scences["Default"][0]
        self.images=self.Scences["Default"][1]
        self.coliderList=self.Scences["Default"][2]
        self.targetScene="Default"
        self.windowSize=self.window.get_size()
        self.defaultFont = pg.font.SysFont('Comic Sans MS', 25)
        self.TargetColiderFunction=self.ColiderChek_WithBufferOther
        
    def ClearGarbage(self):
        self.GarbageList.clear()
        
    def LoadScene(self,scene):
        self.objects=self.Scences[scene][0]
        self.images=self.Scences[scene][1]
        self.coliderList=self.Scences[scene][2]   
        self.targetScene=scene     
    
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

    def LoadImage(self,img):
        self.images.append(img)
        
    def LoadColider(self,rect):
        self.coliderList.append(rect)

    def Set_icon(self,image):
        pg.display.set_icon(image)

    def Set_frame(self, fps):
        self.fps_max = fps
    
    def Set_caption(self,caption):
        pg.display.set_caption(caption)
    
    def Set_resolution(self,res,fullsceen=False):
        if fullsceen:
            self.flags = pg.FULLSCREEN | pg.DOUBLEBUF
        self.window=pg.display.set_mode(res,self.flags)
        self.windowSize=self.window.get_size()
    
    def Set_resolutionCustom(self,res,flags):
        self.flags=flags
        self.window=pg.display.set_mode(res,self.flags)
        self.windowSize=self.window.get_size()
    
    def GarbageStore(self,obj):
        if not obj.CanGarbage:
            return True
        if -100<obj.Position.x<self.windowSize[0]+100 and -100<obj.Position.y<self.windowSize[1]+100:
            return True
        self.GarbageList.append(obj)
        self.objects.remove(obj)
        if obj.Colider in self.coliderList:
            self.coliderList.remove(obj.Colider)
        obj.OnGarbage()
        return False
        
    def RemoveFromGarbage(self,obj: GameObject):
        if obj in self.GarbageList:
            self.objects.append(obj)
            if obj.ColiderChek: self.coliderList.append(obj.Colider)
            self.GarbageList.remove(obj)
    
    def AddToGarbage(self,obj):
        self.GarbageList.append(obj)
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
        self.window.fill((0,0,0))
        font = pg.font.SysFont('Comic Sans MS', 140)
        font2 = pg.font.SysFont('Comic Sans MS', 100)
        text = font.render("PyEngine",True,(255,255,255))
        text2 = font2.render("by Python3",True,(255,255,255))
        self.window.blit(text,(self.windowSize[0]*0.2,self.windowSize[1]*0.2))
        self.window.blit(text2,(self.windowSize[0]*0.2,self.windowSize[1]*0.45))
        pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))
        pg.time.wait(2000)
    
    
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
            if colider in self.ColiderListBuffer:        # GOOD
                self.ColiderListBuffer.remove(colider)
                continue
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
    
    
    def LoadSceneFromEditor(self,file):
        self.objects=[]
        self.coliderList=[]
        self.ColiderListBuffer=[]
        self.GarbageList=[]
        self.ColiderListBuffer=[]
        with open(file,"rb") as f:
            data_objects=pickle.load(f)
        for key in data_objects:
            for obj in data_objects[key][0]:
                obj.ToReadFile()
                obj.Start()
            for img in data_objects[key][1]:
                img.ToReadFile()
        self.Scences=data_objects
        self.LoadScene("Default")
    
    def Set_WithBufferColiderChekOther(self):
        self.TargetColiderFunction=self.ColiderChek_WithBufferOther
        self.ColiderListBuffer.clear()
        
    def run(self):
        self.Running=True
        self.startScene()  
        for img in self.images:
            img.Start()
        for obj in self.objects:
            obj.Start()
        while self.Running:
            self.keys=pg.key.get_pressed()
            self.deltaTime=self.Clock.get_time()/100
            self.window.fill((0,0,0))
        
            for key in self.Scripts:
                if self.Scripts[key][1]:
                    self.Scripts[key][0]()
               
            for imgI in np.arange(len(self.images)):
                if self.images[imgI].Enabled:
                    self.images[imgI].Update()
            
            for obj in self.objects:
                if obj.Enabled and self.GarbageStore(obj):
                    obj.Update()
                    if obj.ColiderChek: self.TargetColiderFunction(obj)

            for event in pg.event.get():
                if event.type==pg.QUIT:
                    self.Running = False
                elif self.InputText:
                    if event.type==pg.KEYDOWN:
                        self.InputText+=event.unicode
                    
            text=self.defaultFont.render(str(int(self.Clock.get_fps())),True,(255,255,255))############# TMP ПОТОМ УДАЛИТЬ
            self.window.blit(text,(0,0))                                                   ############# TMP ПОТОМ УДАЛИТЬ
            self.Clock.tick(self.fps_max)
            pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))
        sys.exit()

DarkEngine = DarkEngineLoop()
