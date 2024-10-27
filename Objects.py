from Engine.EngineSrc import GameObject,ImageLoader,ImageObject,Vector2,DarkEngine
import pygame as pg
import random

imageload=ImageLoader()


class Loger(GameObject):
    
    def Awake(self):
        super().Awake()
        
    def Update(self):
        print("loged")
        super().Update()

class Phone(ImageObject):
    

    def Awake(self):
        self.Width,self.Height=1280,720
        #self.Width*=2
        self.Load_Image(imageload.load("phone2.png"))
        super().Awake()
    

class Player(GameObject):
    
    def Awake(self):
        self.Position=Vector2(0,0)
        self.Width=20
        self.Height=20
        self.Load_Sprite()
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
    
    def Set_parms(self,w,h,pos):
        self.Width=w,
        self.Height=h
        self.Position=pos
    
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
        
def gen_lab(rows,columns):
    chars=['#',"."," "]
    lab=[]
    for i in range(rows):
        lab.append([""])
        for j in range(columns):
            if j==0 or j == columns-1 or i==0 or i==rows-1:
                lab[i][0]+='#'
                continue
            lab[i][0]+=random.choice(chars)
    return lab

def load_lab(lab):
    w,h=DarkEngine.windowSize[0]/len(lab[0][0]),DarkEngine.windowSize[1]/len(lab)   
    for row,col in enumerate(lab):
        for i in range(len(col[0])):
            if col[0][i]=="#":
                tmp=LabBlock()
                tmp.Set_parms(w+1,h+1,Vector2(i*w,row*h))

