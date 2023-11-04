import pygame
from bitmapfont import BitmapFont

SCR_W, SCR_H = 320, 180
WIN_W, WIN_H = SCR_W * 3, SCR_H * 3

pygame.init()


class Game:
    def __init__(self):
        self.initVideo()
        self.running = False
        
        self.font = BitmapFont('gfx/heimatfont.png')
        
    def initVideo(self):
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), flags)
    
    ###
        
    def controls(self):
        while True:
            e = pygame.event.poll()
            
            if not e:
                break
                
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.running = False
                    return
        
    def update(self):
        pass
        
    def render(self):
        self.font.centerText(self.screen, 'CATS HAVE NINE LIVES', y=5)
        
        pygame.display.flip()
        
    def run(self):
        self.running = True
        
        while self.running:
            self.render()
            self.controls()
            self.update()



game = Game()
game.run()

pygame.quit()

