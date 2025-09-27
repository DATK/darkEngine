from Engine.EngineSrc import DarkEngine,ImageLoader,ImageObject,GameObject,TextBox,Vector2,CustomEvent,Event,PhysicBody2D, RectangleShape
import pygame as pg
import random as r
from textures import squareTexture
from settings import RESOLUTION


class Square(GameObject):

    def Start(self):
        self.Width = 56
        self.Height = self.Width
        self.Set_Sprite(squareTexture)
        #self.AddSelfColider()
        Event(pg.MOUSEBUTTONDOWN,self.move)
        self.shape = RectangleShape(self.Width/2,self.Height/2)
        self.p = PhysicBody2D(self.shape,4,self.Position,2,0.3)
        return super().Start()

    def Update(self):
        self.Rotate(self.p.angle)
        self.Position = self.p.Position
        if DarkEngine.keys[pg.K_d]:
            self.p.angle+=1
    
        return super().Update()

    def move(self):
        if pg.mouse.get_pressed()[0]:
            dif = self.Position-Vector2(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])
            dif.normalized()
            self.MovePosition(self.Position-dif*1000*DarkEngine.deltaTime)
        

    

def create():
    if pg.mouse.get_pressed()[2]:
        Square(Vector2(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]))


Event(pg.MOUSEBUTTONDOWN,create)