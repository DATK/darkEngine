import pygame as pg
import math
import numpy as np



class Vector2:
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
    def normalise(self):
        if self.x != 0 or self.y !=0:
            inv_length = 1/(math.sqrt((self.x**2+self.y**2)))
            self.x *= inv_length
            self.y *= inv_length
        
    def __add__(self,other): 
        if isinstance(other,Vector2):
            self.x+=other.x
            self.y+=other.y
            return Vector2(self.x,self.y)
        elif isinstance(other,(float,int)):
            self.x+=other
            self.y+=other
            return Vector2(self.x,self.y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
    
    
    def __sub__(self,other):
        if isinstance(other,Vector2):
            self.x-=other.x
            self.y-=other.y
            return Vector2(self.x,self.y)
        elif isinstance(other,(float,int)):
            self.x-=other
            self.y-=other
            return Vector2(self.x,self.y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
    
    def __mul__(self,other):
        if isinstance(other,Vector2):
            self.x*=other.x
            self.y*=other.y
            return Vector2(self.x,self.y)
        elif isinstance(other,(float,int)):
            self.x*=other
            self.y*=other
            return Vector2(self.x,self.y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")
    
    def __div__(self,other):
        if isinstance(other,Vector2):
            self.x/=other.x
            self.y/=other.y
            return Vector2(self.x,self.y)
        elif isinstance(other,(float,int)):
            self.x/=other
            self.y/=other
            return Vector2(self.x,self.y)
        else:
            raise ArithmeticError("Правый операнд должен быть числом или Vector2")

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
        
    
    def Load_Sprite(self):
        self.Sprite=pg.Surface((self.Width,self.Height))
        self.Colider=pg.Rect(self.Position.x,self.Position.y,self.Sprite.get_width(),self.Sprite.get_height())
        DarkEngine.window.blit(self.Sprite,(self.Position.x,self.Position.y))
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
        self.speed=1
        self.Height=50
        self.Width=50
        self.Load_Sprite()
        self.Sprite.fill((255,255,255))
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
        print(self.Position)
        self.Movement()
        super().Update()

    
class tmpObject(GameObject):
    
    def Update(self):
        return super().Update()
    
    


class DarkEngineLoop:
    
    def __init__(self):
        pg.init()
        flags = pg.DOUBLEBUF
        self.window = pg.display.set_mode((640,480),flags)
        self.Clock = pg.time.Clock()
        self.fps_max=144
        self.fps_now=144
        self.deltaTime=0
        self.objects=np.array([],dtype=GameObject)
        self.keys=pg.key.get_pressed()
        
        #16120
    def LoadObject(self,obj: object):
        self.objects=np.append(obj,self.objects)


    def run(self):
        for obj in self.objects:
            obj.Start()
        while True:
            self.keys=pg.key.get_pressed()
            self.deltaTime=self.Clock.get_time()
            self.window.fill((0,0,0))
            for obj in self.objects:
                if obj.Drawing and obj.Enabled:
                    obj.Update() 
                
                
            for obj in self.objects:    
                for obj2 in self.objects:
                    if (obj.Drawing and obj.Enabled) and (obj2.Drawing and obj2.Enabled):
                        obj.OnColliderCurrent(obj2)
                    
            [pg.quit() for event in pg.event.get() if event.type==pg.QUIT]
                    
                    
            
            pg.display.set_caption(str(int(self.Clock.get_fps())))
            self.Clock.tick(self.fps_max)
            pg.display.update(pg.Rect(0,0,self.window.get_width(),self.window.get_height()))
            



DarkEngine = DarkEngineLoop()
DarkEngine.LoadObject(Player())


for i in np.arange(2000):
    tmp=tmpObject()
    tmp.Enabled=1
    DarkEngine.LoadObject(tmp)




DarkEngine.run()