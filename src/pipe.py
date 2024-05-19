### IMPORTS ###

import pygame

### PIPE CLASS ###

class Pipe(pygame.sprite.Sprite):

    def __init__(self, pos, orientation, PIPE):
        super().__init__()
        self.PIPE = PIPE
        if orientation == "up":
            self.image = self.PIPE
            self.rect = self.image.get_rect(midbottom = pos)
        elif orientation == "down":
            self.image = pygame.transform.flip(PIPE, False, True)
            self.rect = self.image.get_rect(midtop = pos)
        self.passed = False  # New attribute to track if the bird has passed this pipe


    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self, SCROLL_SPEED):
        self.rect.x -= SCROLL_SPEED
        self.destroy()

    def draw(self, win):
        win.blit(self.image, self.rect)

### END ###