import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.birdimg = pg.transform.scale_by(pg.image.load(r"Bird.gif"),.10)
        self.birdrect = self.birdimg.get_rect(center=(60, 80)) 
        
        # velocity in pixels per second (positive => down)
        self.velocity = 0.0
        

    def draw(self,win):
        win.blit(self.birdimg,self.birdrect)


    def update(self,dt):
        # gravity (px/s^2)
        self.gravity = 370
        self.velocity += self.gravity * dt
        # integrate position using velocity (px)
        self.birdrect.y += self.velocity * dt

        # clamp to screen bounds
        

    def flap(self):
        # instant upward impulse (set velocity upward in px/s)
        self.velocity = -260

    def Reset(self):
        self.birdrect=self.birdimg.get_rect(center=(60, 80))