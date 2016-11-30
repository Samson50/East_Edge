import pygame, sys
import characters
import story
from pygame.locals import *
from images import *

class MiniPlayer:
    def __init__(self, x, y, sprites):
        self.y = y
        self.x = x
        self.left = Rect(x,  y,   7, 20)
        self.right= Rect(x+7,y,   7, 20)
        self.head = Rect(x,  y-1, 14,5 )
        self.foot = Rect(x,  y+16,14,5 )
        self.b_left = Rect(x-1,y, 6, 20)
        self.b_right = Rect(x+7,y,6, 20)
        self.sprites = sprites
        self.face = 0
        self.pace = 0

    def show(self, surface):
##        pygame.draw.rect(surface, (255,0,255),   self.b_left, 0)
##        pygame.draw.rect(surface, (255,0,255),   self.b_right, 0)
##        pygame.draw.rect(surface, (0,255,0),     self.right,0)
##        pygame.draw.rect(surface, (0,0,255),     self.left, 0)
##        pygame.draw.rect(surface, (255,0,0),     self.head, 0)
##        pygame.draw.rect(surface, (255,255,255), self.foot, 0)
        surface.blit(self.sprites[self.pace/3 + self.face*4], (self.x, self.y))

    def set_y(self, delt):
        self.y = delt
        self.b_left.y = delt
        self.b_right.y = delt
        self.left.y = delt
        self.right.y = delt
        self.head.y = delt-1
        self.foot.y = delt+16

    def set_x(self, delt):
        self.x = delt
        self.b_left.x = delt-1
        self.b_right.x = delt+7
        self.left.x = delt
        self.right.x = delt+7
        self.head.x = delt
        self.foot.x = delt

class Tile:
    def __init__(self, X, Y, image):
        self.rect = image.get_rect(x=X, y=Y)
        self.img = image

    def show(self, surface):
        surface.blit(self.img, (self.rect.x,self.rect.y))

