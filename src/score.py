### IMPORTS ###

import pygame
import os

### SCORE CLASS ###

class Score(pygame.sprite.Sprite):

    def __init__(self, birdy, pipes, WIDTH, POINT_WAV):
        super().__init__()

        self.ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.WIDTH = WIDTH
        self.POINT_WAV = POINT_WAV
        self.score = 0
        self.highscore = 0
        self.frames = self.get_frames()
        self.image = self.frames["0"]
        self.rect = self.image.get_rect(center = (self.WIDTH // 2 , 50))
        self.image2 = self.frames["0"]
        self.rect2 = self.image2.get_rect(center = (self.WIDTH // 2 + 100, 50))
        self.getHighScore()

    def getHighScore(self):
        try:
            with open(os.path.join("score.floopy"), "r") as scoreFile:
                contents = scoreFile.readline()
                if type(eval(contents)) is int:
                    self.highscore = eval(contents)
                else:
                    raise
        except:
            self.setHighScore(0)

    
    def setHighScore(self, score):
        with open(os.path.join("score.floopy"), "w") as scoreFile:
            scoreFile.write(f"{score}")
        self.highscore = score

    def update(self):
        self.image = self.combine_images(str(int(self.score)))
        self.rect = self.image.get_rect(center = (self.WIDTH // 2 - 100, 50))
        self.image2 = self.combine_images(str(int(self.highscore)))
        self.rect2 = self.image2.get_rect(center = (self.WIDTH // 2 + 100, 50))

    def draw(self, win):
        win.blit(self.image, self.rect)
        win.blit(self.image2, self.rect2)

    def combine_images(self, score_str):
        digit_width = 30 
        digit_height = 40 
        total_width = len(score_str) * digit_width 
        combined_image = pygame.Surface((total_width, digit_height), pygame.SRCALPHA) 
        x_offset = 0 
        for digit_char in score_str:
            digit_image = self.frames[digit_char] 
            combined_image.blit(digit_image, (x_offset, 0)) 
            x_offset += digit_width
        return combined_image
        
    def get_frames(self):
        frames = {}
        for frame in os.listdir(os.path.join(self.ROOT_DIR, "assets", "sprites")):
            if (frame.split(".")[0]).isdigit():
                new_frame = pygame.transform.scale(pygame.image.load(os.path.join(self.ROOT_DIR, "assets", "sprites", frame)).convert_alpha(), (30, 40))
                frames[frame.split(".")[0]] = new_frame
        return frames

### END ###