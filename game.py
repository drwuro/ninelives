import pygame
import os

from bitmapfont import BitmapFont

SCR_W, SCR_H = 320, 180
TW, TH = 16, 16

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"


TILES = {'#': pygame.image.load('gfx/wall.png'),
         '+': pygame.image.load('gfx/border.png'),
         }


class Game:
    def __init__(self):
        self.running = False

        self.initVideo()

        self.font = BitmapFont('gfx/heimatfont.png')

    def initVideo(self):
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), flags)

    def loadLevel(self, number):
        filename = 'lev/level%i' % number

        with open(filename) as f:
            lines = f.readlines()

        self.level = lines

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
                if e.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

            if e.type == pygame.QUIT:
                self.running = False
                return

    def update(self):
        pass

    def render(self):
        for y, line in enumerate(self.level):
            for x, tile in enumerate(line):
                if tile in TILES:
                    self.screen.blit(TILES[tile], (x * TW, y * TH))

        self.font.centerText(self.screen, 'CATS HAVE NINE LIVES', y=5)
        self.font.centerText(self.screen, 'F11 = FULLSCREEN', y=7)

        pygame.display.flip()

    def run(self):
        self.running = True

        while self.running:
            self.render()
            self.controls()
            self.update()


game = Game()

game.loadLevel(1)
game.run()

pygame.quit()

