import copy
import datetime
import random
from time import time
import sys
import os
import pygame

import Button
import GenerationAndSolving as gs
import Settings

testGrid = [[0, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 6, 0, 0],
            [0, 0, 0, 1, 0, 9, 0, 0, 0],
            [0, 0, 9, 0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 9, 8, 0],
            [0, 4, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]

LIGHTBLUE = (96, 216, 232)
originalGrid = []
numOfPieces = 81 - (81 - 36)
piecesPlaced = 0


def drawNumbers():
    offx = 23
    offy = 18
    for i in range(0, 9):
        for j in range(0, 9):
            number = testGrid[i][j]
            if number != 0:
                out = font.render(str(number), True, pygame.Color("black"))
                screen.blit(out, pygame.Vector2(j * 60 + 10 + offx, i * 60 + 70 + offy))


def drawSeparationLines():
    index = 1
    while (index * 60 < 540):
        if (index == 4) or (index == 7) or (index == 9):
            pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(10, index * 60 + 10),
                             pygame.Vector2(550, index * 60 + 10), 4)
        if index % 3 == 0:
            pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(index * 60 + 10, 70),
                             pygame.Vector2(index * 60 + 10, 610), 4)
        index += 1


def drawBackground():
    screen.fill(pygame.Color("white"))
    pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(10, 70, 540, 540), 3)
    index = 1

    while (index * 60 < 540):
        pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(index * 60 + 10, 70),
                         pygame.Vector2(index * 60 + 10, 610), 2)
        pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(10, index * 60 + 10),
                         pygame.Vector2(550, index * 60 + 10), 2)
        index += 1
    pygame.draw.line(screen, pygame.Color("black"), pygame.Vector2(10, 540 + 10), pygame.Vector2(550, 540 + 10), 2)
    drawSeparationLines()


def inGrid(x, y):
    if x > 10 and x < 541 and y > 70 and y < 610:
        return True
    return False


def getCell(x, y):
    x = (x - 10) // 60
    y = (y - 70) // 60
    return y, x


def getCellCoord(x, y):
    x = x * 60 + 70
    y = y * 60 + 10
    return y, x

def getSquare(x,y):
    return x//3*3,y//3*3

def drawHelpersSquare(x,y):
    x, y = getSquare(x, y)
    for i in range(0, 3):
        for j in range(0, 3):
            x1, y1 = getCellCoord(x+i, y+j)
            pygame.draw.rect(screen, LIGHTBLUE, pygame.Rect(x1 + 2, y1 + 2, 58, 58))

def drawHelpers(x, y):
    for i in range(0, 9):
        x1, y1 = getCellCoord(x, i)
        pygame.draw.rect(screen, LIGHTBLUE, pygame.Rect(x1 + 2, y1 + 2, 58, 58))
        x1, y1 = getCellCoord(i, y)
        pygame.draw.rect(screen, LIGHTBLUE, pygame.Rect(x1 + 2, y1 + 2, 58, 58))

    drawSeparationLines()


def makeSelection(x, y, helpToggle):
    if (inGrid(x, y)):
        x, y = getCell(x, y)
        number = testGrid[x][y]
        if helpToggle:
            if (number == 0):
                drawHelpers(x, y)

            else:

                for i in range(0, 9):
                    for j in range(0, 9):
                        if testGrid[i][j] == testGrid[x][y]:
                            drawHelpersSquare(i, j)
                            drawHelpers(i, j)

        else:
            x1, y1 = getCellCoord(x, y)
            pygame.draw.rect(screen, LIGHTBLUE, pygame.Rect(x1 + 2, y1 + 2, 58, 58))


def getDifficulty():
    global numOfPieces
    if numOfPieces == 81 - (81 - 36):
        return "Easy"
    else:
        if numOfPieces == 81 - (81 - 31):
            return "Medium"
        else:
            if numOfPieces == 81 - (81 - 26):
                return "Hard"


def getTimeString(date):
    hour = str(date.hour - 2)
    if len(hour) == 1: hour = "0" + hour
    minute = str(date.minute)
    if len(minute) == 1: minute = "0" + minute
    seconds = str(date.second)
    if len(seconds) == 1: seconds = "0" + seconds
    return str(hour + ":" + minute + ":" + seconds)


