import pygame
import os
import time

from bitmapfont import BitmapFont

SCR_W, SCR_H = 320, 180
TW, TH = 16, 16
LEV_W, LEV_H = 20, 11

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
         'id': pygame.image.load('gfx/floor_id.png'),
         'j': pygame.image.load('gfx/floor_j.png'),
         'jd': pygame.image.load('gfx/floor_jd.png'),
         'b': pygame.image.load('gfx/box.png'),
         'g': pygame.image.load('gfx/fish_dead.png'),
         'g1': pygame.image.load('gfx/fish_dead2.png'),
         'g3': pygame.image.load('gfx/fish_dead3.png'),
         'f': pygame.image.load('gfx/fish_alive.png'),
         'k': pygame.image.load('gfx/candle.png'),
         'kd': pygame.image.load('gfx/candle_d.png'),
         't': pygame.image.load('gfx/Taschenlampe_t1.png'),
         'v': pygame.image.load('gfx/Taschenlampe_v1.png'),
         'u': pygame.image.load('gfx/Taschenlampe_u1.png'),
         'w': pygame.image.load('gfx/Taschenlampe_w1.png'),
         't2': pygame.image.load('gfx/Taschenlampe_t2.png'),
         'v2': pygame.image.load('gfx/Taschenlampe_v2.png'),
         'u2': pygame.image.load('gfx/Taschenlampe_u2.png'),
         'w2': pygame.image.load('gfx/Taschenlampe_w2.png'),
         '-': pygame.image.load('gfx/floor_g.png'),
         'c': pygame.image.load('gfx/cat.png'),
         'e': pygame.image.load('gfx/enemy_1.png'),

         'enemy': pygame.image.load('gfx/enemy_1.png'),
         'enemy2': pygame.image.load('gfx/enemy_2.png'),
         'cat': pygame.image.load('gfx/cat.png'),
         'cat_ghost': pygame.image.load('gfx/cat_g.png'),
         'cat_ghost2': pygame.image.load('gfx/cat_g2.png'),
         'cursor': pygame.image.load('gfx/cursor.png'),
         'cursor2': pygame.image.load('gfx/cursor2.png'),
         'saving': pygame.image.load('gfx/areyousure.png'),
         'dummy': pygame.image.load('gfx/dummy.png'),
         }

OBSTACLES_AS_CAT = ['#', '+']
OBSTACLES_AS_GHOST = ['+']
OBSTACLES_AS_ENEMY = ['#', '+', 'b']

PUSHABLES_AS_CAT = ['b']
PUSHABLES_AS_GHOST = []

OBSTACLES = OBSTACLES_AS_CAT
PUSHABLES = PUSHABLES_AS_CAT

FLOORS = [' ', 'i', 'j']
LIGHT_BLOCKERS = ['#', '+', 'b']
DO_NOT_RENDER = ['e', 'c', ' ']


