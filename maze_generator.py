import pygame, sys, random, math

from character import *

# Objects: Input window for what screen to display, x and y for position on display, squSize for size
#class Player:
#    def __init__(self, window, x, y, squSize):
#        self.window = window
#        self.image = pygame.transform.scale(pygame.image.load("./Images/player_right.png"), (squSize*14, squSize*27)).convert_alpha()
#        self.rect = self.image.get_rect()
#        self.window.blit(self.image, (x, y))

class Path:
    def __init__(self, window, x, y, squSize):
        self.window = window
        self.image = pygame.transform.scale(pygame.image.load("./Images/floor.png"), (squSize*2, squSize*2)).convert()
        self.window.blit(self.image, (x, y))

class EndPath(pygame.sprite.Sprite):
    def __init__(self, window, x, y, squSize):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.transform.scale(pygame.image.load("./Images/end_floor.png"), (squSize*2, squSize*2)).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.window.blit(self.image, (x, y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, window, x, y, squSize):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.transform.scale(pygame.image.load("./Images/wall.png"), (squSize*2, squSize*2)).convert()
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.window.blit(self.image, (x, y))

    def getRect(self):
        return self.rect

    def getPos(self):
        return (self.x, self.y)

class Spawner(pygame.sprite.Sprite):
    def __init__(self, window, x, y, squSize):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.transform.scale(pygame.image.load("./Images/spawner.png"), (squSize*2, squSize*2)).convert()
        self.rect = self.image.get_rect()
        self.window.blit(self.image, (x, y))

class Maze:
    def __init__(self, window, player):
        self.scale = 8
        self.squSize = 10 * self.scale
        self.window = window
        self.surface = pygame.Surface((window.get_width(), window.get_height()))
        self.screen_width = window.get_width() * self.scale
        self.screen_height = window.get_height() * self.scale
        self.init_pos_x = 100 * self.scale
        self.init_pos_y = self.screen_height/2
        self.record = []
        self.record_end = []
        self.record_path = []
        self.record_wall = []
        self.record_spawn = []
        self.record_mon = []
        self.margin = 60
        self.load_dist = 50 * self.scale


        self.midpoint = (self.window.get_width()//2, self.window.get_height()//2)

        self.player = player

        self.wall_group = pygame.sprite.Group()
        self.end_group = pygame.sprite.Group()
        self.spawner_group = pygame.sprite.Group()
        self.monster_group = pygame.sprite.Group()

        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Generating the main path that the player will walk on
        # WILL NOT generate path, will only setup positions of each individual path objects
        def generatePath():
            # This variables contain where exactly the path object should be at and what object should spawn
            self.record_path = []
            self.record_end = []
            # Creates 4 different paths
            for path in range(4):
                # Variables to help generate new paths
                self.pos_x = self.init_pos_x
                self.pos_y = self.init_pos_y

                # Logic:
                # Randomly picks a number between 0 - 3(exclusive)
                # On 0, self.pos_x + half of self.squSize, moving right
                # On 1, self.pos_y + half of self.squSize, moving down
                # On 2, self.pos_y - half of self.squSize, moving left
                # Then add self.pos_x and self.pos_y to the recording variables
                while True:
                    self.record = [[self.init_pos_x, self.init_pos_y, 0]]
                    rand = random.randrange(0, 3)
                    last_move = rand
                    if rand == 0 and not([self.pos_x + (self.squSize*2), self.pos_y, 0] in self.record):
                        if self.pos_x + self.squSize*2 > self.screen_width - 80:
                            break
                        else:
                            self.pos_x += (self.squSize*2)
                            if not([self.pos_x + self.squSize*2, self.pos_y, 0] in self.record_path):
                                self.record_path.append([self.pos_x, self.pos_y, 0])
                    elif self.pos_y > self.margin and self.pos_y < self.screen_height - self.margin:
                        if rand == 1 and last_move != 2 and not([self.pos_x, self.pos_y + (self.squSize*2), 0] in self.record):
                            self.pos_y += (self.squSize*2)
                            if not([self.pos_x, self.pos_y + self.squSize*2, 0] in self.record_path):
                                self.record_path.append([self.pos_x, self.pos_y, 0])
                        elif rand == 2 and last_move != 1 and not([self.pos_x, self.pos_y - (self.squSize*2), 0] in self.record):
                            self.pos_y -= (self.squSize*2)
                            if not([self.pos_x, self.pos_y - self.squSize*2, 0] in self.record_path):
                                self.record_path.append([self.pos_x, self.pos_y, 0])
                    elif self.pos_y <= self.margin:
                        self.pos_y += (self.squSize*2)
                        if not([self.pos_x, self.pos_y + self.squSize*2, 0] in self.record_path):
                            self.record_path.append([self.pos_x, self.pos_y, 0])
                    elif self.pos_y >= self.screen_height - self.margin:
                        self.pos_y -= (self.squSize*2)
                        if not([self.pos_x, self.pos_y - self.squSize*2, 0] in self.record_path):
                            self.record_path.append([self.pos_x, self.pos_y, 0])

            # On the last path, at the end, create 3x3 square
            for square in [[self.squSize*2, 0], [-self.squSize*2, 0], [0, self.squSize*2], [0, -self.squSize*2], [-self.squSize*2, -self.squSize*2], [-self.squSize*2, self.squSize*2], [self.squSize*2, -self.squSize*2], [self.squSize*2, self.squSize*2], [0, 0]]:
                self.record_end.append([self.pos_x + square[0], self.pos_y + square[1], 1])
            self.record_end.append([self.init_pos_x, self.init_pos_y, 1])

        # Generating wall
        # WILL NOT generate wall, will only setup positions of each individual wall objects
        def generateWall():
            self.record_wall = []
            # Logic:
            # Goes through every point and checks if there is a path object
            # If path object detect, it checks every point adjacent to it
            # If path object not detected, create wall object
            for row in range(0, self.screen_height, self.squSize*2):
                for col in range(0, self.screen_width, self.squSize*2):
                    if [col, row, 0] in self.record_path or [col, row, 1] in self.record_end:
                        for square in [[self.squSize*2, 0], [-self.squSize*2, 0], [0, self.squSize*2], [0, -self.squSize*2], [-self.squSize*2, -self.squSize*2], [-self.squSize*2, self.squSize*2], [self.squSize*2, -self.squSize*2], [self.squSize*2, self.squSize*2]]:
                            if not([col + square[0], row + square[1], 0] in self.record_path) and not([col + square[0], row + square[1], 1] in self.record_end) and not([col + square[0], row + square[1], 1] in self.record_wall):
                                self.record_wall.append([col + square[0], row + square[1], 2])

        # Generating spawners
        # WILL NOT generate spawners, will only setup positions of each individual spawner objects
        def generateSpawners():
            self.record_spawn = []
            # Logic:
            # If there exist a path at where function is at, it's at a corner containing a wall object to the left,
            # and it have a valid dist_from_spwn, then create spawner
            dist_from_spwn = 150 * self.scale
            for row in range(0, self.screen_height, self.squSize*2):
                for col in range(0, self.screen_width, self.squSize*2):
                    if [col - self.squSize*2, row, 2] in self.record_wall and [col - self.squSize*2, row + self.squSize*2, 2] in self.record_wall and [col, row + self.squSize*2, 2] in self.record_wall and [col, row, 0] in self.record_path and not([col, row, 1] in self.record_end):
                        isFar = True
                        for point in self.record_spawn:
                            if math.sqrt((point[0] - col)**2 + (point[1] - row)**2) < dist_from_spwn:
                                isFar = False
                        if isFar == True:
                            self.record_spawn.append([col, row, 3])
                    elif [col - self.squSize*2, row, 2] in self.record_wall and [col - self.squSize*2, row - self.squSize*2, 2] in self.record_wall and [col, row - self.squSize*2, 2] in self.record_wall and [col, row, 0] in self.record_path and not([col, row, 1] in self.record_end):
                        isFar = True
                        for point in self.record_spawn:
                            if math.sqrt((point[0] - col)**2 + (point[1] - row)**2) < dist_from_spwn:
                                isFar = False
                        if isFar == True:
                            self.record_spawn.append([col, row, 3])

        # This function is for spawning monsters where the spawners are at
        def spawnMonsters(spawners):
            self.temp_record = []
            for point in self.record_spawn:
                if not(point in self.temp_record):
                    self.temp_record.append(point)
            self.record_spawn = self.temp_record[:]

            for point in spawners:
                self.record_mon.append([point[0], point[1], 4])

        # Creates all the objects
        def initializeObjects(displacement):
            # Logic:
            # Goes through all of the recordings of coordinate points and spawns the right object at that point
            self.record = self.record_path[:] + self.record_end + self.record_wall + self.record_spawn + self.record_mon
            for i in range(len(self.record)):
                if self.record[i][2] == 0:
                    path = Path(self.surface, self.record[i][0], self.record[i][1] + displacement, self.squSize)
                    self.record[i][1] += displacement
                elif self.record[i][2] == 1:
                    end_path = EndPath(self.surface, self.record[i][0], self.record[i][1] + displacement, self.squSize)
                    self.record[i][1] += displacement
                elif self.record[i][2] == 2:
                    wall = Wall(self.surface, self.record[i][0], self.record[i][1] + displacement, self.squSize)
                    self.wall_group.add(wall)
                    self.record[i][1] += displacement
                elif self.record[i][2] == 3:
                    spawner = Spawner(self.surface, self.record[i][0], self.record[i][1] + displacement, self.squSize)
                    self.spawner_group.add(spawner)
                    self.record[i][1] += displacement
                elif self.record[i][2] == 4:
                    monster = Monster(self.surface, self.record[i][0], self.record[i][1] + displacement, 4, self, self.player)
                    self.spawner_group.add(monster)
                    self.record[i][1] += displacement

            self.player_x = 0
            self.player_y = 0
            self.window.blit(self.surface, (0, 0))

        # Calls functions
        def createMaze():
            self.surface.fill(BLACK)
            self.record = []
            # The while loop allows the maze have more tunnels making it look more like a maze
            while len(self.record_wall) < 1500:
                self.surface.fill(BLACK)
                generatePath()
                generateWall()
            generateItems()
            initializeObjects(-(self.scale - 1) * (window.get_height() / 2))
        def generateItems():
            generateSpawners()
            spawnMonsters(self.record_spawn)
        def setUpMap():
            createMaze()
            generateItems()
        createMaze()

    def moveObjects(self, disp_x, disp_y):
        self.temp_record = []
        # Makes sure that there are no duplicates in coordinate points for walls
        for point in self.record_wall:
            if not(point in self.temp_record):
                self.temp_record.append(point)
        self.record_wall = self.temp_record[:]
        self.record = self.record_path[:] + self.record_end + self.record_wall + self.record_spawn + self.record_mon
        self.surface.fill((0,0,0))
        self.wall_group.empty()
        self.spawner_group.empty()
        # Goes through each point and if player is at some distance from those points, objects will spawn at points
        for i in range(len(self.record)):
            if self.record[i][2] == 0:
                if math.sqrt((self.record[i][0] - self.surface.get_width()/2)**2 + (self.record[i][1] - self.surface.get_height()/2)**2) < self.load_dist:
                    path = Path(self.surface, self.record[i][0] + disp_x, self.record[i][1] + disp_y, self.squSize)
                self.record[i][1] += disp_y
                self.record[i][0] += disp_x
            if self.record[i][2] == 1:
                if math.sqrt((self.record[i][0] - self.surface.get_width()/2)**2 + (self.record[i][1] - self.surface.get_height()/2)**2) < self.load_dist:
                    end_path = EndPath(self.surface, self.record[i][0] + disp_x, self.record[i][1] + disp_y, self.squSize)
                    self.end_group.add(end_path)
                self.record[i][1] += disp_y
                self.record[i][0] += disp_x
            if self.record[i][2] == 2:
                if math.sqrt((self.record[i][0] - self.surface.get_width()/2)**2 + (self.record[i][1] - self.surface.get_height()/2)**2) < self.load_dist:
                    wall = Wall(self.surface, self.record[i][0] + disp_x, self.record[i][1] + disp_y, self.squSize)
                    self.wall_group.add(wall)
                self.record[i][1] += disp_y
                self.record[i][0] += disp_x
            if self.record[i][2] == 3:
                if math.sqrt((self.record[i][0] - self.surface.get_width()/2)**2 + (self.record[i][1] - self.surface.get_height()/2)**2) < self.load_dist:
                    spawner = Spawner(self.surface, self.record[i][0] + disp_x, self.record[i][1] + disp_y, self.squSize)
                    self.spawner_group.add(spawner)
                self.record[i][1] += disp_y
                self.record[i][0] += disp_x
            if self.record[i][2] == 4:
                if math.sqrt((self.record[i][0] - self.surface.get_width()/2)**2 + (self.record[i][1] - self.surface.get_height()/2)**2) < self.load_dist:
                    monster = Monster(self.surface, self.record[i][0] + disp_x, self.record[i][1] + disp_y, 4, self, self.player)
                    self.monster_group.add(monster)
                self.record[i][1] += disp_y
                self.record[i][0] += disp_x
        self.window.blit(self.surface, (self.player_x, self.player_y))

    # Function that gets Groups
    def getGroups(self, type):
        if type == "wall":
            return self.wall_group
        elif type == "end":
            return self.end_group

# Main is only used for testing
def main():
    pygame.init()
    window = pygame.display.set_mode(size=(1200, 800))
    #maze = Maze(window, ) #error said to add player (originally only had window)
    speed = 6           #and then said player not defined
    BLACK = (0, 0, 0)

    while True:
        test = Player(window, 600, 400, 4)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            window.fill(BLACK)
            maze.moveObjects(0, -speed)
            test = Player(window, 600, 400, 4)
        if key[pygame.K_UP]:
            window.fill(BLACK)
            maze.moveObjects(0, speed)
            test = Player(window, 600, 400, 4)
        if key[pygame.K_RIGHT]:
            window.fill(BLACK)
            maze.moveObjects(-speed, 0)
            test = Player(window, 600, 400, 4)
        if key[pygame.K_LEFT]:
            window.fill(BLACK)
            maze.moveObjects(speed, 0)
            test = Player(window, 600, 400, 4)
        pygame.display.update()

if __name__ == "__main__":
    main()
