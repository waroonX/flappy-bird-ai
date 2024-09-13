import os
import random
import time

from pygame import transform, image, mask, display
import pygame
import neat

from constants import IMG_DIR, WIN_HEIGHT, WIN_WIDTH


#Loading all icons
ALL_BIRD_IMGS = ['bird1.png', 'bird2.png', 'bird3.png']
BIRD_IMGS = [transform.scale2x(image.load(os.path.join(IMG_DIR, img))) for img in ALL_BIRD_IMGS]
PIP_IMG = transform.scale2x(image.load(os.path.join(IMG_DIR, 'pipe.png')))
BASE_IMG = transform.scale2x(image.load(os.path.join(IMG_DIR, 'base.png')))
BG_IMG = transform.scale2x(image.load(os.path.join(IMG_DIR, 'bg.png')))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = Bird.IMGS[0]
        
    def jump(self) -> None:
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self) -> None:
        self.tick_count += 1
        
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        
        #terminal velocity
        if d >= 16:
            d = 16
        
        # fine tuniing jumping up. Can be changed
        if d < 0:
            d -= 2
            
        self.y += d
        
        if d<0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
                
    def draw(self, win):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        # when the bird is tilted at an angle
        # make sure its not flapping wings
        # self.ANIMATION_TIME*2 because we want it to align with the timings mentioned above
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
            
        rotated_img = transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        
        win.blit(rotated_img, new_rect.topleft)
        
    def get_mask(self):
        return mask.from_surface(self.img)
    
def draw_window(win, bird: Bird):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    display.update()
    
def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_window(win, bird)
                
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main()
