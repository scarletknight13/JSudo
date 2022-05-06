from bs4 import BeautifulSoup
import requests
import pygame, sys
import random
from pygame.constants import K_BACKSPACE, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, SRCCOLORKEY

pygame.init()
grid = [[random.randint(1, 9) for j in range(9)] for i in range(9) ]
filledSpaces = 0
startTime = 0
countDownTime = 200
mat = [[0]*9 for j in range(9)]
validList = [set() for i in range(27)]
USERSCORE = 0
COMPSCORE = 0
WIDTH, HEIGHT = 550, 650 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
FPS = 60
ORGFONT = pygame.font.SysFont('Comic Sans MS', 10)
NEWFONT = pygame.font.SysFont('Comic Sans MS', 25)
SCOREFONT = pygame.font.SysFont('Comic Sans MS', 17)

class button():
    def __init__(self, x, y, width, height, text = ''):
        self.x, self.y = x, y
        self.height, self.width = height, width 
        self.text = text

    def draw(self):
        pygame.draw.rect(WIN, WHITE, (self.x, self.y, self.width, self.height), 1)
        WIN.blit(self.text, (self.x + (self.width // 2 - self.text.get_width() // 2), self.y + (self.height // 2 - self.text.get_height() // 2)))
    
    def pressed(self, pos):
        returnVal = pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height
        return returnVal

clear_button_text = SCOREFONT.render("CLEAR", True, RED)
buttonHeight, buttonWidth = clear_button_text.get_height(), clear_button_text.get_width()
clear_button_pos = (200 + (350 - 200) // 2 - buttonWidth // 2, 500 + (HEIGHT - 500) // 1.25 - buttonHeight)
clear_button = button(clear_button_pos[0], clear_button_pos[1], buttonWidth, buttonHeight, clear_button_text)

def clear():
    global grid, filledSpaces, startTime, countDownTime, mat, validList, USERSCORE, COMPSCORE
    mat = [[0]*9 for j in range(9) ]
    validList = [set() for i in range(27)]
    USERSCORE = 0
    filledSpaces = 0

def restart():
    global grid, filledSpaces, startTime, countDownTime, mat, validList, USERSCORE, COMPSCORE
    clear()
    grid = [[random.randint(1, 9) for j in range(9)] for i in range(9) ]
    startTime = pygame.time.get_ticks()
    countDownTime = 900
    COMPSCORE = 0

def getScore():
    global grid
    score = 0
    tempList = []
    for i in range(5):
        currScore = 0
        lookupText = "https://www.sudokuweb.org/"
        html_text = requests.get(lookupText).text
        soup = BeautifulSoup(html_text, 'lxml')
        hidden_numbers = soup.find_all('span', {"true", "sedy"})
        arr = []
        matrix = []
        for i in hidden_numbers:
            arr.append(int(i.text))
            if(len(arr) == 9):
                matrix.append(arr)
                arr = []
        
        dict = [0 for x in range(9)]
        for i in range(9):
            for j in range(9):
                dict[matrix[i][j] - 1] += grid[i][j]

        dict.sort()
        dict[4], dict[-1] = dict[-1], dict[4] 
        for i, val in enumerate(dict):
            currScore += (i + 1) * val

        tempList.append(currScore)
    tempList.sort()
    score = tempList[0]
    return score
                
                
def draw_display():
    WIN.fill(WHITE)
    pygame.display.set_caption("JSudo")
    for i in range(0, 10):
        pygame.draw.line(WIN, BLACK, (50 + 50 * i, 50), (50 + 50 * i, 500), 4 if i % 3 == 0 else 2)
        pygame.draw.line(WIN, BLACK, (50, 50 + 50 * i), (500, 50 + 50 * i), 4 if i % 3 == 0 else 2)

    a = SCOREFONT.render("Score: " + str(USERSCORE), 1, BLACK)
    WIN.blit(a, (50 + (200 - 50) // 2 - a.get_width() // 2, 500 + (HEIGHT - 500) // 2 - a.get_height()))
    a = SCOREFONT.render("Comp: " + str(COMPSCORE), 1, BLACK)
    WIN.blit(a, (350 + (500 - 350) // 2 - a.get_width() // 2, 500 + (HEIGHT - 500) // 2 - a.get_height()))
    current_time = countDownTime - (pygame.time.get_ticks() - startTime) // 1000
    color = RED if current_time <= 120 else BLACK 
    a = SCOREFONT.render("Time: " + str(current_time // 60).rjust(2, '0') + ":" + str(current_time % 60).rjust(2, '0'), 1, color)
    WIN.blit(a, (200 + (350 - 200) // 2 - a.get_width() // 2, 500 + (HEIGHT - 500) // 2 - a.get_height()))
    clear_button.draw()
    
    for i in range(0, 9):
        for j in range(0, 9):
            if(mat[i][j] != 0):
                value = NEWFONT.render(str(mat[i][j]), 1, BLACK) 
                WIN.blit(value, ((i + 1) * 50 + 25 - value.get_width() // 2, (j + 1) * 50 + 25 - value.get_height() // 2))
            else:
                value = ORGFONT.render(str(grid[i][j]), 1, BLACK)
                WIN.blit(value, ((i + 1) * 50 + 10, (j + 1) * 50 + 10))

    pygame.display.update()

def isValid(i, j, num):
    flag = num not in validList[9+i] and num not in validList[18+j] and num not in validList[3 * (i // 3) + (j // 3)]
    return flag

def insert(pos):

    global USERSCORE, filledSpaces
    x, y = pos[0] // 50, pos[1] // 50
    if(pos[0] > 500 or pos[0] < 50 or pos[1] > 500 or pos[1] < 50):
        return
    else:
        run = True
        while(run):
             for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    temp_pos = pygame.mouse.get_pos()
                    x, y = temp_pos[0] // 50, temp_pos[1] // 50
                if event.type == pygame.KEYDOWN:
                    if event.key == K_BACKSPACE:
                        USERSCORE -= mat[x - 1][y - 1] * grid[x - 1][y - 1]
                        validList[9+(x - 1)].remove(mat[x - 1][y - 1])
                        validList[18+(y - 1)].remove(mat[x - 1][y - 1])
                        validList[3 * ((x - 1) // 3) + ((y - 1) // 3)].remove(mat[x - 1][y - 1])
                        mat[x - 1][y - 1] = 0
                        filledSpaces -= 1
                        run = False 
                    elif(event.key - 48 > 0 and event.key - 48 < 10):
                        temp = event.key - 48
                        if(isValid(x - 1, y - 1, temp) == True) :
                            USERSCORE -= mat[x - 1][y - 1] * grid[x - 1][y - 1]
                            mat[x - 1][y - 1] = temp
                            USERSCORE += mat[x - 1][y - 1] * grid[x - 1][y - 1]
                            validList[9+(x - 1)].add(temp)
                            validList[18+(y - 1)].add(temp)
                            validList[3 * ((x - 1) // 3) + ((y - 1) // 3)].add(temp)
                            filledSpaces += 1
                        run = False
               
def endGame():

    global USERSCORE, COMPSCORE
    WIN.fill(GREY)
    winOrLose = ""
    if(USERSCORE > COMPSCORE and filledSpaces == 81):
        winOrLose = "CONGRATS YOU BEAT THE COMPUTER"
    else:
        if(USERSCORE <= COMPSCORE):
            winOrLose = "YOU SCORE WASN'T HIGH ENOUGH, TRY AGAIN"
        else:
            winOrLose = "YOU DIDN'T COMPLETE THE BOARD" 

    status = SCOREFONT.render(winOrLose, 1, WHITE)
    WIN.blit(status, ( WIDTH // 2 - status.get_width() // 2, HEIGHT // 2 - status.get_height() // 2) )
    pygame.display.update()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key != "K_ESCAPE":
                restart()
                main()
            else:
                break

def main():

    global COMPSCORE, startTime
    COMPSCORE = getScore()
    clock = pygame.time.Clock()
    run = True
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if(clear_button.pressed(pos)):
                    clear()
                else:
                    insert(pos)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if startTime == 0:
            startTime = pygame.time.get_ticks()
        draw_display()
        current_time = countDownTime - (pygame.time.get_ticks() - startTime) // 1000
        if(current_time <= 0 or filledSpaces == 81):
            endGame()
            break
    
    pygame.quit()

if __name__ == "__main__":
    main()
