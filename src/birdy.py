### IMPORTS ###

import random
import pygame
import os

### BIRDY CLASS ###

class Birdy(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.frames = self.get_frames(random.choice(["bluebird", "redbird", "yellowbird"]))
        self.frame_index= 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.hit_ground = False
        self.up_dn_num = 2
        self.tilt = 0
        self.up_dn_lim = 0
        self.hit_roof = False

    def animate(self):
        self.frame_index += 0.1
        if int(self.frame_index) >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        self.frame_index += 0.1
        if int(self.frame_index) >= len(self.frames):
            self.frame_index = 0
        if self.direction.y < 0:
            self.tilt = 20 
        else:
            self.tilt -= 2 
        if self.tilt < -90:
            self.tilt = -90
        elif self.tilt > 30:
            self.tilt = 30
        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], self.tilt)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_frames(self, bird_color):
        frames = []
        for frame in os.listdir(os.path.join(self.ROOT_DIR, "assets", "sprites")):
            if frame.split("-")[0] == bird_color:
                new_frame = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", frame)).convert_alpha(), (50, 40))
                frames.append(new_frame)
        return frames

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def after_landing(self, SCROLL_SPEED):
        self.rect.x -= SCROLL_SPEED

    def flap(self):
        self.direction.y = -12

    def up_down(self):
        self.rect.y += self.up_dn_num
        self.up_dn_lim += self.up_dn_num
        if self.up_dn_lim > 5:
            self.up_dn_num = -1
        if self.up_dn_lim < -5:
            self.up_dn_num = 1

    def update(self, SCROLL_SPEED):
        if self.gravity == 0 and not self.hit_ground:
            self.up_down()
            self.animate()
        else:
            if not self.hit_ground:
                self.rotate()
            self.apply_gravity()
        if self.hit_ground:
            self.after_landing(SCROLL_SPEED)

### END ###
