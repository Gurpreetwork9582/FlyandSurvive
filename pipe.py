import pygame as pg
import random

class Pipe:
    def __init__(self):
        self.distance = 50
        self.ran_y_down = random.randint(80, 150)
        self.ran_y_up = 700 - self.ran_y_down - self.distance


        self.ran_x_up = random.randint(700, 800)
        self.ran_x_down = random.randint(700, 800)
        
        self.imgup=pg.transform.scale_by(pg.image.load(r"pipeup.png").convert_alpha(),.15)
        self.imgdown=pg.transform.scale_by(pg.image.load(r"pipedown.png").convert_alpha(),.15)
        self.rect_imgup=self.imgup.get_rect(center=(self.ran_x_up,self.ran_y_up))
        self.rect_imgdown=self.imgdown.get_rect(center=(self.ran_x_down,self.ran_y_down))
        
        self.scored = False


    def draw(self,win):
        win.blit(self.imgup,self.rect_imgup)
        win.blit(self.imgdown,self.rect_imgdown)

    def movement(self, dt):
        
        self.rect_imgup.x -= 200 * dt
        self.rect_imgdown.x -= 200 * dt
        