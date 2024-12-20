import pygame as pg
import random
import numpy as np
from Engine.EngineSrc import DarkEngine,GameObject,Vector2,ImageLoader,ImageObject,Sound

class Player(GameObject):
    
    def Start(self):
        self.Position=Vector2(200,200)
        self.speed=20
        self.Height=50
        self.Width=50
        self.Direction=0
        self.CanGarbage=True
        self.SpriteReverse=pg.transform.rotate(imageload.load("hero.png",colorkey=[1,(255,255,255)]),180)
        self.MainSprite=imageload.load("hero.png",colorkey=[1,(255,255,255)])
        self.Set_Sprite(imageload.load("hero.png",colorkey=[1,(255,255,255)]))
        self.AddSelfColider()
        super().Start()
    
    def OnColliderCurrent(self, colider):
        return super().OnColliderCurrent(colider) 
            
    def OnGarbage(self):
        self.MovePosition(Vector2(100,100))
        DarkEngine.RemoveFromGarbage(self)
        return super().OnGarbage()
   
    def reverse(self):
        if pg.mouse.get_pos()[0]>self.Position.x:
            self.Set_Sprite(self.MainSprite)
            self.Direction=self.Sprite.get_width()
        else:
            self.Set_Sprite(self.SpriteReverse)
            self.Direction=0
    
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
            inputVector.x+=1    ####
        elif keys[pg.K_1]:                            ####  FOR DEBUG  
            DarkEngine.Set_WithBufferColiderChek()    ####
        elif keys[pg.K_2]:                            ####
            DarkEngine.Set_WithBufferColiderChekOther() 
        elif keys[pg.K_3]:                            ####
            tmp=Enemy()
            tmp.Start()
            DarkEngine.ClearColiderBufer()####  FOR DEBUG
        inputVector.normalise()
        self.MovePosition(self.Position+inputVector*(self.speed*DarkEngine.deltaTime))

    
    def Update(self):
        self.reverse()
        self.Movement()
        super().Update()

class Phone(ImageObject):
    
    def __init__(self,statpos):
        super().__init__(statpos)
    
    def Start(self):
        self.speed=5
        self.Width,self.Height=DarkEngine.windowSize
        #self.Width*=2
        self.Load_Image(imageload.load("phone2.png"))
        return super().Start()
    
    def Update(self):
        self.Position.x-=self.speed
        if self.Position.x <= -self.Width:
            self.Position.x=DarkEngine.windowSize[0]
        super().Update()
    
class Enemy(GameObject):
    
    def Start(self):
        self.Position=Vector2(0,random.randint(0,DarkEngine.windowSize[1]))
        self.Width=70
        self.Height=60
        self.Enabled=True
        self.hp=200
        self.Direction=0
        self.gen_point()
        self.speed=random.randint(4,6)
        self.Set_Sprite(imageload.load("enemy2.png",colorkey=[1,(255,255,255)]))
        self.AddSelfColider()
        self.CanGarbage=False
        self.sound = Sound("polet.ogg")
        self.played=False
        return super().Start()
    
    def gen_point(self):
        randVector=Vector2(0,0)
        randVector.getRandomDir()
        self.target=self.Position+randVector*random.randint(10,15)
        self.dif=self.Position-self.target
        self.dif.normalise()

    
    def randomMov(self):
        self.MovePosition(self.Position-self.dif*(self.speed*DarkEngine.deltaTime))
        if self.Position==self.target:
            self.speed=0
            self.gen_point()
        if self.Position.x<0 or self.Position.x>1200 or self.Position.y>700 or self.Position.y<0:
            self.Position=Vector2(random.randint(0,DarkEngine.windowSize[0]),random.randint(0,DarkEngine.windowSize[1]))
            self.gen_point()
    
    def Update(self):
        # self.MovePosition(Vector2(self.Position.x,self.Position.y)+Vector2(-1,0)*self.speed)
        # if self.Position.x<-20:
        #     self.MovePosition(Vector2(DarkEngine.windowSize[0]+10,random.randint(50,DarkEngine.windowSize[1])))
        self.randomMov()
        #self.MovePosition(Vector2(500,500))
        if self.hp<0:
            self.Enabled=False
        #print(self.hp)  
        if self.Position.get_Difference(player.Position)<10:
            self.sound.play()
            self.played=True
        # if self.played and self.Position.get_Difference(player.Position)>14:
        #     self.sound.stop()
        #     self.played=False
        

        super().Update()
        
    def OnColliderCurrent(self, object):
        return super().OnColliderCurrent(object) 
    
class Weapon(GameObject):
    
    def Start(self):
        self.drc=0
        self.Width=5
        self.Height=5
        self.Load_Sprite()
        self.Sprite.fill((255,255,255))
        self.Position=self.obj.Position
        self.CanGarbage=True
        self.schet=0
        self.sound = Sound("shoot.ogg")
                         
        return super().Start()

    def SetParms(self,obj,speed,rasbros,damage):
        self.obj=obj
        self.speed=speed
        self.rasbros=rasbros
        self.damage=damage
        self.maxCount=2000
        self.count=1


    def shoot(self):
        if DarkEngine.keys[pg.K_SPACE]:
            self.schet+=self.count*DarkEngine.deltaTime
            if self.schet>self.maxCount:
                bulet=Bullet((self.Position.x,self.Position.y),self.speed,self.rasbros,self.damage,self.drc)
                bulet.init()
                self.sound.play()
                self.schet=0

    
    
    def update_positon(self):
        self.drc=self.obj.Direction
        self.Enabled=self.obj.Enabled
        tmp=self.drc
        if self.drc==0:
            self.drc=-1
        else:
            self.drc=1
        self.Position=self.obj.Position+Vector2(tmp,self.obj.Sprite.get_height()/2-self.Sprite.get_height()/3)
    
    def Update(self):
        self.update_positon()
        self.shoot()
        super().Update()

class Bullet(GameObject):
    
    def __init__(self, startPosition,speed,rasbros,damage,Direction):
        self.speed=speed
        self.rasbros=rasbros
        self.damage=damage
        self.Direction=Direction
        super().__init__(startPosition)
    
    def init(self):
        self.Width=15
        self.Height=15
        self.Set_Sprite(imageload.load("bullet_enemy1.png",colorkey=[1,(255,255,255)]))
        self.AddSelfColider()
    
    def Update(self):
        self.MovePosition(self.Position+Vector2(self.Direction,random.randint(self.rasbros[0],self.rasbros[1]))*self.speed)
        super().Update()
    
    def OnColliderCurrent(self, object):
        #print(object)
        if isinstance(object,Enemy):
            object.hp-=self.damage
            pass
        super().OnColliderCurrent(object)
        return False
    
imageload=ImageLoader()

player=Player() 

weap=Weapon()
weap.SetParms(player,8,(-1,1),100)
weap.count=1
weap.maxCount=10


phone1=Phone((0,0))
phone2=Phone((DarkEngine.windowSize[0],0))


# DarkEngine.LoadObject(player)
# for i in np.arange(100):
#     tmp=Enemy()
#     w=Weapon()
#     w.SetParms(tmp,14,(-1,1),2)
#     w.count=1
#     w.maxCount=150


[Enemy() for i in np.arange(2)]

DarkEngine.Set_frame(100)
DarkEngine.Set_WithBufferColiderChekOther()
                                                                                                             

DarkEngine.run()