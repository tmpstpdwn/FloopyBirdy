### IMPORTS ###

import pygame

### GROUND CLASS ###

class Ground(pygame.sprite.Sprite):

    def __init__(self, HEIGHT, WIDTH, GROUND):
        super().__init__()
        self.WIDTH = WIDTH
        self.GROUND = GROUND
        self.HEIGHT = HEIGHT
        self.image = pygame.Surface((self.WIDTH * 2, 100))
        self.image.blit(self.GROUND, (0, 0))
        self.image.blit(self.GROUND, (self.WIDTH, 0))
        self.rect = self.image.get_rect(topleft = (0, self.HEIGHT - 100))
        self.mask = pygame.mask.from_surface(self.image)

    def scroll_ground(self, SCROLL_SPEED):
        if self.rect.centerx <= 0: # old: self.WIDTH // 2:
            self.rect.x = 0
        else:
            self.rect.x -= SCROLL_SPEED

    def update(self, SCROLL_SPEED):
        self.scroll_ground(SCROLL_SPEED)

### END ###