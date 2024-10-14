import pygame as pg
import random
import numpy as np
from Engine.Engine import DarkEngine,GameObject,Vector2,ImageLoader,ImageObject


class Player(GameObject):
    
    def Start(self):
        self.Position=Vector2(200,200)
        self.speed=20
        self.Height=50
        self.rot=False
        self.pl=True
        self.Width=50
        self.SpriteReverse=pg.transform.rotate(imageload.load("hero.png",colorkey=[1,(255,255,255)]),180)
        self.MainSprite=imageload.load("hero.png",colorkey=[1,(255,255,255)])
        self.Set_Sprite(imageload.load("hero.png",colorkey=[1,(255,255,255)]))
        self.AddSelfColider()
        super().Start()
    
    def OnColliderCurrent(self, colider):
        return super().OnColliderCurrent(colider) 
            
   
    def reverse(self):
        if pg.mouse.get_pos()[0]>self.Position.x:
            self.Set_Sprite(self.MainSprite)
        else:
            self.Set_Sprite(self.SpriteReverse)
    
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
        if keys[pg.K_1]:                              ####
            DarkEngine.Set_DefaultColiderFunc()       ####
        elif keys[pg.K_2]:                            ####  FOR DEBUG  
            DarkEngine.Set_WithBufferColiderChek()    ####
        elif keys[pg.K_3]:                            ####
            DarkEngine.Set_WithOutBufferColiderChek() ####
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
        self.Position=Vector2(DarkEngine.windowSize[0],random.randint(0,DarkEngine.windowSize[1]))
        self.Width=70
        self.Height=60
        self.Enabled=True
        self.gen_point()
        self.speed=random.randint(4,6)
        self.Set_Sprite(imageload.load("enemy2.png",colorkey=[1,(255,255,255)]))
        self.AddSelfColider()
        self.CanGarbage=False
        return super().Start()
    
    def gen_point(self):
        randVector=Vector2(0,0)
        randVector.getRandomDir()
        self.target=self.Position+randVector*random.randint(10,15)
        self.dif=self.Position-self.target
        self.dif.normalise()

    def randomMov(self):
        self.MovePosition(self.Position+self.dif*(self.speed*DarkEngine.deltaTime))
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
        #self.randomMov()
        self.MovePosition(Vector2(500,500))
        super().Update()
        
    def OnColliderCurrent(self, object):
        return super().OnColliderCurrent(object) 
    

class Printer(GameObject):
    
    def Update(self):
        #print(DarkEngine.ColiderListBuffer.__sizeof__())
        super().Update()

imageload=ImageLoader()

player=Player()



phone1=Phone((0,0))
phone2=Phone((DarkEngine.windowSize[0],0))

# bullets=[Bullet(10,2) for i in range(300)]

# weapon = Weapon((player.Position.x,player.Position.y),1,(-1,1),1,player)
# weapon.load_Bullets(bullets,1)

# for i in bullets:
#     DarkEngine.LoadObject(i)

DarkEngine.LoadObject(player)
[DarkEngine.LoadObject(Enemy()) for i in np.arange(1)]
DarkEngine.LoadImage(phone1)
DarkEngine.LoadImage(phone2)
DarkEngine.LoadObject(Printer())
#DarkEngine.LoadObject(weapon)



DarkEngine.Set_frame(60)

#DarkEngine.Set_DefaultColiderFunc()
#DarkEngine.Set_WithBufferColiderChek()
#DarkEngine.Set_WithOutBufferColiderChek()
DarkEngine.run()