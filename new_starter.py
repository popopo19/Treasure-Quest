import pygame
from pygame.locals import *
import time
import tkinter as tk
from tkinter import *

from maze_generator import *

#Setting rbg to variable colors
gold = (207,183,31)
light_gold = (249, 223, 56)
red = (204, 9, 6)
white = (255, 255, 255)
black = (0,0,0)
green = (73, 152, 94)
dark_gold = (128, 128, 21)

#This is for test 1 <<<Does this make it a global variable
pause = False

#The button class setting the color, size and text of buttons
class button:
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #Drawing the buttons onto the screen and giving an outline to the button
    def draw(self,screen,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)

        #If there is not nothing for text then set it to this font and text size
        #Centering the text inside the button
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

    #This locates the position of the mouse and sees if it is above a button
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    #If the mouse position is over the button change it to a different color
    def changeColor(self, screen, newColor):
        self.color = newColor
        self.draw(screen, dark_gold)

#The tkinter window that
def instruct_win():
        root = tk.Tk()
        root.title("Game Instructions")
        root.configure(background="black")
        image1 = tk.PhotoImage(file="./Images/trophy.gif")
        image2 = tk.PhotoImage(file="./Images/arrowspic.gif")

        header_format = Label(root,
                       text="How to Play\n",
                       fg="yellow", bg="black",
                       font=" none 40 bold underline").pack()

        heading1 = "Goal:"
        heading2 = "Movements:"

        text1 = '''        To win the game you must find your way through the maze and find the
        treasure in the secret room. On your search, monsters will try and kill you.
        Monsters will immediately die when you shoot them and you will immediately
        die when they touch you. Whenever you need to pause the game, press the
        button at the top right cornor.'''

        text2 = '''        mouse = to aim and shoot\n
        Right arrow key = move forward \n
        Left arrow key = move backward \n
        Up arrow key = move up the screen \n
        Down arrow key = move down the screen'''
        #Should I talk about how to obtain the keys and mystery boxes

        heading1_format = Label(root,
                                justify = LEFT,
                                compound = LEFT,
                                padx = 0,
                                background = "black",
                                font = "none 25 bold underline",
                                text = heading1,
                                fg = "white").pack()

        text1_format = Label(root,
                             justify=LEFT,
                             compound = LEFT,
                             padx = 15,
                             background = "black",
                             text=text1,
                             fg = "white",
                             image=image1).pack()

        heading2_format = Label(root,
                                justify=RIGHT,
                                compound = RIGHT,
                                padx = 15,
                                background = "black",
                                font = "none 25 bold underline",
                                text=heading2,
                                fg = "white").pack()

        text2_format = Label(root,
                             justify=LEFT,
                             compound = LEFT,
                             padx = 15,
                             background = "black",
                             text=text2,
                             fg = "white",
                             image=image2).pack()


        return_button = tk.Button(root, text = "Return")
        return_button.pack()
        return_button['command'] = root.destroy
        root.mainloop()

# Loop for the menu
def starterLoop(screen):
    starterOver = False

    gold = (207,183,31)
    light_gold = (249, 223, 56)
    red = (204, 9, 6)
    white = (255, 255, 255)
    black = (0,0,0)
    #green = (73, 152, 94)
    dark_gold = (128, 128, 21)

    title_imgRect = (550, 300)
    monster_imgRect = (200, 300)

    title_img = pygame.image.load("./Images/treasurequest_img.png")
    title_img = pygame.transform.scale(title_img, title_imgRect)
    player_img = pygame.image.load("Images/player_right_run1.png")
    player_img = pygame.transform.scale(player_img, monster_imgRect)

    screen.blit(title_img, (325,10)) # paint to screen
    pygame.display.flip()
    screen.blit(player_img, (500,300))
    pygame.display.flip() # paint screen one time

    startButton = button((gold), 313,630,140,50, 'Start')
    controlButton = button((gold), 513, 630, 175, 50, 'Controls')
    exitButton = button((gold), 747, 630, 140, 50, 'Exit')

    startButton.draw(screen, dark_gold)
    controlButton.draw(screen, dark_gold)
    exitButton.draw(screen, dark_gold)

    while not starterOver:
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                starterOver = True
                pygame.quit
                quit()


            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.isOver(pos):
                    starterOver = True
                    print("works")
                    return True

                if controlButton.isOver(pos):
                    instruct_win()

                if exitButton.isOver(pos):
                    pygame.quit()
                    quit()


            if event.type == pygame.MOUSEMOTION:
                if startButton.isOver(pos):
                    startButton.changeColor(screen, light_gold)
                else:
                    startButton.changeColor(screen, gold)

                if controlButton.isOver(pos):
                    controlButton.changeColor(screen, light_gold)
                else:
                    controlButton.changeColor(screen, gold)

                if exitButton.isOver(pos):
                    exitButton.changeColor(screen, light_gold)
                else:
                    exitButton.changeColor(screen, gold)



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    loser_screen()

                if event.key == pygame.K_c:
                    congrats_screen()