def drawWinScreen(win):
    global currentTimePaused, paused,counter
    counter=False
    drawTimer()

    mili = int(time() * 1000)
    currentTimePaused = datetime.datetime.fromtimestamp((mili - milliseconds) / 1000.0)
    paused = True
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect(100, 150, 400, 300))
    pygame.draw.rect(screen, pygame.Color("black"), pygame.Rect(100, 150, 400, 300), 2)
    font = pygame.font.SysFont('none', 30)

    if win == True:
        anouncement = font.render("Game completed!", True, pygame.Color("black"))
    else:
        anouncement = font.render("Game lost,the time has expired!", True, pygame.Color("black"))
    screen.blit(anouncement, (100 + (400 / 2 - anouncement.get_width() / 2), 175))
    info1 = "Difficulty:" + getDifficulty()
    if win == True:
        info2 = "Time:" + getTimeString(currentTimePaused)
    else:
        info2 = "Pieces left:" + str(81 - piecesPlaced - numOfPieces)
    info3 = "Tips used:" + str(tipsUsed)
    info4 = "Mistakes made:" + str(mistakes)
    info5 = "Hit start to play again or choose another puzzle!"
    info1 = font.render(info1, True, pygame.Color("black"))
    info2 = font.render(info2, True, pygame.Color("black"))
    info3 = font.render(info3, True, pygame.Color("black"))
    info4 = font.render(info4, True, pygame.Color("black"))
    font = pygame.font.SysFont('none', 25)
    info5 = font.render(info5, True, pygame.Color("black"))
    screen.blit(info1, (100 + (400 / 2 - info1.get_width() / 2), 225))
    screen.blit(info2, (100 + (400 / 2 - info2.get_width() / 2), 275))
    screen.blit(info3, (100 + (400 / 2 - info3.get_width() / 2), 325))
    screen.blit(info4, (100 + (400 / 2 - info4.get_width() / 2), 375))
    screen.blit(info5, (100 + (400 / 2 - info5.get_width() / 2), 410))


def drawButtons():
    font = pygame.font.SysFont(None, 30)
    text = font.render("Difficulty", True, pygame.Color("black"))
    screen.blit(text, (580, 70))
    easy.draw(screen)
    medium.draw(screen)
    hard.draw(screen)
    pause.draw(screen)
    text = font.render("Tools", True, pygame.Color("black"))
    screen.blit(text, (580, 330))
    helper.draw(screen)
    tip.draw(screen)
    start.draw(screen)
    countdown.draw(screen)


def getTimeInSeconds(date):
    return date.second + date.minute * 60 + date.hour * 60 * 60


def drawTimer():
    global paused, currentTimePaused, milliseconds, counter
    font = pygame.font.SysFont(None, 30)
    if not counter:
        text = font.render("Timer:", True, pygame.Color("black"))
    else:
        text = font.render("Counter:", True, pygame.Color("black"))
    screen.blit(text, (10, 30))
    mili = int(time() * 1000)
    if paused == False:
        currentTime = datetime.datetime.fromtimestamp((mili - milliseconds) / 1000.000)
    else:
        milliseconds = mili - currentTimePaused.second * 1000.000 - currentTimePaused.minute * 60 * 1000.000 - (
                    currentTimePaused.hour - 2) * 60 * 60 * 1000.000

    if paused == False:
        if counter == True:
            cnt = getCounterInSeconds()
            dif = getTimeInSeconds(currentTime)
            if cnt + 2 * 60 * 60 - dif > 0:
                currentTime = datetime.datetime.fromtimestamp((cnt + 2 * 60 * 60 - dif))
            else:
                currentTime = datetime.datetime.fromtimestamp(1)

        hour = str(currentTime.hour - 2)
        if len(hour) == 1: hour = "0" + hour
        minute = str(currentTime.minute)
        if len(minute) == 1: minute = "0" + minute
        seconds = str(currentTime.second)
        if len(seconds) == 1: seconds = "0" + seconds
    else:

        hour = str(currentTimePaused.hour - 2)
        if len(hour) == 1: hour = "0" + hour
        minute = str(currentTimePaused.minute)
        if len(minute) == 1: minute = "0" + minute
        seconds = str(currentTimePaused.second)
        if len(seconds) == 1: seconds = "0" + seconds

    showTime = str(hour + ":" + minute + ":" + seconds)
    showTimeRender = font.render(showTime, True, pygame.Color("black"))
    if not counter:
        screen.blit(showTimeRender, (80, 31))
    else:
        screen.blit(showTimeRender, (100, 31))