class MiniGame:
    def __init__(self):
        self.y_off = 185
        self.x_off = 5
        self.player = MiniPlayer(15+self.x_off, 70+self.y_off, mini_sprite)
        self.l_limit = 5+self.x_off
        self.r_limit = 280+self.x_off
        self.background = mini_background
        self.frame = mini_frame
        self.running = True
        self.h_tile = Tile(10+self.x_off, 10+self.y_off, mini_health)
        self.bounds = [Rect(0,self.y_off,15,120),
                       Rect(0,self.y_off,10,300),
                       Rect(275,self.y_off,20,120)]
        self.tiles = []
        self.obstacles = []
        self.enemies = []
        self.goal = []
        self.result_text = []

    def gen_map(self, map_matrix):
        self.tiles = []
        self.obstacles = []
        self.enemies = []
        self.goal = []
        i = 0
        for tile in map_matrix[0][0]:
            if tile == 1:
                self.tiles.append(Tile(self.x_off+i*24, self.y_off+95, map_matrix[0][1]))
            i += 1
        for obstacle in map_matrix[1][0]:
            self.obstacles.append(Tile(self.x_off+obstacle[0], self.y_off+obstacle[1], map_matrix[1][1][obstacle[2]]))
        for enemy in map_matrix[2][0]:
            self.enemies.append(Tile(self.x_off+enemy[0], self.y_off+enemy[1], map_matrix[2][1][enemy[2]]))
        self.goal = [Tile(self.x_off+map_matrix[3][0], self.y_off, map_matrix[3][1])]

    def run(self, surface):
        fpsClock = pygame.time.Clock()
        health = 30
        health_counter = 0
        jump_force = -8
        y_delt = 0
        x_delt = -2

        while(self.running):
            ## Get Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_UP and self.player.foot.collidelist(self.tiles + self.obstacles) != -1:
                        y_delt = jump_force

            keys = pygame.key.get_pressed()

            if keys:
                if keys[K_RIGHT]:
                    x_pos = 4
                    self.player.face = 0
                    self.player.pace += 1
                else:
                    x_pos = 0
                if keys[K_LEFT]:
                    x_neg = -4
                    self.player.face = 1
                    self.player.pace += 1
                else:
                    x_neg = 0
                if not keys[K_LEFT] and not keys[K_RIGHT]:
                    self.player.pace = 0
                if not keys[K_UP]:
                    if y_delt < 0: y_delt = 0

                    ## Update Positions
                    ## Update y
            self.player.pace %= 12

            if (self.player.foot.collidelist(self.tiles + self.obstacles) == -1):
                y_delt += 1
                self.player.set_y(self.player.y + y_delt)
                if (self.player.left.collidelist(self.tiles + self.obstacles) != -1 and y_delt > 0):
                    self.player.set_y(
                        (self.tiles + self.obstacles)[self.player.left.collidelist(self.tiles + self.obstacles)].rect.y - self.player.left.height)
                if (self.player.right.collidelist(self.tiles + self.obstacles) != -1 and y_delt > 0):
                    self.player.set_y(
                        (self.tiles + self.obstacles)[self.player.right.collidelist(self.tiles + self.obstacles)].rect.y - self.player.right.height)
            else:
                self.player.set_y(self.player.y + y_delt)
                if (self.player.left.collidelist(self.tiles + self.obstacles) != -1 and y_delt > 0):
                    self.player.set_y(
                        (self.tiles + self.obstacles)[self.player.left.collidelist(self.tiles + self.obstacles)].rect.y - self.player.left.height)
                    y_delt = 0
                if (self.player.right.collidelist(self.tiles + self.obstacles) != -1 and y_delt > 0):
                    self.player.set_y(
                        (self.tiles + self.obstacles)[self.player.right.collidelist(self.tiles + self.obstacles)].rect.y - self.player.right.height)
                    y_delt = 0

            if (self.player.head.collidelist(self.tiles + self.obstacles) != -1):
                y_delt = 0
                self.player.set_y(
                    (self.tiles + self.obstacles)[self.player.head.collidelist(self.tiles + self.obstacles)].rect.y + (self.tiles + self.obstacles)[
                        self.player.head.collidelist(self.tiles + self.obstacles)].rect.height)

            ## move tile
            for tile in self.tiles + self.enemies + self.obstacles + self.goal: tile.rect.x += x_delt

            ## Update Positions
            ## Update x
            bl = self.player.b_left.collidelist(self.tiles + self.obstacles + self.bounds)
            br = self.player.b_right.collidelist(self.tiles + self.obstacles + self.bounds)
            if (bl != -1):
                self.player.set_x(min(max(self.player.x + x_pos + x_delt, self.l_limit), self.r_limit))
            elif (br != -1):
                self.player.set_x(min(max(self.player.x + x_neg + x_delt, self.l_limit), self.r_limit))
            else:
                self.player.set_x(min(max(self.player.x + x_pos + x_neg + x_delt, self.l_limit), self.r_limit))
                bl = self.player.b_left.collidelist(self.tiles + self.obstacles)
                br = self.player.b_right.collidelist(self.tiles + self.obstacles)
                if (bl != -1): self.player.set_x((self.tiles + self.obstacles)[bl].rect.x + (self.tiles + self.obstacles)[bl].rect.width)
                if (br != -1): self.player.set_x((self.tiles + self.obstacles)[br].rect.x - 10)

            ## End Game Conditionals
            if (bl != -1 and br != -1 and br != bl):
                print "pinch"
                if (self.player.left.collidelist(self.tiles + self.obstacles) != -1 or self.player.right.collidelist(self.tiles + self.obstacles) != -1):
                    self.running = False
                    health = 0

            if (self.player.left.colliderect(self.goal[0])):
                print "goal"
                self.running = False

            if (self.player.left.y > 120+self.y_off):
                print "drop"
                self.running = False
                health = 0

            ## Enemy Things
            if ((self.player.left.collidelist(self.enemies) != -1 or self.player.right.collidelist(self.enemies) != -1) and health_counter == 0):
                health -= 2
                health_counter = 12
            elif (health_counter > 0):
                health_counter -= 1

            ## Display the scene

            surface.blit(self.background, (0,self.y_off))

            self.goal[0].show(surface)
            for tile in self.tiles: tile.show(surface)
            for obstacle in self.obstacles: obstacle.show(surface)
            for enemy in self.enemies: enemy.show(surface)
            for i in range(0, health):
                self.h_tile.rect.x = 20 + i
                self.h_tile.show(surface)
            if (health_counter % 2 == 0):
                self.player.show(surface)

            surface.blit(self.frame, (0,self.y_off))

            pygame.display.update()
            fpsClock.tick(15)

        self.player.set_x(self.x_off+15)
        self.player.set_y(self.y_off+90)
        self.running = True
        return health


map_01 = [[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],mini_tile],
             [[[200,60,0],[150,75,0],[100,80,0],[250,55,1]],[mini_shelf,mini_wall]],
             [[[300,40,0],[365,60,0]],[mini_enemy]],
             [500,mini_goal]]

mini_maps = [map_01]
