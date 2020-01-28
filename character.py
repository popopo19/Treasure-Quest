import pygame
import random, math


class Player(pygame.sprite.Sprite):
    def __init__(self, window, x, y, size, maze):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load("./Images/player_right.png"), (self.size*14, self.size*27)).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        self.midpoint = (x, y)
        self.window.blit(self.image, self.midpoint)
        self.maze = maze

        self.left = pygame.Rect(self.midpoint[0], self.midpoint[1]+20, 10, 78)
        self.top = pygame.Rect(self.midpoint[0]+5, self.midpoint[1], 45, 10)
        self.right = pygame.Rect(self.midpoint[0]+50, self.midpoint[1]+20, 10, 78)
        self.bottom = pygame.Rect(self.midpoint[0]+5, self.midpoint[1]+108, 45, 10)

        self.health = 3

        # Setup for the animation
        # Using for loop to slow down or speed up player
        self.anim_speed = 10
        self.right_anim = ["./Images/player_right_run1.png" for i in range(self.anim_speed)] + ["./Images/player_right_run2.png" for i in range(self.anim_speed)]
        self.right_count = 0
        self.left_anim = ["./Images/player_left_run1.png" for i in range(self.anim_speed)] + ["./Images/player_left_run2.png" for i in range(self.anim_speed)]
        self.left_count = 0
        self.front_anim = ["./Images/player_front_run1.png" for i in range(self.anim_speed)] + ["./Images/player_front_run2.png" for i in range(self.anim_speed)]
        self.front_count = 0
        self.back_anim = ["./Images/player_back_run1.png" for i in range(self.anim_speed)] + ["./Images/player_back_run2.png" for i in range(self.anim_speed)]
        self.back_count = 0

    # Next four functions plays the animation for specific direction
    def moveRight(self):
        self.image.fill((255, 255, 255, 0))
        self.window.blit(self.image, (self.window.get_width()/2, self.window.get_height()/2))
        self.image = pygame.transform.scale(pygame.image.load(self.right_anim[self.right_count]), (self.size*14, self.size*27)).convert_alpha()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.window.blit(self.image, self.midpoint)

        if self.right_count == len(self.right_anim) - 1:
            self.right_count = 0
        else:
            self.right_count += 1

    def moveLeft(self):
        self.image.fill((255, 255, 255, 0))
        self.window.blit(self.image, (self.window.get_width()/2, self.window.get_height()/2))
        self.image = pygame.transform.scale(pygame.image.load(self.left_anim[self.left_count]), (self.size*14, self.size*27)).convert_alpha()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.window.blit(self.image, self.midpoint)

        if self.left_count == len(self.left_anim) - 1:
            self.left_count = 0
        else:
            self.left_count += 1

    def moveBack(self):
        self.image.fill((255, 255, 255, 0))
        self.window.blit(self.image, (self.window.get_width()/2, self.window.get_height()/2))
        self.image = pygame.transform.scale(pygame.image.load(self.back_anim[self.back_count]), (self.size*14, self.size*25)).convert_alpha()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.window.blit(self.image, self.midpoint)

        if self.back_count == len(self.back_anim) - 1:
            self.back_count = 0
        else:
            self.back_count += 1

    def moveFront(self):
        self.image.fill((255, 255, 255, 0))
        self.window.blit(self.image, (self.window.get_width()/2, self.window.get_height()/2))
        self.image = pygame.transform.scale(pygame.image.load(self.front_anim[self.front_count]), (self.size*14, self.size*27)).convert_alpha()
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.window.blit(self.image, self.midpoint)

        if self.front_count == len(self.front_anim) - 1:
            self.front_count = 0
        else:
            self.front_count += 1
    def moveNot(self):
        self.image = pygame.transform.scale(pygame.image.load("./Images/player_right.png"), (self.size*14, self.size*27)).convert_alpha()
        self.window.blit(self.image, self.midpoint)

    # Used to move the play and scroll the maze
    def move(self, key, speed):
        wall_list = self.maze.getGroups("wall").sprites()
        self.canL = True
        self.canR = True
        self.canT = True
        self.canB = True
        # Returns if player has collided with wall or not
        # If collided, player cannot move in direction of wall
        for wall in wall_list:
            if self.left.colliderect(wall.rect):
                self.canL = False
            if self.right.colliderect(wall.rect):
                self.canR = False
            if self.top.colliderect(wall.rect):
                self.canT = False
            if self.bottom.colliderect(wall.rect):
                self.canB = False
        # For the key that is pressed, animate player and move maze in opposite direction
        if key[pygame.K_RIGHT] and self.canR:
            self.maze.moveObjects(-speed, 0)
            self.moveRight()
        if key[pygame.K_LEFT] and self.canL:
            self.maze.moveObjects(speed, 0)
            self.moveLeft()
        if key[pygame.K_UP] and self.canT:
            self.maze.moveObjects(0, speed)
            if key[pygame.K_LEFT] and self.canL:
                self.moveLeft()
            elif key[pygame.K_RIGHT] and self.canR:
                self.moveRight()
            elif self.canB:
                self.moveBack()
        if key[pygame.K_DOWN] and self.canB:
            self.maze.moveObjects(0, -speed)
            if key[pygame.K_LEFT] and self.canL:
                self.moveLeft()
            elif key[pygame.K_RIGHT] and self.canR:
                self.moveRight()
            elif self.canT:
                self.moveFront()
        if not(key[pygame.K_DOWN] or key[pygame.K_UP] or key[pygame.K_RIGHT] or key[pygame.K_LEFT]):
            self.maze.moveObjects(0, 0)
            self.moveNot()
        # Checks if player is at the end and returns True if so
        if math.sqrt((self.y - self.maze.record_end[0][1])**2 + (self.x - self.maze.record_end[0][0])**2) < 100:
            self.window.fill((0,0,0))
            return False

# IN DEVELOPMENT
class Monster(pygame.sprite.Sprite):
    def __init__(self, window, x, y, size, maze, player):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load("./Images/monster_front.png"), (self.size*14, self.size*27)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.midpoint = (x, y)
        self.window.blit(self.image, (x, y))
        self.maze = maze
        self.player = player

        self.x = x
        self.y = y
        self.jump_dist = 10

        self.left = pygame.Rect(self.midpoint[0], self.midpoint[1]+20, 10, 78)
        self.top = pygame.Rect(self.midpoint[0]+5, self.midpoint[1], 45, 10)
        self.right = pygame.Rect(self.midpoint[0]+50, self.midpoint[1]+20, 10, 78)
        self.bottom = pygame.Rect(self.midpoint[0]+5, self.midpoint[1]+108, 45, 10)

        self.health = 3

        self.right_anim = pygame.image.load("./Images/monster_right.png")
        self.left_anim = pygame.image.load("./Images/monster_left.png")
        self.front_anim = pygame.image.load("./Images/monster_front.png")
        self.back_anim = pygame.image.load("./Images/monster_back.png")

        self.image = pygame.transform.scale(pygame.image.load("./Images/monster_front.png"), (self.size*14, self.size*27)).convert_alpha()
        self.rect = self.image.get_rect()
        self.window.blit(self.image, (self.x, self.y))

    # Function makes monsters jump by changing y value up then down
    def jump(self, key):
        for j in [-1, 1]:
            for i in range(0, j*self.jump_dist, j*1):
                self.y += i
                self.player.move(key, 4)
                self.image = pygame.transform.scale(pygame.image.load("./Images/monster_front.png"), (self.size*14, self.size*27)).convert_alpha()
                self.window.blit(self.image, (self.x, self.y))
                pygame.display.flip()
