# Master File

# Imports from other files
from new_starter import *
from character import *
from maze_generator import *

def clearWindow(window):
    window.fill(BLACK)

def main():
    pygame.init()
    window = pygame.display.set_mode(size=(1200, 800))
    speed = 4
    BLACK = (0, 0, 0)

    clock = pygame.time.Clock()

    startHasInit = True

    while True:
        # Makes sure that the start button is clicked before the game starts
        if startHasInit:
            if starterLoop(window):
                global player
                global maze
                global monster
                window.fill(BLACK)
                player = Player(window, window.get_width()/2, window.get_height()/2, 4, None)
                maze = Maze(window, player)
                maze.moveObjects(-200, 0)
                player = Player(window, window.get_width()/2, window.get_height()/2, 4, maze)
            startHasInit = False
        else:
            # For the quiting
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            # This part starts up the game
            key = pygame.key.get_pressed() # Gets the key that is pressed
            if player.move(key, speed) == False:
                if congrats_screen(window) == False: # Goes to the congrats screen if player wins
                    window.fill(BLACK)
                    player = Player(window, window.get_width()/2, window.get_height()/2, 4, None)
                    maze = Maze(window, player)
                    maze.moveObjects(-200, 0)
                    player = Player(window, window.get_width()/2, window.get_height()/2, 4, maze)

            if key[K_p]: # Pause during the game if key p is pressed
                paused = True
                pause(window, player, key)

        pygame.display.update()

if __name__ == "__main__":
    main()