def checkButtonClick(x, y):
    global milliseconds
    global testGrid, helpToggle, tipsUsed, paused, currentTimePaused, started, originalGrid, numOfPieces, piecesPlaced, counter, countdown, counterMode
    if easy.onButton(x, y) == True:
        testGrid = copy.deepcopy(gs.createGame(81 - 36))
        numOfPieces = 81 - (81 - 36)
        piecesPlaced = 0
        originalGrid = copy.deepcopy(testGrid)
        milliseconds = int(time() * 1000)
        initScore()
        resetTime()
        paused = True
        started = False
        counter = False
        counterMode = False
    if medium.onButton(x, y) == True:
        testGrid = copy.deepcopy(gs.createGame(81 - 31))
        numOfPieces = 81 - (81 - 31)
        piecesPlaced = 0
        originalGrid = copy.deepcopy(testGrid)
        milliseconds = int(time() * 1000)
        initScore()
        resetTime()
        paused = True
        started = False
        counter = False
        counterMode = False
    if hard.onButton(x, y) == True:
        testGrid = copy.deepcopy(gs.createGame(81 - 26))
        numOfPieces = 81 - (81 - 26)
        piecesPlaced = 0
        originalGrid = copy.deepcopy(testGrid)
        milliseconds = int(time() * 1000)
        initScore()
        resetTime()
        paused = True
        started = False
        counter = False
        counterMode = False

    if tip.onButton(x, y) == True:
        if not paused:
            tipGrid = copy.deepcopy(testGrid)
            gs.solveSudoku(tipGrid, 0, 0)
            while True:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                if (testGrid[x][y] != tipGrid[x][y]):
                    testGrid[x][y] = tipGrid[x][y]
                    piecesPlaced += 1
                    tipsUsed += 1
                    break

    if (helper.onButton(x, y) == True):
        if (helpToggle == False):
            helpToggle = True
        else:
            helpToggle = False
    if (pause.onButton(x, y) == True):
        if started == True:
            if counter == False and counterMode == False:
                if paused == False:
                    mili = int(time() * 1000)
                    currentTimePaused = datetime.datetime.fromtimestamp((mili - milliseconds) / 1000.0)
                    paused = True
                else:
                    paused = False
    if (start.onButton(x, y) == True):
        initScore()
        resetTime()
        piecesPlaced = 0
        started = True
        paused = False
        counterMode = False
        counter = False

        testGrid = copy.deepcopy(originalGrid)

    if (countdown.onButton(x, y) == True):
        if counter == False:
            counter = True
            paused = False
            counterMode = True

        if started==False:
            started=True


paused = True


def initScore():
    global tipsUsed, mistakes
    tipsUsed = 0
    mistakes = 0


def resetTime():
    global milliseconds, currentTimePaused
    milliseconds = int(time() * 1000)
    mili = int(time() * 1000)
    currentTimePaused = datetime.datetime.fromtimestamp((mili - milliseconds) / 1000.0)


def drawMistakes():
    global mistakes
    font = pygame.font.SysFont(None, 30)
    text = font.render("Mistakes:" + str(mistakes), True, pygame.Color("black"))
    screen.blit(text, (200, 30))
    global tipsUsed
    text = font.render("Tips Used:" + str(tipsUsed), True, pygame.Color("black"))
    screen.blit(text, (330, 30))


def highlightSelection(helpToggle):
    if (helpToggle == True):
        offx = 23
        offy = 18
        x, y = getCell(mx, my)
        number = testGrid[x][y]
        if number != 0:
            for i in range(0, 9):
                for j in range(0, 9):
                    if testGrid[i][j] == testGrid[x][y]:
                        out = font.render(str(number), True, pygame.Color("red"))
                        screen.blit(out, pygame.Vector2(j * 60 + 10 + offx, i * 60 + 70 + offy))


def getCounterInSeconds():
    if numOfPieces == 81 - (81 - 36):
        return 10 * 60
    if numOfPieces == 81 - (81 - 31):
        return 15 * 60
    if numOfPieces == 81 - (81 - 26):
        return 30 * 60


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


