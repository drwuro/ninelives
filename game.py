import pygame
import os

from bitmapfont import BitmapFont

SCR_W, SCR_H = 320, 180
TW, TH = 16, 16

pygame.init()

#   os.environ['SDL_VIDEO_WINDOW_POS'] = WINDOWPOS_CENTERED

#       TILE repository:
#       +   "stahlwand"
#       #   wand
#           bodenfliese
#       i   beleuchtet
#         j halb beleuchtet
#       b   box
#       k   kerze
#       t   taschenlampe TOP
#         u taschenlampe RIGHT
#         v taschenlampe DOWN
#         w taschenlampe LEFT
#       f   fisch
#       g   "gestorbener" fisch
#       e   enemy (starting position)
#       c   cat (starting position)


TILES = {'#': pygame.image.load('gfx/wall.png'),
         '+': pygame.image.load('gfx/border.png'),
         ' ': pygame.image.load('gfx/floor.png'),
         'i': pygame.image.load('gfx/floor_i.png'),
         'j': pygame.image.load('gfx/floor_j.png'),
         'b': pygame.image.load('gfx/box.png'),
         'g': pygame.image.load('gfx/g.png'),

         'cat': pygame.image.load('gfx/cat.png'),
         'cursor': pygame.image.load('gfx/cursor.png'),
         'dummy': pygame.image.load('gfx/dummy.png'),
         }

OBSTACLES = ['#', '+']
FLOORS = [' ', 'i', 'j']


class Object:
    def __init__(self, sprite_id, xpos=1, ypos=1):
        self.sprite_id = sprite_id
        self.xpos = xpos
        self.ypos = ypos
        self.xdir = 0
        self.ydir = 0

        self.movedelay = 0

    def render(self, target):
        target.blit(TILES[self.sprite_id], (self.xpos * TW, self.ypos * TH))

    def moveLeft(self):
        self.xdir = -1
        self.ydir = 0

    def stopLeft(self):
        if self.xdir < 0:
            self.xdir = 0

    def moveRight(self):
        self.xdir = 1
        self.ydir = 0

    def stopRight(self):
        if self.xdir > 0:
            self.xdir = 0

    def moveUp(self):
        self.ydir = -1
        self.xdir = 0

    def stopUp(self):
        if self.ydir < 0:
            self.ydir = 0

    def moveDown(self):
        self.ydir = 1
        self.xdir = 0

    def stopDown(self):
        if self.ydir > 0:
            self.ydir = 0

    def update(self):
        self.xpos += self.xdir
        self.ypos += self.ydir

        self.movedelay = 8

    def mayMove(self):
        self.movedelay -= 1

        if self.movedelay <= 0:
            return True

        return False


class Game:
    def __init__(self):
        self.initVideo()

        self.running = False
        self.editmode = False
        self.font = BitmapFont('gfx/heimatfont.png')

        self.player = Object('cat')

        # editmode
        self.editcursor = Object('cursor')

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
                    self.player.moveLeft()

                if e.key == pygame.K_RIGHT:
                    self.player.moveRight()

                if e.key == pygame.K_UP:
                    self.player.moveUp()

                if e.key == pygame.K_DOWN:
                    self.player.moveDown()


                if e.key == pygame.K_TAB:
                    self.editmode = not self.editmode

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    self.player.stopLeft()

                if e.key == pygame.K_RIGHT:
                    self.player.stopRight()

                if e.key == pygame.K_UP:
                    self.player.stopUp()

                if e.key == pygame.K_DOWN:
                    self.player.stopDown()

            if e.type == pygame.QUIT:
                self.running = False
                return

    def update(self):
        # update cat

        if not self.player.mayMove():
            return

        tileLeft = self.getTile(self.player.xpos -1, self.player.ypos)
        tileRight = self.getTile(self.player.xpos +1, self.player.ypos)
        tileUp = self.getTile(self.player.xpos, self.player.ypos -1)
        tileDown = self.getTile(self.player.xpos, self.player.ypos +1)

        tileLeft2 = self.getTile(self.player.xpos -2, self.player.ypos)
        tileRight2 = self.getTile(self.player.xpos +2, self.player.ypos)
        tileUp2 = self.getTile(self.player.xpos, self.player.ypos -2)
        tileDown2 = self.getTile(self.player.xpos, self.player.ypos +2)

        if self.player.xdir == -1:
            if tileLeft not in OBSTACLES:
                if tileLeft == 'b':
                    if tileLeft2 in FLOORS:
                        self.setTile(self.player.xpos -2, self.player.ypos, 'b')
                        self.setTile(self.player.xpos -1, self.player.ypos, ' ')
                        self.player.update()
                else:
                    self.player.update()

        if self.player.xdir == 1:
            if tileRight not in OBSTACLES:
                if tileRight == 'b':
                    if tileRight2 in FLOORS:
                        self.setTile(self.player.xpos +2, self.player.ypos, 'b')
                        self.setTile(self.player.xpos +1, self.player.ypos, ' ')
                        self.player.update()
                else:
                    self.player.update()

        if self.player.ydir == -1:
            if tileUp not in OBSTACLES:
                if tileUp == 'b':
                    if tileUp2 in FLOORS:
                        self.setTile(self.player.xpos, self.player.ypos -2, 'b')
                        self.setTile(self.player.xpos, self.player.ypos -1, ' ')
                        self.player.update()
                else:
                    self.player.update()

        if self.player.ydir == 1:
            if tileDown not in OBSTACLES:
                if tileDown == 'b':
                    if tileDown2 in FLOORS:
                        self.setTile(self.player.xpos, self.player.ypos +2, 'b')
                        self.setTile(self.player.xpos, self.player.ypos +1, ' ')
                        self.player.update()
                else:
                    self.player.update()

    def render(self):
        self.screen.fill((0, 0, 0))

        for y, line in enumerate(self.level):
            for x, tile in enumerate(line):
                # always draw floor
                self.screen.blit(TILES[' '], (x * TW, y * TH))

                if tile in TILES:
                    self.screen.blit(TILES[tile], (x * TW, y * TH))
                else:
                    self.screen.blit(TILES['dummy'], (x * TW, y * TH))

        # draw cat
        self.player.render(self.screen)

        #self.font.centerText(self.screen, 'CATS HAVE NINE LIVES', y=5)
        #self.font.centerText(self.screen, 'F11 or ALT+ENTER = FULLSCREEN', y=7)

        # show editmode
        if self.editmode:
            self.font.drawText(self.screen, 'EDIT MODE', x=1, y=1)
            self.cursor.render(self.screen)


        pygame.display.flip()


        #editmode
    def editmode(self):
        pygame.draw.rect()


    def run(self):
        self.running = True

        clock = pygame.time.Clock()

        while self.running:
            self.render()
            self.controls()
            self.update()

            clock.tick(60)


game = Game()

game.loadLevel(1)
game.run()

pygame.quit()

