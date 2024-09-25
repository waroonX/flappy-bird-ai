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
PIPE_IMG = transform.scale2x(image.load(os.path.join(IMG_DIR, 'pipe.png')))
BASE_IMG = transform.scale2x(image.load(os.path.join(IMG_DIR, 'base.png')))
BG_IMG = transform.scale2x(image.load(os.path.join(IMG_DIR, 'bg.png')))

# Score constants
pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

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

class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self, x) -> None:
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        self.x -= self.VEL
        
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird: Bird):
        bird_mask = bird.get_mask()
        top_pipe_mask = mask.from_surface(self.PIPE_TOP)
        bottom_pipe_mask = mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_pipe_mask, bottom_offset)
        t_point = bird_mask.overlap(top_pipe_mask, top_offset)
        
        return b_point or t_point

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = Base.WIDTH
        
    def move(self):
        self.x1 -= Base.VEL
        self.x2 -= Base.VEL
        
        if self.x1 + Base.WIDTH < 0:
            self.x1 = self.x2 + Base.WIDTH
            
        if self.x2 + Base.WIDTH < 0:
            self.x2 = self.x1 + Base.WIDTH
            
    def draw(self, win):
        win.blit(Base.IMG, (self.x1, self.y))
        win.blit(Base.IMG, (self.x2, self.y))
    
def draw_window(win, bird: Bird, pipes : list[Pipe], base: Base, score: int):
    win.blit(BG_IMG, (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
        
    base.draw(win)
    bird.draw(win)
    
    text = STAT_FONT.render(f"Score: {score}", 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    display.update()
    
def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(600)]
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_SPACE:
                bird.jump()
                
        rem_pipes = []
        add_pipe = False
        bird.move()
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            
            # Remove pipes once it goes off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem_pipes.append(pipe)
                
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
                
            pipe.move()
            
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
            add_pipe = False
            
        for r in rem_pipes:
            pipes.remove(r)
            
        if bird.y + bird.img.get_height() > 730:
            pass
            
        base.move()
        draw_window(win, bird, pipes, base, score)
                
    pygame.quit()
    quit()
    
if __name__ == "__main__":
    main()
