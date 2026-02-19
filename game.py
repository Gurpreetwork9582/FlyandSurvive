import sys, pygame as pg
from bird import Bird
from pipe import Pipe
pg.init()

class Game:
    def __init__(self):
        #win
        self.win=pg.display.set_mode((400,600))

        #background 
        self.img=pg.transform.scale_by(pg.image.load(r"C:\Users\gurpreet.singh\Desktop\program\flappy-bird-background.jpg").convert(),1)
        self.rect=self.img.get_rect()
        self.img2=pg.transform.scale_by(pg.image.load(r"C:\Users\gurpreet.singh\Desktop\program\flappy-bird-background.jpg").convert(),1)
        self.rect2=self.img2.get_rect()
        self.scored = False 

        self.rect.x = 0
        self.rect.y=0
        self.rect2.x=self.rect.right  
        self.rect2.y=0

        #Score
        self.score_font = pg.font.Font(r"C:\Users\gurpreet.singh\Desktop\program\font.ttf",9)
        self.score_img=self.score_font.render("Score: 0",True,(0,0,0))
        self.Score_rect=self.score_img.get_rect(center=(30,30))
        self.new_value = 0
        

        #Bird class
        self.bird=Bird()
        self.is_entered = False
        self.game_over = False
        
        #Pipe 
        self.scored = False
        self.pip=[]
        self.pipe_counter = 10

        self.collided = False

        #Restart
        self.Restart_font= pg.font.Font(r"C:\Users\gurpreet.singh\Desktop\program\font.ttf",15)
        self.Restart_img=self.Restart_font.render("Restart", False, (0,0,0))
        self.Restart_rect=self.Restart_img.get_rect(center=(200,550))

    def Gameloop(self):
        clock = pg.time.Clock()
        while True:
            dt=clock.tick(90)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                         self.is_entered =True     
                    if event.key == pg.K_SPACE:
                        self.bird.flap()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.collided and self.Restart_rect.collidepoint(event.pos):
                        self.Reset()
                        self.is_entered = False
                    continue
                
            self.motion(dt)
            self.display()
            pg.display.flip()
            

        

    # Displaying the imgs on screen
    def display(self):
        self.win.blit(self.img,self.rect)
        self.win.blit(self.img2,self.rect2)
        self.win.blit(self.score_img,self.Score_rect)
        self.bird.draw(self.win)


        if self.pipe_counter > 150:
            self.pip.append(Pipe())
            self.pipe_counter = 0 
        self.pipe_counter +=1

        for i in self.pip:
            i.draw(self.win)

        if self.collided: 
            self.win.blit(self.Restart_img,self.Restart_rect)
        
        
                

    #Motion of back ground
    def motion(self,dt):
        if self.is_entered and not self.game_over:
            self.rect.x -= 200 * dt
            self.rect2.x -= 200 * dt
            
            # Loop images when they go off screen
            if self.rect.right <0:
                self.rect.x = self.rect2.right 
            if self.rect2.right <0:
                self.rect2.x = self.rect.right 

            #movement of bird
            self.bird.update(dt) 
            self.Scoreinfo()   


            for pipe in self.pip:
                pipe.movement(dt)

        if self.is_entered and not self.game_over:
            self.bird.update(dt) 

        
        self.Collision()

# Collidon of Bird and Pipe
    def Collision(self):                            
        if self.bird.birdrect.bottom >= 480:
            self.bird.birdrect.y = 480
            self.game_over=True
            self.collided =True

        if self.bird.birdrect.top <= 0:
            self.bird.birdrect.y=0
            self.collided =True

        for pipe in self.pip:
            if self.bird.birdrect.colliderect(pipe.rect_imgup) or self.bird.birdrect.colliderect(pipe.rect_imgdown): 
                self.game_over =True
                self.collided=True

     
            
        
# Score checking
    def Scoreinfo(self):
         for pipe in self.pip:
            if not pipe.scored and (self.bird.birdrect.left > pipe.rect_imgup.left and  self.bird.birdrect.left > pipe.rect_imgdown.left):  
                pipe.scored = True
                self.new_value+= 1  
                 
                
            if self.bird.birdrect.left > pipe.rect_imgup.right and  self.bird.birdrect.left > pipe.rect_imgdown.right: 
                self.score_img =self.score_font.render(f"Score: {self.new_value}",True,(0,0,0))


    def Reset(self):
        self.game_over =False
        self.collided=False
        self.is_entered=False

        self.rect.x = 0
        self.rect2.x = self.rect.right

        self.pip.clear()

        self.bird.Reset()

        self.new_value =0
        self.score_img =self.score_font.render(f"Score: {self.new_value}",True,(0,0,0))
        
p1=Game() 
p1.Gameloop()