easy = Button.button(pygame.Color("green"), 580, 100, 100, 50, "Easy")
medium = Button.button(pygame.Color("brown"), 580, 170, 100, 50, "Medium")
hard = Button.button(pygame.Color("red"), 580, 240, 100, 50, "Hard")
helper = Button.button(LIGHTBLUE, 580, 360, 100, 50, "Helper")
tip = Button.button(pygame.Color("yellow"), 580, 420, 100, 50, "Tip")
pause = Button.button(pygame.Color("gray"), 580, 480, 100, 50, "Pause")
start = Button.button(pygame.Color("green"), 470, 20, 80, 40, "Start")
countdown = Button.button(pygame.Color("brown"), 580, 540, 100, 50, "Counter")
mistakes = 0
tipsUsed = 0
started = False
pygame.init()
pygame.display.set_caption('Sudoku')
counter = False

counterMode = False
font = pygame.font.SysFont(None, 40)
screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
testGrid = copy.deepcopy(gs.createGame(81 - 36))
originalGrid = copy.deepcopy(testGrid)
running = True
selection = False
mx, my = -1, -1
nextNumber = -1
milliseconds = int(time() * 1000)
currentTimePaused = datetime.datetime.fromtimestamp(0)

helpToggle = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            checkButtonClick(mx, my)
            if (inGrid(mx, my)):
                selection = True
        if selection == True:
            if event.type == pygame.KEYDOWN:
                if (not paused and started == True):
                    if event.key == pygame.K_KP0:
                        nextNumber = 0
                    if event.key == pygame.K_0:
                        nextNumber = 0
                    if event.key == pygame.K_KP1:
                        nextNumber = 1
                    if event.key == pygame.K_1:
                        nextNumber = 1
                    if event.key == pygame.K_KP2:
                        nextNumber = 2
                    if event.key == pygame.K_2:
                        nextNumber = 2
                    if event.key == pygame.K_KP3:
                        nextNumber = 3
                    if event.key == pygame.K_3:
                        nextNumber = 3
                    if event.key == pygame.K_KP4:
                        nextNumber = 4
                    if event.key == pygame.K_4:
                        nextNumber = 4
                    if event.key == pygame.K_KP5:
                        nextNumber = 5
                    if event.key == pygame.K_5:
                        nextNumber = 5
                    if event.key == pygame.K_KP6:
                        nextNumber = 6
                    if event.key == pygame.K_6:
                        nextNumber = 6
                    if event.key == pygame.K_KP7:
                        nextNumber = 7
                    if event.key == pygame.K_7:
                        nextNumber = 7
                    if event.key == pygame.K_KP8:
                        nextNumber = 8
                    if event.key == pygame.K_8:
                        nextNumber = 8
                    if event.key == pygame.K_KP9:
                        nextNumber = 9
                    if event.key == pygame.K_9:
                        nextNumber = 9
        else:
            nextNumber = -1

        if nextNumber != -1:
            x, y = getCell(mx, my)
            if (inGrid(mx, my)):
                if testGrid[x][y] == 0:
                    if (gs.isValid(x, y, testGrid, nextNumber) == True):
                        testGrid[x][y] = nextNumber
                        piecesPlaced += 1
                        temp = copy.deepcopy(testGrid)
                        if (gs.solveSudoku(temp, 0, 0) == False):
                            testGrid[x][y] = 0
                            piecesPlaced -= 1
                            mistakes += 1
                    else:
                        mistakes += 1
                    nextNumber = -1
                    selection = False
            else:
                selection = False
    drawBackground()
    if (selection == True):
        makeSelection(mx, my, helpToggle)

    drawNumbers()

    if (selection == True):
        if inGrid(mx, my):
            highlightSelection(helpToggle)
    drawButtons()
    drawTimer()
    drawMistakes()

    if (numOfPieces + piecesPlaced == 81):
        drawWinScreen(True)
    mili = int(time() * 1000)

    if (counterMode == True and (getCounterInSeconds() < getTimeInSeconds(
            datetime.datetime.fromtimestamp((mili - milliseconds) / 1000.000)) - 2 * 60 * 60 + 0.5)):
        drawWinScreen(False)

    pygame.display.flip()