class Object:
    def __init__(self, sprite_id, xpos=1, ypos=1):
        self.sprite_id = sprite_id
        self.xpos = xpos
        self.ypos = ypos
        self.xdir = 0
        self.ydir = 0
        self.speed = 8      # how many frames until next step

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
        if self.xdir != 0 or self.ydir != 0:
            self.movedelay = self.speed

        self.xpos += self.xdir
        self.ypos += self.ydir

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
        self.saving = False
        self.exitmode = False
        self.ghostmode = False
        self.gameover = False
        self.levelcomplete = False
        self.gamecomplete = False
        self.titlescreen = True

        self.font = BitmapFont('gfx/heimatfont.png')
        self.bigfont = BitmapFont('gfx/heimatfont.png', zoom=2)

        self.levelno = 1

        self.player = Object('cat')
        self.enemies = []
        self.fishcount = 0

        # editmode
        self.cursor = Object('cursor')



    def initVideo(self):
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), flags)


    # levels (load, save)
    def levelExists(self, number):
        filename = 'lev/level%i' % number
        return os.path.exists(filename)

    def loadLevel(self, number):
        filename = 'lev/level%i' % number

        with open(filename) as f:
            lines = f.readlines()

        self.level = lines

        # find player start pos and create enemies etc
        self.enemies = []
        self.fishcount = 0

        for y, line in enumerate(self.level):
            for x, tile in enumerate(line):
                if tile == 'c':
                    self.player.xpos = x
                    self.player.ypos = y
                    #self.setTile(x, y, ' ')

                if tile == 'e':
                    enemy = Object('enemy', x, y)
                    enemy.speed = 32
                    self.enemies.append(enemy)
                    #self.setTile(x, y, ' ')

                if tile in ['f', 'g']:
                    self.fishcount += 1

        self.floor = [' ' * LEV_W] * LEV_H

    def saveLevel(self, number):
        filename = 'lev/level%i' % number

        with open(filename, 'w') as f:
            for y, line in enumerate(self.level):
                f.write(line)
                # f.write('\n')


    def setTile(self, x, y, tile):
        if x >= LEV_W or y >= LEV_H or x < 0 or y < 0:
            return

        self.level[y] = self.level[y][:x] + tile + self.level[y][x+1:]

    def getTile(self, x, y):
        if x >= LEV_W or y >= LEV_H or x < 0 or y < 0:
            return '+'

        return self.level[y][x]

    def setFloor(self, x, y, tile):
        if x >= LEV_W or y >= LEV_H or x < 0 or y < 0:
            return

        self.floor[y] = self.floor[y][:x] + tile + self.floor[y][x+1:]

    def getFloor(self, x, y):
        if x >= LEV_W or y >= LEV_H or x < 0 or y < 0:
            return ' '

        return self.floor[y][x]

    def calcLighting(self):
        # clear all lighting
        for y in range(LEV_H):
            for x in range(LEV_W):
                self.setFloor(x, y, ' ')

        # re-calculate lighting
        for y in range(LEV_H):
            for x in range(LEV_W):
                if self.getTile(x, y) == 'k':
                    self.emitLighting(x, y)
                elif self.getTile(x, y) in ['t', 'u', 'v', 'w']:
                    self.emitFlashlight(x, y)

    def emitLighting(self, x, y):
        INTENSITY = [' ', 'j', 'i', 'i']

        def illuminate(x, y, intensity):
            if intensity == 0:
                return

            if INTENSITY.index(self.getFloor(x, y)) < intensity:
                self.setFloor(x, y, INTENSITY[intensity])

            coordlist = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for coords in coordlist:
                if self.getTile(x + coords[0], y + coords[1]) not in LIGHT_BLOCKERS:
                    illuminate(x + coords[0], y + coords[1], intensity -1)

        illuminate(x, y, 3)

    def emitFlashlight(self, x, y):
        flashlight = self.getTile(x, y)

        if flashlight == 't':
            coord = (0, -1)

        elif flashlight == 'u':
            coord = (1, 0)

        elif flashlight == 'v':
            coord = (0, 1)

        elif flashlight == 'w':
            coord = (-1, 0)

        while True:
            x += coord[0]
            y += coord[1]

            if x < 0 or x >= LEV_W or y < 0 or y > LEV_H:
                break

            if self.getTile(x, y) in LIGHT_BLOCKERS:
                break

            self.setFloor(x, y, 'i')

    def enterGhostMode(self):
        self.ghostmode = True
        self.player.sprite_id = 'cat_ghost'

        global OBSTACLES, PUSHABLES
        OBSTACLES = OBSTACLES_AS_GHOST
        PUSHABLES = PUSHABLES_AS_GHOST

        self.enemies = []

    def enterNormalMode(self):
        self.ghostmode = False
        self.player.sprite_id = 'cat'

        global OBSTACLES, PUSHABLES
        OBSTACLES = OBSTACLES_AS_CAT
        PUSHABLES = PUSHABLES_AS_CAT

    ###

    def controls(self):

        if self.editmode:
            cur_object = self.cursor
        else:
            cur_object = self.player



        while True:
            e = pygame.event.poll()

            if not e:
                break

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if not self.gamecomplete and not self.levelcomplete and not self.gameover and not self.titlescreen:
                        self.exitmode = not self.exitmode
                    else:
                        self.running = False
                        return

                if e.key == pygame.K_r:
                    if self.exitmode:
                        self.loadLevel(self.levelno)
                        self.enterNormalMode()
                        self.exitmode = False
                if e.key == pygame.K_q:
                    if self.exitmode:
                        self.running = False

                if e.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if e.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.display.toggle_fullscreen()

                if self.editmode:
                    if e.unicode in TILES and e.unicode != ("i") and e.unicode != ("j"):
                        if e.unicode != self.getTile(self.cursor.xpos, self.cursor.ypos):
                            self.setTile(self.cursor.xpos, self.cursor.ypos, e.unicode)
                        else:
                            self.setTile(self.cursor.xpos, self.cursor.ypos, " ")
                    else:
                        if e.unicode.isnumeric():
                            self.loadLevel(int(e.unicode))
                            self.levelno = int(e.unicode)
                        else:
                            if e.unicode == "s":
                                self.saving = not self.saving

                    if e.key == pygame.K_RETURN:
                        print(e.key)
                        self.saveLevel(self.levelno)
                        self.saving = False




                if e.key == pygame.K_LEFT:
                    cur_object.moveLeft()

                if e.key == pygame.K_RIGHT:
                    cur_object.moveRight()

                if e.key == pygame.K_UP:
                    cur_object.moveUp()

                if e.key == pygame.K_DOWN:
                    cur_object.moveDown()


                if e.key == pygame.K_SPACE:
                    if self.gameover:
                        self.gameover = False
                        self.loadLevel(self.levelno)
                        self.enterNormalMode()

                    elif self.levelcomplete:
                        self.levelcomplete = False
                        self.levelno += 1

                        if self.levelExists(self.levelno):
                            self.loadLevel(self.levelno)
                            self.enterNormalMode()
                        else:
                            self.gamecomplete = True

                    elif self.gamecomplete:
                        self.gamecomplete = False
                        self.titlescreen = True

                    elif self.titlescreen:
                        self.titlescreen = False
                        self.levelno = 1
                        self.loadLevel(self.levelno)
                        self.enterNormalMode()


                if e.key == pygame.K_TAB:
                    self.editmode = not self.editmode
                #if e.unicode == "s":
                #    if e.key == pygame.K_TAB:
                #r        self.saving = not self.saving

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    cur_object.stopLeft()

                if e.key == pygame.K_RIGHT:
                    cur_object.stopRight()

                if e.key == pygame.K_UP:
                    cur_object.stopUp()

                if e.key == pygame.K_DOWN:
                    cur_object.stopDown()

                if e.key == pygame.K_DOWN:
                    cur_object.stopDown()

            if e.type == pygame.QUIT:
                self.running = False
                return

    def update(self):
        # update lighting

        self.calcLighting()

        # update cursor (editmode)

        if self.editmode:
            if self.cursor.mayMove():
                self.cursor.update()

            return

        # update cat

        if self.player.mayMove():
            tileLeft = self.getTile(self.player.xpos -1, self.player.ypos)
            tileRight = self.getTile(self.player.xpos +1, self.player.ypos)
            tileUp = self.getTile(self.player.xpos, self.player.ypos -1)
            tileDown = self.getTile(self.player.xpos, self.player.ypos +1)

            tileLeft2 = self.getTile(self.player.xpos -2, self.player.ypos)
            tileRight2 = self.getTile(self.player.xpos +2, self.player.ypos)
            tileUp2 = self.getTile(self.player.xpos, self.player.ypos -2)
            tileDown2 = self.getTile(self.player.xpos, self.player.ypos +2)

            # check if enemies are behind pushables:
            enemLeft = False
            enemRight = False
            enemUp = False
            enemDown = False
            for enemy in self.enemies:
                if enemy.xpos == self.player.xpos -2 and enemy.ypos == self.player.ypos:
                    enemLeft = True
                if enemy.xpos == self.player.xpos +2 and enemy.ypos == self.player.ypos:
                    enemRight = True
                if enemy.xpos == self.player.xpos and enemy.ypos == self.player.ypos -2:
                    enemUp = True
                if enemy.xpos == self.player.xpos and enemy.ypos == self.player.ypos +2:
                    enemDown = True

            # check crate pushing
            if self.player.xdir == -1:
                if tileLeft not in OBSTACLES:
                    if tileLeft in PUSHABLES:
                        if tileLeft2 in FLOORS and not enemLeft:
                            self.setTile(self.player.xpos -2, self.player.ypos, tileLeft)
                            self.setTile(self.player.xpos -1, self.player.ypos, ' ')
                            self.player.update()
                    else:
                        self.player.update()

            if self.player.xdir == 1:
                if tileRight not in OBSTACLES:
                    if tileRight in PUSHABLES:
                        if tileRight2 in FLOORS and not enemRight:
                            self.setTile(self.player.xpos +2, self.player.ypos, tileRight)
                            self.setTile(self.player.xpos +1, self.player.ypos, ' ')
                            self.player.update()
                    else:
                        self.player.update()

            if self.player.ydir == -1:
                if tileUp not in OBSTACLES:
                    if tileUp in PUSHABLES:
                        if tileUp2 in FLOORS and not enemUp:
                            self.setTile(self.player.xpos, self.player.ypos -2, tileUp)
                            self.setTile(self.player.xpos, self.player.ypos -1, ' ')
                            self.player.update()
                    else:
                        self.player.update()

            if self.player.ydir == 1:
                if tileDown not in OBSTACLES:
                    if tileDown in PUSHABLES:
                        if tileDown2 in FLOORS and not enemDown:
                            self.setTile(self.player.xpos, self.player.ypos +2, tileDown)
                            self.setTile(self.player.xpos, self.player.ypos +1, ' ')
                            self.player.update()
                    else:
                        self.player.update()

        cur_x, cur_y = self.player.xpos, self.player.ypos
        cur_tile = self.getTile(cur_x, cur_y)

        if cur_tile == 'f':
            if not self.ghostmode:
                self.setTile(cur_x, cur_y, ' ')
                self.fishcount -= 1

        elif cur_tile == 'g':
            if self.ghostmode:
                self.setTile(cur_x, cur_y, ' ')
                self.fishcount -= 1

        if self.getFloor(cur_x, cur_y) != ' ':
            if self.ghostmode:
                self.gameover = True

        if self.fishcount == 0:
            self.levelcomplete = True


        # update enemies

        for enemy in self.enemies:
            if self.player.xpos < enemy.xpos:
                enemy.xdir = -1
            elif self.player.xpos > enemy.xpos:
                enemy.xdir = 1
            else:
                enemy.xdir = 0

            if self.player.ypos < enemy.ypos:
                enemy.ydir = -1
            elif self.player.ypos > enemy.ypos:
                enemy.ydir = 1
            else:
                enemy.ydir = 0

            tileLeft = self.getTile(enemy.xpos -1, enemy.ypos)
            tileRight = self.getTile(enemy.xpos +1, enemy.ypos)
            tileUp = self.getTile(enemy.xpos, enemy.ypos -1)
            tileDown = self.getTile(enemy.xpos, enemy.ypos +1)

            if enemy.xdir == -1 and tileLeft in OBSTACLES_AS_ENEMY:
                enemy.xdir = 0
            if enemy.xdir == 1 and tileRight in OBSTACLES_AS_ENEMY:
                enemy.xdir = 0
            if enemy.ydir == -1 and tileUp in OBSTACLES_AS_ENEMY:
                enemy.ydir = 0
            if enemy.ydir == 1 and tileDown in OBSTACLES_AS_ENEMY:
                enemy.ydir = 0

            # avoid diagonal movement
            if enemy.xdir != 0 and enemy.ydir != 0:
                enemy.xdir = 0

            if enemy.mayMove():
                enemy.update()

            if enemy.xpos == self.player.xpos and enemy.ypos == self.player.ypos:
                self.enterGhostMode()
                break


    def render(self):
        self.screen.fill((0, 0, 0))

        flicker = (time.time() * 1000) % 600 < 250

        for y, line in enumerate(self.level):
            for x, tile in enumerate(line):

                # draw floor / lighting
                floortile = self.getFloor(x, y)
                if floortile != ' ' and flicker:
                    floortile += 'd'

                if floortile == ' ' and self.ghostmode:
                    floortile = '-'

                self.screen.blit(TILES[floortile], (x * TW, y * TH))

                # draw actual tile
                if tile == ' ':
                    continue

                if tile in TILES or tile in DO_NOT_RENDER:
                    if tile == 'k':
                        if flicker:
                            tile += 'd'

                    elif tile == 'g':
                        anim = int((time.time() * 1000) % 800 / 200)

                        if anim == 1 or anim == 3:
                            tile += str(anim)

                    elif tile in ['t', 'u', 'v', 'w']:
                        if not flicker:
                            tile += '2'

                    if tile not in DO_NOT_RENDER or self.editmode:
                        self.screen.blit(TILES[tile], (x * TW, y * TH))
                else:
                    self.screen.blit(TILES['dummy'], (x * TW, y * TH))


        if not self.editmode:
            # draw enemies
            for enemy in self.enemies:
                enemy.render(self.screen)

                if (time.time() * 1000) % 250 < 125:
                    enemy.sprite_id = 'enemy2'
                else:
                    enemy.sprite_id = 'enemy'

            # draw cat
            self.player.render(self.screen)

            if self.ghostmode:
                if flicker:
                    self.player.sprite_id = 'cat_ghost'
                else:
                    self.player.sprite_id = 'cat_ghost2'


        # game over
        if self.gameover:
            self.font.centerText(self.screen, 'GAME OVER', y=10)
            self.font.centerText(self.screen, 'PRESS SPACE', y=12)

        if self.levelcomplete:
            self.font.centerText(self.screen, 'LEVEL COMPLETE!', y=10)
            self.font.centerText(self.screen, 'PRESS SPACE', y=12)

        if self.gamecomplete:
            self.screen.fill((0,0,0))

            self.screen.blit(TILES['cat'], (SCR_W / 2 - TW / 2, SCR_H / 2 - TH / 2))

            self.font.centerText(self.screen, 'CONGRATULATIONS!', y=4)
            self.font.centerText(self.screen, 'YOU WON THE GAME!', y=6)
            self.font.centerText(self.screen, 'PRESS SPACE TO RESTART', y=16)

        if self.titlescreen:
            self.screen.fill((0,0,0))

            for y in range(LEV_H):
                for x in range(LEV_W):
                    self.screen.blit(TILES[' '], (x * TW, y * TH))

            self.screen.blit(TILES['cat'], (SCR_W / 2 - TW / 2, SCR_H / 2 - TH / 2))

            self.bigfont.centerText(self.screen, 'NINE LIVES', y=3)
            self.font.centerText(self.screen, 'A BODENSEE GAMEJAM 2023 GAME BY', y=14)
            self.font.centerText(self.screen, 'MSMR, ROSOBE, ZEHA', y=16)

        if self.exitmode:
            self.font.centerText(self.screen, 'PAUSED', y=8)
            self.font.centerText(self.screen, 'R = RETRY', y=10)
            self.font.centerText(self.screen, 'ESC = BACK TO GAME', y=11)
            self.font.centerText(self.screen, 'Q = QUIT', y=12)


        # show editmode
        if self.editmode and not self.saving:
            self.font.drawText(self.screen, 'EDIT MODE --- LEVEL ' + str(self.levelno), x=1, y=21)
            self.cursor.render(self.screen)
        if self.editmode and self.saving:
            self.font.drawText(self.screen, 'SAVE LEVEL ' + str(self.levelno) + '?  [S] no  /  [ENTER] OK ', x=1, y=21)




        pygame.display.flip()




    def run(self):
        self.running = True

        clock = pygame.time.Clock()

        while self.running:
            self.render()
            self.controls()

            if not self.gamecomplete and not self.levelcomplete and not self.gameover and not self.titlescreen:
                self.update()

            clock.tick(60)


game = Game()

game.loadLevel(1)
game.run()

pygame.quit()

