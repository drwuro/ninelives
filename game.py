import pygame
import os

from bitmapfont import BitmapFont

SCR_W, SCR_H = 320, 180
TW, TH = 16, 16

pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "-1,-1"


TILES = {'#': pygame.image.load('gfx/wall.png'),
         '+': pygame.image.load('gfx/border.png'),
         ' ': pygame.image.load('gfx/floor.png'),
         'b': pygame.image.load('gfx/box.png'),

         'cat': pygame.image.load('gfx/cat.png'),
         }

OBSTACLES = ['#', '+']
FLOORS = [' ', 'i', 'j']


class Object:
    def __init__(self, sprite_id, xpos=1, ypos=1):
        self.sprite_id = sprite_id
        self.xpos = xpos
        self.ypos = ypos

    def render(self, target):
        target.blit(TILES[self.sprite_id], (self.xpos * TW, self.ypos * TH))

    def moveLeft(self):
        self.xpos -= 1

    def moveRight(self):
        self.xpos += 1

    def moveUp(self):
        self.ypos -= 1

    def moveDown(self):
        self.ypos += 1

class Game:
    def __init__(self):
        self.initVideo()

        self.running = False
        self.editmode = False
        self.font = BitmapFont('gfx/heimatfont.png')

        self.player = Object('cat')

    def initVideo(self):
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), flags)

    def loadLevel(self, number):
        filename = 'lev/level%i' % number

        with open(filename) as f:
            lines = f.readlines()

        self.level = lines

        # find player start pos

        for y, line in enumerate(self.level):
            for x, tile in enumerate(line):
                if tile == 'c':
                    self.player.xpos = x
                    self.player.ypos = y
                    self.setTile(x, y, ' ')

    def setTile(self, x, y, tile):
        self.level[y] = self.level[y][:x] + tile + self.level[y][x+1:]

    def getTile(self, x, y):
        if x >= len(self.level[0]) or y >= len(self.level):
            return '+'

        return self.level[y][x]

    ###

    def controls(self):
        tileLeft = self.getTile(self.player.xpos -1, self.player.ypos)
        tileRight = self.getTile(self.player.xpos +1, self.player.ypos)
        tileUp = self.getTile(self.player.xpos, self.player.ypos -1)
        tileDown = self.getTile(self.player.xpos, self.player.ypos +1)

        tileLeft2 = self.getTile(self.player.xpos -2, self.player.ypos)
        tileRight2 = self.getTile(self.player.xpos +2, self.player.ypos)
        tileUp2 = self.getTile(self.player.xpos, self.player.ypos -2)
        tileDown2 = self.getTile(self.player.xpos, self.player.ypos +2)

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
                if e.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.display.toggle_fullscreen()


                if e.key == pygame.K_LEFT:
                    if tileLeft not in OBSTACLES:
                        if tileLeft == 'b' and tileLeft2 in FLOORS:
                            self.setTile(self.player.xpos -2, self.player.ypos, 'b')
                            self.setTile(self.player.xpos -1, self.player.ypos, ' ')
                            self.player.moveLeft()
                        else:
                            self.player.moveLeft()

                if e.key == pygame.K_RIGHT:
                    if tileRight not in OBSTACLES:
                        if tileRight == 'b' and tileRight2 in FLOORS:
                            self.setTile(self.player.xpos +2, self.player.ypos, 'b')
                            self.setTile(self.player.xpos +1, self.player.ypos, ' ')
                            self.player.moveRight()
                        else:
                            self.player.moveRight()

                if e.key == pygame.K_UP:
                    if tileUp not in OBSTACLES:
                        if tileUp == 'b' and tileUp2 in FLOORS:
                            self.setTile(self.player.xpos, self.player.ypos -2, 'b')
                            self.setTile(self.player.xpos, self.player.ypos -1, ' ')
                            self.player.moveUp()
                        else:
                            self.player.moveUp()

                if e.key == pygame.K_DOWN:
                    if tileDown not in OBSTACLES:
                        if tileDown == 'b' and tileDown2 in FLOORS:
                            self.setTile(self.player.xpos, self.player.ypos +2, 'b')
                            self.setTile(self.player.xpos, self.player.ypos +1, ' ')
                            self.player.moveDown()
                        else:
                            self.player.moveDown()

                if e.key == pygame.K_TAB:
                    self.editmode = not self.editmode


            if e.type == pygame.QUIT:
                self.running = False
                return

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        for y, line in enumerate(self.level):
            for x, tile in enumerate(line):
                if tile in TILES:
                    self.screen.blit(TILES[tile], (x * TW, y * TH))

        # draw cat
        self.player.render(self.screen)

        #self.font.centerText(self.screen, 'CATS HAVE NINE LIVES', y=5)
        #self.font.centerText(self.screen, 'F11 or ALT+ENTER = FULLSCREEN', y=7)

        # show editmode
        if self.editmode:
            self.font.drawText(self.screen, 'EDIT MODE', x=1, y=1)


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

