import pygame
import time

from key_pos import BLACK_KEYS, WHITE_KEYS_LEFT, WHITE_KEYS_MID, WHITE_KEYS_RIGHT, DICT_NOTES_POS
from img import white_pr_l, white_pr_r, white_pr_mid, black_pr, last_pr


WIDTH_DISPLAY = 1240
HEIGHT_DISPLAY = 829

NOTE_WHITE_WIDTH = 22
NOTE_BLACK_WIDTH = 18
NOTE_FIRST = 21
NOTES_TOTAL = 88
BORDER = 23


COL1 = pygame.Color('#ffffff')
COL2 = pygame.Color('#f7f4f4')
COL3 = pygame.Color('#efeae9')
COL4 = pygame.Color('#e7dfde')
COL5 = pygame.Color('#dfd5d3')
COL6 = pygame.Color('#d7cac8')
COL7 = pygame.Color('#c2b6b4')
COL8 = pygame.Color('#aca2a0')
COL9 = pygame.Color('#978d8c')
COL10 = pygame.Color('#817978')
COL11 = pygame.Color('#827a79')
COL12 = pygame.Color('#6c6564')
COL13 = pygame.Color('#565150')
COL14 = pygame.Color('#403d3c')
COL15 = pygame.Color('#2b2828') 
COL16 = pygame.Color('#151414')
COL17 = pygame.Color('#000000')

COLOR_LIST = [COL1, COL2, COL3, COL4, COL5, COL6,
              COL7, COL8, COL9, COL10, COL11, COL12, COL13, COL14, COL15, COL16, COL17]


class Ball(pygame.sprite.Sprite):
    def __init__(self, win, x, time=100, velocity=100, channel=0):
        super(Ball, self).__init__()

        self.win = win
        self.x = DICT_NOTES_POS[x]      
        self.time = time
        self.velocity = velocity
        self.color = COLOR_LIST[channel]

        self.radius = velocity * 0.07
        self.y = self.radius * 2 + 70
        self.y_down = HEIGHT_DISPLAY - 159

        self.alive = True

        self.surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.surface.set_colorkey((0, 0, 0))
        self.rect = self.surface.get_rect()

        
    def update(self, speed, move='down'):
        if move == 'down':
            self.y += speed
            if self.y + self.radius >= HEIGHT_DISPLAY - 70:
                self.kill()

            if self.alive and self.velocity != 0:
                ball_cur = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)
                self.win.blit(self.surface, ball_cur)

        elif move == 'up':
            self.y_down -= speed
            if self.y_down + self.radius <= self.radius * 2 + 70:
                self.kill()

            if self.alive and self.velocity != 0:
                ball_cur = pygame.draw.circle(self.win, self.color, (self.x, self.y_down), self.radius)
                self.win.blit(self.surface, ball_cur)



class Key(pygame.sprite.Sprite):
    def __init__(self, win, x, time=0, y=675):
        super(Key, self).__init__()

        self.win = win
        if x in BLACK_KEYS:
            self.x = DICT_NOTES_POS[x] - NOTE_BLACK_WIDTH / 2
        else:
            self.x = DICT_NOTES_POS[x] - NOTE_WHITE_WIDTH / 2 

        self.y = y
        self.time = time

        if x in BLACK_KEYS:
            self.key_pr_img = black_pr
        elif x in WHITE_KEYS_LEFT or WHITE_KEYS_RIGHT or WHITE_KEYS_MID:
            if x in WHITE_KEYS_MID:
                self.key_pr_img = white_pr_mid
            if x in WHITE_KEYS_LEFT:
                self.key_pr_img = white_pr_l
            if x in WHITE_KEYS_RIGHT:
                self.key_pr_img = white_pr_r
            if x == 108:
                self.key_pr_img = last_pr
        else:
            self.kill()

        self.pressed = False

        self.surface = pygame.Surface((self.x, self.y), pygame.SRCALPHA)
        self.surface.set_colorkey((0, 0, 0))

    def update(self, kill=False):
        if not self.pressed:
            self.win.blit(self.key_pr_img, (self.x, self.y))
        if kill:
            self.pressed = True
            self.kill()
        if time.time() - self.time > 0.4:
            self.kill()
