import pygame as pg
import math
import random
import os
import numpy as np

 
 
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
    
    def update(self,x: float,y: float):
        self.x=x
        self.y=y
    
    def updateWithVector(self,Vector):
        self.x,self.y=Vector.x,Vector.y
    
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
        self.Position = Vector2(startPosition[0],startPosition[1])
        
    def Load_Image(self,img: pg.Surface):
       self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
    
    def Update(self):
        DarkEngine.window.blit(self.Sprite,(self.Position.x,self.Position.y))
        
    def Start(self):
        return 

    
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
        
    def OnGarbage(self):
        return
    
    def Rotation(self,angle):
        self.Sprite=pg.transform.rotate(self.Sprite,angle)
    
    def Set_Sprite(self,img):
        self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
    
    def AddSelfColider(self):
        DarkEngine.LoadColider(self.Colider)
        self.ColiderChek=True
        
    
    def Load_Sprite(self):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Colider.update(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
    
    def Start(self):
        return 
    
    def MovePosition(self,NewPosition: Vector2):
        self.Position.updateWithVector(NewPosition)
    
    def OnColliderCurrent(self,object):
        return False
    
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
        self.objects=[]
        self.images=[]
        self.coliderList=[]
        self.ColiderListBuffer=[]
        self.keys=pg.key.get_pressed()
        self.windowSize=self.window.get_size()
        self.defaultFont = pg.font.SysFont('Comic Sans MS', 25)
        self.TargetColiderFunction=self.ColiderChek_Default
        self.GarbageList=[]
        
        #16120
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
    
    def ColiderChek_Default(self,obj: GameObject):
        rect=obj.Colider.collidelistall(self.coliderList)
        myindex=self.coliderList.index(obj.Colider)  
        #myindexrect=self.coliderList.index(obj.Colider)  
        rect.remove(myindex)
        if rect!=[]:
            for i in rect:
                if obj.OnColliderCurrent(self.objects[i]):
                    break
                
    def ColiderChek_WithBuffer(self,obj: GameObject):
        if obj in self.ColiderListBuffer:
            self.ColiderListBuffer.remove(obj)
            return
        rect=obj.Colider.collidelistall(self.coliderList)
        myindex=self.coliderList.index(obj.Colider) 
        rect.remove(myindex)
        if rect!=[]:
            for i in rect:
                if obj.OnColliderCurrent(self.objects[i]):
                    break
            self.ColiderListBuffer.append(obj)
            for i in rect:
                if self.objects[i] not in self.ColiderListBuffer:
                    self.objects[i].OnColliderCurrent(obj)  
                    self.ColiderListBuffer.append(self.objects[i])
                    
    def ColiderChek_WithoutBuffer(self,obj: GameObject):
        rect=obj.Colider.collidelistall(self.coliderList)
        myindex=self.coliderList.index(obj.Colider)
        rect.remove(myindex)
        if rect!=[]:
            for i in rect:
                if obj.OnColliderCurrent(self.objects[i]):
                    break
            for i in rect:
                    self.objects[i].OnColliderCurrent(obj)  

                
    def Set_DefaultColiderFunc(self):
        self.TargetColiderFunction=self.ColiderChek_Default
        self.ColiderListBuffer.clear()
        
    def Set_WithBufferColiderChek(self):
        self.TargetColiderFunction=self.ColiderChek_WithBuffer
        self.ColiderListBuffer.clear()
        
    def Set_WithOutBufferColiderChek(self):
        self.TargetColiderFunction=self.ColiderChek_WithoutBuffer
        self.ColiderListBuffer.clear()
    
    def run(self):
        self.startScene()  
        for img in self.images:
            img.Start()
        for obj in self.objects:
            obj.Start()
        while True:
            self.keys=pg.key.get_pressed()
            self.deltaTime=self.Clock.get_time()/100
            self.window.fill((0,0,0))
                                     
            for imgI in np.arange(len(self.images)):
                if self.images[imgI].Enabled:
                    self.images[imgI].Update()
            
            for obj in self.objects:
                if obj.Enabled and self.GarbageStore(obj):
                    obj.Update()
                    if obj.ColiderChek: self.TargetColiderFunction(obj)

            
            [pg.quit() for event in pg.event.get() if event.type==pg.QUIT]
                    
            text=self.defaultFont.render(str(int(self.Clock.get_fps())),True,(255,255,255))############# TMP ПОТОМ УДАЛИТЬ
            self.window.blit(text,(0,0))                                                   ############# TMP ПОТОМ УДАЛИТЬ
            self.Clock.tick(self.fps_max)
            pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))




DarkEngine = DarkEngineLoop()
