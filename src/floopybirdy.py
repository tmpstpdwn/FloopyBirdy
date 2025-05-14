### IMPORTS ###

import pygame
import random
from birdy import Birdy
from ground import Ground
from pipe import Pipe
from score import Score
import datetime
import os
import time

### CLASS FLOOPYBIRDY ###

class FloopyBirdy:

    def __init__(self) -> None:
        
        ### PYGAME INIT ###

        pygame.init()

        ### CONSTANTS ###

        self.ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.HIT_WAV = pygame.mixer.Sound(os.path.join(self.ROOT_DIR, "assets", "audio", "hit.wav"))
        self.POINT_WAV = pygame.mixer.Sound(os.path.join(self.ROOT_DIR, "assets", "audio", "point.wav"))
        self.WING_WAV = pygame.mixer.Sound(os.path.join(self.ROOT_DIR, "assets", "audio", "wing.wav"))
        self.WIDTH, self.HEIGHT = 400, 600
        self.FPS = 60
        self.WIN = pygame.display.set_mode((self.WIDTH , self.HEIGHT))
        pygame.display.set_caption("FloopyBirdy")
        self.FLOOPYTITLE = pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", "floopybird.png"))
        self.GAMEOVER   = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", "gameover.png")).convert_alpha(), (70/100*self.WIDTH, 10/100*self.HEIGHT))
        self.TAP = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", "tap.png")).convert_alpha(), (150, 150))
        self.TAP1 = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", "tap1.png")).convert_alpha(), (150, 65))
        self.ICON = pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "icons", "favicon.ico"))
        self.BG_IMAGE, self.PIPE_IMAGE = self.returnBgPipe()
        self.BG = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", self.BG_IMAGE)), (self.WIDTH, self.HEIGHT))
        self.PIPE = pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", self.PIPE_IMAGE))
        self.GROUND = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", "base.png")), (self.WIDTH, 100))
        pygame.display.set_icon(self.ICON)
        self.SPAWN_PIPE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_PIPE_EVENT, random.randint(1000, 1500))
        self.SCROLL_SPEED = 4

        ### VARIABLES ###

        self.clock = pygame.time.Clock()
        self.ground = pygame.sprite.GroupSingle()
        self.ground.add(Ground(self.HEIGHT, self.WIDTH, self.GROUND))
        self.birdy = pygame.sprite.GroupSingle()
        self.birdy.add(Birdy((self.WIDTH // 2, self.HEIGHT // 2 - 50)))
        self.pipes = pygame.sprite.Group()
        self.score = Score(self.birdy, self.pipes, self.WIDTH, self.POINT_WAV)
        self.gameState = "start" # start / running / gameover

    def returnBgPipe(self):
        CURR_HR = datetime.datetime.now().hour
        if CURR_HR > 18:
            return "background-night.png", "pipe-red.png"
        else:
            return "background-day.png", "pipe-green.png"
 
    def startDraw(self):
        # draw onto the screen when the game is in start mode

        self.WIN.blit(self.BG, (0, 0))
        self.ground.draw(self.WIN)
        self.birdy.draw(self.WIN)
        floopyTitle = self.FLOOPYTITLE.get_rect(center = (self.WIDTH // 2, 60))
        tapRect = self.TAP.get_rect(center = (self.WIDTH // 2, self.HEIGHT // 2 + 100))
        self.WIN.blit(self.FLOOPYTITLE, floopyTitle)
        self.WIN.blit(self.TAP, tapRect)
        button_pressed = pygame.mouse.get_pressed()
        if button_pressed[0]:
            self.gameState = "running"

    def gameOverDraw(self):
        self.WIN.blit(self.BG, (0, 0))
        self.pipes.draw(self.WIN)
        self.ground.draw(self.WIN)
        self.birdy.draw(self.WIN)
        gameOver = self.GAMEOVER.get_rect(center = (self.WIDTH // 2, 60))
        tap1Rect = self.TAP1.get_rect(center = (self.WIDTH // 2, self.HEIGHT // 2 + 150))
        self.WIN.blit(self.GAMEOVER, gameOver)
        self.WIN.blit(self.TAP1, tap1Rect)
        button_pressed = pygame.mouse.get_pressed()
        if button_pressed[0]:
            self.reset()

    def scrollSpeedUpd(self):
        if self.score.score > 10:
            self.SCROLL_SPEED = 4.3
        if self.score.score > 50:
            self.SCROLL_SPEED = 4.5
        if self.score.score > 100:
            self.SCROLL_SPEED = 4.8
        if self.score.score > 250:
            self.SCROLL_SPEED = 5.2
        if self.score.score > 500:
            self.SCROLL_SPEED = 5.7
        if self.score.score > 1000:
            self.SCROLL_SPEED = 6

    def runningDraw(self):
        # draw onto the screen when the game is running

        self.WIN.blit(self.BG, (0, 0))
        self.pipes.draw(self.WIN)
        self.ground.draw(self.WIN)
        self.birdy.draw(self.WIN)
        self.score.draw(self.WIN)
 
    def draw(self, mode):
        # draw contents onto the window and update

        if mode == "start":
            self.startDraw()
        elif mode == "running":
            self.runningDraw()
        else:
            self.gameOverDraw()
        pygame.display.update()

    def collisions(self): 
        # check collision of the bird with ground, roof or pipes

        if pygame.sprite.collide_rect(self.birdy.sprite, self.ground.sprite): # check for collotion of bird with ground
            self.birdy.sprite.rect.bottom = self.ground.sprite.rect.top
            self.birdy.sprite.direction.y = 0
            self.birdy.sprite.hit_ground = True
            if not pygame.mixer.get_busy():
                self.HIT_WAV.play()

        if  self.birdy.sprite.rect.top < 0: # check for collotion of bird with roof
            self.birdy.sprite.hit_roof = True
            if not pygame.mixer.get_busy():
                self.HIT_WAV.play()
    
        if pygame.sprite.spritecollide(self.birdy.sprite, self.pipes, False): # check for collotion of bird with pipes
            self.birdy.sprite.hit_ground = True
            if not pygame.mixer.get_busy():
                self.HIT_WAV.play()

        for pipe in self.pipes:
            if not pipe.passed and self.birdy.sprite.rect.left > pipe.rect.right:
                self.POINT_WAV.play()
                self.score.score += 0.5
                pipe.passed = True

    def spawn_pipes(self):
        #code logic of spawning and arrangement of pipes

        height = self.PIPE.get_height()
        x = self.WIDTH
        while True:
            y_1, y_2 =  random.randint(-300, 0), random.randint(self.HEIGHT - 100, self.HEIGHT + 200)
            up_height = (height - (y_2 - (self.HEIGHT - 100)))
            down_height = (height + y_1)
            gap = self.HEIGHT - (up_height + down_height)
            if gap >= 250 and gap <= 300:
                break
        self.pipes.add(Pipe((x, y_1), "down", self.PIPE))
        self.pipes.add(Pipe((x, y_2), "up", self.PIPE))


    def eventLoop(self):
        self.clock.tick(self.FPS)
        for event in pygame.event.get(): # event loop
            if event.type == pygame.QUIT:
                    exit()
            if not (self.birdy.sprite.hit_ground or  self.birdy.sprite.hit_roof):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.birdy.sprite.flap()
                        self.WING_WAV.play()
                        self.birdy.sprite.gravity = 0.8
            if event.type == self.SPAWN_PIPE_EVENT and self.gameState in ["running", "gameover"]:
                self.spawn_pipes()

    def objUpdate(self):
        self.ground.update(self.SCROLL_SPEED) 
        self.birdy.update(self.SCROLL_SPEED)
        self.pipes.update(self.SCROLL_SPEED)
        self.score.update()

    def reset(self):
        self.birdy.sprite.kill()
        self.birdy.add(Birdy((self.WIDTH // 2, self.HEIGHT // 2 - 50)))
        self.score.score = 0
        self.pipes.empty()
        self.SCROLL_SPEED = 4
        self.gameState = "start"
        time.sleep(0.2)

    def gameStateControl(self):
        if self.birdy.sprite.rect.right < 0: # when the bird goes out of the window after dead.
            self.gameState = "gameover"
            if self.score.score > self.score.highscore:
                self.score.setHighScore(int(self.score.score))
        if self.gameState == "start":
            self.draw(mode="start")
        elif self.gameState == "running":
            self.collisions()
            self.draw(mode="running")
        else:
            self.draw(mode="gameover")

    def run(self):
        # run fn : puts all things togather and makes it work

        while True: # Game loop
            self.eventLoop() # sets up the event loop and looks for events and exec repective code.
            self.scrollSpeedUpd()
            self.objUpdate() # updates objects [ground, birdy, pipe, score] . eg: animation.
            self.gameStateControl() # code that executes particular game state related code. eg: drawing the start / running interface
        else:
            exit()

### END ###
