from Engine.EngineSrc import GameObject,ImageLoader,ImageObject,Vector2,DarkEngine
import pygame as pg
import random

imageload=ImageLoader()


class Phone(ImageObject):
    
    def Awake(self):
        self.Width,self.Height=200,200
        #self.Width*=2
        self.Load_Image(imageload.load("phone2.png"))
        super().Awake()
    
    
class Player(GameObject):
    
    def Awake(self):
        self.Position=Vector2(0,0)
        self.Width=30
        self.Height=30
        self.Load_Sprite()
        #self.Set_Sprite(imageload.load("hero.png",colorkey=[1,(255,255,255)]))
        self.Sprite.fill((255,255,255))
        super().Awake()
    
    def Start(self):    
        self.AddSelfColider()
        self.CanGarbage=False
        self.inputVector=Vector2(0,0)
        self.SecondInput=self.inputVector
        self.speed=30
        super().Start()
    
    def Update(self):
        if DarkEngine.keys[pg.K_d]:
            self.inputVector.x+=1
        if DarkEngine.keys[pg.K_a]:
            self.inputVector.x-=1
        if DarkEngine.keys[pg.K_w]:
            self.inputVector.y-=1
        if DarkEngine.keys[pg.K_s]:
            self.inputVector.y+=1
        if DarkEngine.keys[pg.K_t]:
            self.Position=Vector2(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])
        self.inputVector.normalise()
        
        self.SecondInput=Vector2(self.inputVector.x,self.inputVector.y)
        self.MovePosition(self.Position+self.inputVector*self.speed*DarkEngine.deltaTime)
        self.inputVector.nulling()
        super().Update()
        
    def OnColliderCurrent(self, object):
        if isinstance(object,LabBlock):
            self.MovePosition(self.Position-self.SecondInput*(self.speed)*DarkEngine.deltaTime)
        super().OnColliderCurrent(object)

           
class LabBlock(GameObject):
    
    def Awake(self):
        self.Position=Vector2(0,0)
        self.Width=50
        self.Height=50
        self.Load_Sprite()
        self.Sprite.fill((0,200,0))
        super().Awake()
    
    
    def Start(self):
        for player in DarkEngine.objects:
            if isinstance(player,Player):
                self.player=player
                break
        self.AddSelfColider()
        super().Start()    
    
    def colorUpdate(self):
        color_d = self.Position.get_Difference(self.player.Position)
        if color_d > 200:
            d=0
        else:
            d=210-color_d 
        self.Sprite.fill((0,int(d),0))
    
    def Update(self):
        self.colorUpdate()
        super().Update()   