def pause(screen, player, key):
    #making the pause button a global variable Test 1!If not put pause = True
    paused= True
    pause_image = pygame.image.load("./Images/pause_image.png")
    pause_image = pygame.transform.scale(pause_image, (455, 150))

    screen.blit(pause_image, (430,100)) # paint to screen
    pygame.display.flip()

    resumeButton = button((gold), 300,500,160,50, 'Resume')
    controlsButton = button((gold), 580, 500, 175, 50, 'Controls')
    quitButton = button((gold), 900, 500, 140, 50, 'Quit')
    #Should I put a restart screen

    resumeButton.draw(screen, dark_gold)
    controlsButton.draw(screen, dark_gold)
    quitButton.draw(screen, dark_gold)

    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if resumeButton.isOver(pos):
                    screen.fill((0,0,0))
                    player.move(key, 0)
                    paused = False

                if controlsButton.isOver(pos):
                    instruct_win()

                if quitButton.isOver(pos):
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if resumeButton.isOver(pos):
                    resumeButton.changeColor(screen, light_gold)
                else:
                    resumeButton.changeColor(screen, gold)

                if controlsButton.isOver(pos):
                    controlsButton.changeColor(screen, light_gold)
                else:
                    controlsButton.changeColor(screen, gold)

                if quitButton.isOver(pos):
                    quitButton.changeColor(screen, light_gold)
                else:
                    quitButton.changeColor(screen, gold)

                pygame.display.update()


def congrats_screen(screen):
    winner_gameOver = True
    screen.fill((0,0,0))

    congratsRect = (440, 150)
    congrats_mes_Rect = (575, 70)

    congrats_image = pygame.image.load("./Images/congrats_img.png")
    congrats_image = pygame.transform.scale(congrats_image, (congratsRect))

    congrats_mes_image = pygame.image.load("./Images/congrats_mes_img.png")
    congrats_mes_image = pygame.transform.scale(congrats_mes_image, (congrats_mes_Rect))

    screen.blit(congrats_image, (385,100)) # paint to screen
    screen.blit(congrats_mes_image, (322, 250))
    pygame.display.flip()

    winner_replayButton = button((gold), 495,450,210,50, 'Play Again')
    winner_quitButton = button((gold), 530, 530, 140, 50, 'Quit')

    winner_replayButton.draw(screen, dark_gold)
    winner_quitButton.draw(screen, dark_gold)

    pygame.display.update()

    while winner_gameOver:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if winner_replayButton.isOver(pos):
                    return False

                if winner_quitButton.isOver(pos):
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEMOTION:
                if winner_replayButton.isOver(pos):
                    winner_replayButton.changeColor(screen, light_gold)
                else:
                    winner_replayButton.changeColor(screen, gold)

                if winner_quitButton.isOver(pos):
                    winner_quitButton.changeColor(screen, light_gold)
                else:
                    winner_quitButton.changeColor(screen, gold)

                pygame.display.update()

def main():

    # Game Initialization
    pygame.init()

    # Game Resolution
    screen_width=1200
    screen_height=800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Monster Maze')

    clock = pygame.time.Clock()

    starterLoop(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause(screen)

if __name__ == "__main__":
    main()
