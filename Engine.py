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
        self.x=random.randint(-1,1)
        self.y=random.randint(-1,1)
        
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
    
    

    
class GameObject:
    
    def __init__(self):
        self.Width=0
        self.Height=0
        self.Enabled=True
        self.Position = Vector2(0,0)
        self.Colider=pg.Rect(-1000,-1000,-1000,-1000)
        self.Drawing=False
        
    def Rotation(self,angle):
        self.Sprite=pg.transform.rotate(self.Sprite,angle)
    
    def Set_Sprite(self,img):
        self.Sprite=pg.transform.scale(img,(self.Width,self.Height))
        self.Colider=pg.Rect(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
    
    def Load_Sprite(self):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Colider=pg.Rect(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        self.Drawing=True
    
    def Start(self):
        return 
    
    def MovePosition(self,NewPosition: Vector2):
        self.Position.x=NewPosition.x
        self.Position.y=NewPosition.y
    
    def OnColliderCurrent(self,object):
        if self.Drawing and self.Enabled and self.Colider.colliderect(object.Colider):
            return True
    
    def Update(self):
        if self.Drawing:
            self.Colider=pg.Rect(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
            DarkEngine.window.blit(self.Sprite,(self.Position.x,self.Position.y))

class Player(GameObject):
    
    def Start(self):
        self.Position=Vector2(200,200)
        self.speed=8
        self.Height=50
        self.rot=False
        self.Width=50
        self.Set_Sprite(imageload.load("hero.png",colorkey=[1,(255,255,255)]))
        super().Start()
    
    def OnColliderCurrent(self, colider):
        if super().OnColliderCurrent(colider):
            self.x,self.y=0,0
   
    
    def Movement(self):
        keys=DarkEngine.keys
        inputVector = Vector2(0,0)
        if keys[pg.K_w]:
            inputVector.y-=1
        if keys[pg.K_s]:
            inputVector.y+=1
        if keys[pg.K_a]:
           inputVector.x-=1
        if keys[pg.K_d]:
            inputVector.x+=1
        inputVector.normalise()
        self.MovePosition(self.Position+inputVector*(self.speed*DarkEngine.deltaTime))

    
    def Update(self):
        self.Movement()
        super().Update()

    
class tmpObject(GameObject):
    
    def Start(self):
        self.Position=Vector2(300,300)
        self.Width=120
        self.Height=110
        self.Enabled=True
        self.gen_point()
        self.speed=random.randint(2,20)
        self.Set_Sprite(imageload.load("enemy2.png",colorkey=[1,(255,255,255)]))
        return super().Start()
    
    def gen_point(self):
        randVector=Vector2(0,0)
        randVector.getRandomDir()
        self.target=self.Position+randVector*random.randint(10,15)
        self.dif=self.Position-self.target
        self.dif.normalise()

    def Update(self):
        self.MovePosition(self.Position+self.dif*(self.speed*DarkEngine.deltaTime))
        if self.Position==self.target:
            self.speed=0
            self.gen_point()
        if self.Position.x<0 or self.Position.x>1200 or self.Position.y>700 or self.Position.y<0:
            self.Position=Vector2(300,300)
            self.gen_point()
        super().Update()
    
    def OnColliderCurrent(self, object):
        if super().OnColliderCurrent(object):
            pass
    
    

class DarkEngineLoop:
    
    def __init__(self):
        pg.init()
        flags = pg.DOUBLEBUF 
        self.window = pg.display.set_mode((1280,720),flags)
        self.Clock = pg.time.Clock()
        self.fps_max=240
        self.fps_now=144
        self.deltaTime=0
        self.objects=np.array([],dtype=GameObject)
        self.keys=pg.key.get_pressed()
        self.windowSize=self.window.get_size()
        self.defaultFont = pg.font.SysFont('Comic Sans MS', 25)
        
        #16120
    def LoadObject(self,obj: object):
        self.objects=np.append(obj,self.objects)

    def Set_icon(self,image):
        pg.display.set_icon(image)
        
    def set_frame(self, fps):
        self.fps_max = fps

    def startScene(self):
        self.window.fill((0,0,0))
        font = pg.font.SysFont('Comic Sans MS', 140)
        font2 = pg.font.SysFont('Comic Sans MS', 100)
        text = font.render("DarkEngine",True,(255,255,255))
        text2 = font2.render("by Python3",True,(255,255,255))
        self.window.blit(text,(self.windowSize[0]*0.2,self.windowSize[1]*0.2))
        self.window.blit(text2,(self.windowSize[0]*0.2,self.windowSize[1]*0.45))
        pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))
        pg.time.wait(2000)
    
    def run(self):
        self.startScene()  
        for obj in self.objects:
            obj.Start()
        while True:
            self.keys=pg.key.get_pressed()
            self.deltaTime=self.Clock.get_time()/100
            self.window.fill((0,0,0))
            # for obj in self.objects:
            #     if obj.Drawing and obj.Enabled:
            #         obj.Update()                                          OLD     OLD   OLD
            # for obj in self.objects:    
            #     for obj2 in self.objects:
            #         if (obj.Drawing and obj.Enabled) and (obj2.Drawing and obj2.Enabled):
            #             obj.OnColliderCurrent(obj2)
            for objI in np.arange(len(self.objects)):
                if self.objects[objI].Enabled:
                    self.objects[objI].Update()
                    for objJ in np.arange(objI+1,len(self.objects)):
                        if self.objects[objJ].Drawing and self.objects[objJ].Enabled:
                            self.objects[objJ].OnColliderCurrent(self.objects[objI])
                            self.objects[objI].OnColliderCurrent(self.objects[objJ])
                            break
                
            
            
            [pg.quit() for event in pg.event.get() if event.type==pg.QUIT]
                    
                    
            
            text=self.defaultFont.render(str(int(self.Clock.get_fps())),True,(255,255,255))############# TMP ПОТОМ УДАЛИТЬ
            self.window.blit(text,(0,0))                                                   ############# TMP ПОТОМ УДАЛИТЬ
            self.Clock.tick(self.fps_max)
            pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))
            



DarkEngine = DarkEngineLoop()
imageload=ImageLoader()

player=Player()


DarkEngine.LoadObject(player)
[DarkEngine.LoadObject(tmpObject()) for i in np.arange(20)]







DarkEngine.run()