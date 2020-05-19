import pygame
from pygame.locals import *
import numpy as np
import math
import random

#naming necessary variables

g = 0.5 # gravity
jumpHeight = 10
jumpVel = 2*jumpHeight*g
t = 0

speed = 25
game_speed = 6

dist = 100 #distance between obstacles
i = 0 # counter variable for same

background_col = (235,235,235)
FPS = 60

pygame.init()
scr_size = (width,height) = (600,200)
screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()

#loading sprites
dino_jump = pygame.image.load("sprites/dino_.png")

dino_run = [pygame.image.load("sprites/dino_1.png"), pygame.image.load("sprites/dino_2.png")]

dino_duck = [pygame.image.load("sprites/dino_ducking1.png"), pygame.image.load("sprites/dino_ducking2.png")]

dino_dead = pygame.image.load("sprites/dino_dead.png")

ground = pygame.image.load("sprites/ground.png")
ground = pygame.transform.scale(ground, (1200,15))
ground1 = ground
(ground_pos_x_0,ground_pos_y) = (0,height - 50)
(ground_pos_x_1,ground_pos_y) = (1200,height - 50)

game_over = pygame.image.load('sprites/game_over.png')

ptera = [pygame.image.load("sprites/ptera1.png"), pygame.image.load("sprites/ptera2.png")]
image_cactii = [pygame.image.load("sprites/c1.png"),pygame.image.load("sprites/c2.png"),pygame.image.load("sprites/c3.png"),pygame.image.load("sprites/c4.png"),pygame.image.load("sprites/c5.png"),pygame.image.load("sprites/c6.png")]

#sprite positions
(x_run,y_run) = (15, ground_pos_y + 10 - dino_run[0].get_rect()[3])
(x_duck,y_duck) = (15, ground_pos_y + 10 - dino_duck[0].get_rect()[3])
x_ptera = width
y_ptera = [y_run, y_run - 20, y_run - 50]
(x_csmall, y_csmall) = (width, ground_pos_y + 10 - 33)
(x_clarge, y_clarge) = (width, ground_pos_y + 10 - 46)

#holding variables
dinos = []
cactii = []
pteras = []

class Dino:
    def __init__(self):
        self.score = 0
        self.image_run = dino_run
        self.image_duck = dino_duck
        self.image_jump = dino_jump
        self.current = self.image_run[0]
        self.width, self.height = self.current.get_rect()[2], self.current.get_rect()[3]
        self.t = 0
        self.x = x_run
        self.y = y_run
        self.jumping = False
        self.ducking = False
        self.walkCount = 0
        self.died = False

        dinos.append(self)

    def jump(self):
        self.current = self.image_jump
        self.t += 1
        self.y = y_run - jumpVel*self.t + g*(self.t**2)/2
        if self.t == 2*jumpVel/g:
            self.t = 0
            self.jumping = False

    def running(self):
        self.x = x_run
        self.y = y_run
        if self.walkCount >= speed:
            self.walkCount =0
        self.current = self.image_run[self.walkCount//(speed//2 + 1)]
        self.walkCount += 1

    def duck(self):
        self.walkCount += 1
        if self.walkCount >= speed:
            self.walkCount =0
        self.x = x_duck
        self.y = y_duck
        self.current = self.image_duck[self.walkCount//(speed//2 + 1)]

    def draw(self,screen):
        screen.blit(self.current,(self.x,self.y))

    def crossed(self):
        if self.x <= -self.width:
            return True
        else:
            return False

    def die(self):
        self.died = True
        self.jumping = False
        self.current = dino_dead
        self.x -= game_speed
        if self.crossed():
            dinos.remove(self)


class Ptera:
    def __init__(self,loc):
        self.image = ptera
        self.current = self.image[0]
        self.width, self.height = self.current.get_rect()[2], self.current.get_rect()[3]
        self.x = x_ptera
        self.y = y_ptera[loc]
        self.walkCount = 0

        pteras.append(self)

    def crossed(self):
        if self.x <= -self.width:
            return True
        else:
            return False

    def draw(self,screen):
        self.x -= game_speed
        if self.walkCount>= speed:
            self.walkCount = 0
        self.current = self.image[self.walkCount//(speed//2 + 1)]
        self.walkCount += 1
        screen.blit(self.current,(self.x,self.y))

    def collided(self, dino):
        if (dino.y + dino.height)> self.y and dino.y < (self.y + self.height):
            if dino.x < (self.x + self.width) and (dino.x + dino.width)>self.x:
                return True
        else:
            return False

class Cactus:
    def __init__(self,ind):
        self.image = image_cactii[ind]
        self.width, self.height = self.image.get_rect()[2], self.image.get_rect()[3]
        self.x = width
        self.y = ground_pos_y + 10 - self.height

        cactii.append(self)

    def crossed(self):
        if self.x <= -self.width:
            return True
        else:
            return False

    def draw(self,screen):
        self.x = self.x - game_speed
        screen.blit(self.image,(self.x,self.y))

    def collided(self, dino):
        if (dino.y + dino.height)> self.y:
            if dino.x < (self.x + self.width) and (dino.x + dino.width)>self.x:
                return True
        else:
            return False


def updateScreen(screen, run = True):
    for dino in dinos:
        #pygame.draw.rect(screen,(0,0,255),(dino.x,dino.y,dino.width,dino.height),1)
        dino.draw(screen)
    for pt in pteras:
        #pygame.draw.rect(screen,(0,0,255),(pt.x,pt.y,pt.width,pt.height),1)
        pt.draw(screen)
    for cactus in cactii:
        #pygame.draw.rect(screen,(0,0,255),(cactus.x,cactus.y,cactus.width,cactus.height),1)
        cactus.draw(screen)

d1 = Dino()

run = True
while run:
    clock.tick(FPS)
    screen.fill(background_col)

    #part that scrolls ground
    ground_pos_x_0 -= game_speed
    ground_pos_x_1 -= game_speed
    screen.blit(ground,(ground_pos_x_0,ground_pos_y))
    screen.blit(ground1,(ground_pos_x_1 ,ground_pos_y))
    if ground_pos_x_0 <= -1200:
        ground_pos_x_0 = 1200
    elif ground_pos_x_1 <= -1200:
        ground_pos_x_1 = 1200

    i += 1
    if i%dist == 0:
        p_or_c = random.randint(1,2) # making cactus or ptera
        if p_or_c == 1: # making cactus
            typ = random.randint(0,5)
            Cactus(typ)
        elif p_or_c == 2:
            typ = random.randint(0,2)
            Ptera(typ)

    for pt in pteras:
        if pt.crossed():
            pteras.remove(pt)
    for cactus in cactii:
        if cactus.crossed():
            cactii.remove(cactus)

    #part that controls ducking, jumping
    keys = pygame.key.get_pressed()

    for dino in dinos:
        if not dino.jumping and not dino.died:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                dino.jumping = True
            elif keys[pygame.K_DOWN]:
                dino.duck()
            else:
                dino.running()

        if dino.jumping:
            dino.jump()

    #decting collisons and updating dino score
    index = 0
    for dino in dinos:
        dino.score = i%20
        for pt in pteras:
            if pt.collided(dino):
                dino.die()

        for cactus in cactii:
            if cactus.collided(dino):
                dino.die()

        index += 1

    updateScreen(screen)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)

    if len(dinos) == 0:
        run = False





