# -*- coding: utf-8 -*-
# Author: Weichen Liao

import pygame
from shapes import define_shapes
from cut_grid import cut_grid_into_shapes
import signal
import random
import math
import copy

# Define the number of side size, initialize it as 9
side_size = 9

# make a virtual grid
matrixCoordinates = [[] for i in range(side_size)]
for i in range(side_size):
    for j in range(side_size):
        matrixCoordinates[i].append([i,j])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 153, 0)
LIGHT_BLUE = (153, 204, 255)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
WIDTH = 950
HEIGHT = 600

pygame.font.init()
BASICFONTSIZE = 25
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

# Positions and sizes
gridPos = (75, 75)
cellSize = 50

# pictures to load
imageWelcome = pygame.image.load('welcome.png')

# display the matrix
def display_matrix(matrix):
    for item in matrix:
        print(' '.join(map(str, item)))

# cut the grid into random shapes
#coordinatesList = cut_grid_into_shapes(matrixCoordinates)

# use the template from the project pdf
coordinatesList = ['0_0_4_11', '0_2_5_14', '0_4_5_1', '2_4_4_13', '1_7_4_11', '2_0_4_1', '2_6_3_6',
                   '3_0_4_9', '3_1_5_18', '3_4_5_16', '3_8_5_13', '4_6_5_19', '5_2_4_11', '6_0_4_3',
                   '6_5_5_16', '6_7_4_11', '7_1_5_18', '8_3_2_2', '8_5_4_1']

# use the standard answer from the project pdf
matrixAnswer = [list(map(str, [3, 1, 2, 4, 2, 1, 5, 4, 3])),
                list(map(str, [2, 4, 3, 1, 5, 4, 3, 1, 2])),
                list(map(str, [3, 1, 2, 4, 2, 1, 2, 4, 3])),
                list(map(str, [2, 4, 3, 1, 3, 5, 3, 1, 2])),
                list(map(str, [1, 5, 2, 4, 2, 1, 2, 4, 3])),
                list(map(str, [4, 3, 1, 3, 5, 4, 3, 5, 1])),
                list(map(str, [1, 2, 4, 2, 1, 2, 1, 4, 3])),
                list(map(str, [4, 5, 1, 3, 4, 5, 3, 2, 1])),
                list(map(str, [3, 2, 4, 2, 1, 2, 1, 4, 3]))]

# the matrix of standard answer
#matrixAnswer = [[random.choice(['1','2','3','4','5']) for i in range(side_size)] for j in range(side_size)]

# show a few fixed numbers at the beginning, eg:['0_4_2', '0_5_1']
# use the fixed numbers from the project pdf
fixedNumbers = ['0_4_2', '0_5_1', '1_2_3', '3_1_4', '3_4_3', '4_2_2', '5_4_5', '6_6_1', '7_3_3', '7_5_5', '7_8_1', '8_0_3', '8_5_2']

class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outlineColor=None):
        if outlineColor:
            pygame.draw.rect(window, outlineColor, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, BLACK)
            window.blit(text, (self.x + (math.floor(self.width/2) - math.floor(text.get_width()/2)), self.y + (math.floor(self.height/2) - math.floor(text.get_height()/2))))

    def isMouseOverTheButton(self, posMouse):
        if posMouse[0] > self.x and posMouse[0] < self.x + self.width:
            if posMouse[1] > self.y and posMouse[1] < self.y + self.height:
                return True
        return False


# draw thick lines to form the desired shape, coordinates is a list, eg:[[0,0],[0,1],[1,1],[1,2]]
def draw_shapes(coordinates, codeSpecialCase=''):
    # draw a line, start and end is defined according with the defination of coordinates, eg: '0_0_LA' means the LeftAbove point of (0,0)
    def draw_line(start, end):
        startX, startY, startPt = start.split('_')
        endX, endY, endPt = end.split('_')
        startX, startY, endX, endY = int(startX), int(startY), int(endX), int(endY)
        # Left Above
        if startPt == 'LA':
            s = [gridPos[0] + startY*cellSize, gridPos[1] + startX*cellSize]
        # Right Above
        elif startPt == 'RA':
            s = [gridPos[0] + (startY+1)*cellSize, gridPos[1] + startX*cellSize]
        # Right Bottom
        elif startPt == 'RB':
            s = [gridPos[0] + (startY+1)*cellSize, gridPos[1] + (startX+1)*cellSize]
        # Left Bottom
        elif startPt == 'LB':
            s = [gridPos[0] + startY*cellSize, gridPos[1] + (startX+1)*cellSize]
        else:
            raise Exception('startPt error')

        if endPt == 'LA':
            e = [gridPos[0] + endY * cellSize, gridPos[1] + endX * cellSize]
        elif endPt == 'RA':
            e = [gridPos[0] + (endY + 1) * cellSize, gridPos[1] + endX * cellSize]
        elif endPt == 'RB':
            e = [gridPos[0] + (endY + 1) * cellSize, gridPos[1] + (endX + 1) * cellSize]
        elif endPt == 'LB':
            e = [gridPos[0] + endY * cellSize, gridPos[1] + (endX + 1) * cellSize]
        else:
            raise Exception('endPt error')

        pygame.draw.line(screen, BLUE, (s[0],s[1]), (e[0],e[1]), width=3)
    # array is coordinates, eg:[[0,0],[0,1],[1,1],[1,2]]
    def get_common_lines(array, codeSpecialCase):
        res = []
        for i in range(len(array)-1):
            lastCoor = array[i]
            nextCoor = array[i+1]
            # left and right neighboring
            if lastCoor[0] == nextCoor[0]:
                # from left to right:
                if lastCoor[1] < nextCoor[1]:
                    res.append('_'.join([str(lastCoor[0]), str(lastCoor[1]), 'RA', 'RB']))
                    res.append('_'.join([str(nextCoor[0]), str(nextCoor[1]), 'LB', 'LA']))
                # from right to left
                else:
                    res.append('_'.join([str(lastCoor[0]), str(lastCoor[1]), 'LB', 'LA']))
                    res.append('_'.join([str(nextCoor[0]), str(nextCoor[1]), 'RA', 'RB']))
            # up and down neighboring
            elif lastCoor[1] == nextCoor[1]:
                # from up to down
                if lastCoor[0] < nextCoor[0]:
                    res.append('_'.join([str(lastCoor[0]), str(lastCoor[1]), 'RB', 'LB']))
                    res.append('_'.join([str(nextCoor[0]), str(nextCoor[1]), 'LA', 'RA']))
                # from down to up
                else:
                    res.append('_'.join([str(lastCoor[0]), str(lastCoor[1]), 'LA', 'RA']))
                    res.append('_'.join([str(nextCoor[0]), str(nextCoor[1]), 'RB', 'LB']))

        # there are a few special cases where the rules above doesn't work because the directions are confusing
        # **
        # **
        if codeSpecialCase == '4_11':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LA', 'RA']))
        # *
        # **
        # *
        elif codeSpecialCase == '4_16':
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LB', 'LA']))
        # ***
        #  *
        elif codeSpecialCase == '4_17':
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LA', 'RA']))
        #  *
        # **
        #  *
        elif codeSpecialCase == '4_18':
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'RA', 'RB']))
        #  *
        # ***
        elif codeSpecialCase == '4_19':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
        # **
        # **
        # *
        elif codeSpecialCase == '5_11':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'LA', 'RA']))
        # ***
        #  **
        elif codeSpecialCase == '5_12':
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'LA', 'RA']))
        #  *
        # **
        # **
        elif codeSpecialCase == '5_13':
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'RA', 'RB']))
        # **
        # ***
        elif codeSpecialCase == '5_14':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'LB', 'LA']))
        # **
        # **
        #  *
        elif codeSpecialCase == '5_15':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'RA', 'RB']))
        #  **
        # ***
        elif codeSpecialCase == '5_16':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RB', 'LB']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'RA', 'RB']))
        # *
        # **
        # **
        elif codeSpecialCase == '5_17':
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[4][0]), str(array[4][1]), 'LB', 'LA']))
        # ***
        # **
        elif codeSpecialCase == '5_18':
            res.append('_'.join([str(array[0][0]), str(array[0][1]), 'RA', 'RB']))
            res.append('_'.join([str(array[1][0]), str(array[1][1]), 'LA', 'RA']))
            res.append('_'.join([str(array[2][0]), str(array[2][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'LB', 'LA']))
            res.append('_'.join([str(array[3][0]), str(array[3][1]), 'RB', 'LB']))

        return res

    '''
    given a coordinate, draw 4 lines surrounding the box
    # firstCoo = [2,1]
    # posLeftAbove = [gridPos[0] + firstCoo[1]*cellSize, gridPos[1] + firstCoo[0]*cellSize]
    # posRightAbove = [gridPos[0] + (firstCoo[1]+1)*cellSize, gridPos[1] + firstCoo[0]*cellSize]
    # posRightBottom = [gridPos[0] + (firstCoo[1]+1)*cellSize, gridPos[1] + (firstCoo[0]+1)*cellSize]
    # posLeftBottom = [gridPos[0] + firstCoo[1]*cellSize, gridPos[1] + (firstCoo[0]+1)*cellSize]
    #
    # pygame.draw.line(screen, RED, (posLeftAbove[0], posLeftAbove[1]), (posRightAbove[0],posRightAbove[1]),width=2)
    # pygame.draw.line(screen, RED, (posRightAbove[0],posRightAbove[1]), (posRightBottom[0],posRightBottom[1]), width=2)
    # pygame.draw.line(screen, RED, (posRightBottom[0],posRightBottom[1]), (posLeftBottom[0], posLeftBottom[1]), width=2)
    # pygame.draw.line(screen, RED, (posLeftBottom[0], posLeftBottom[1]), (posLeftAbove[0], posLeftAbove[1]), width=2)
    '''
    linesToDraw = []
    for coo in coordinates:
        linesToDraw.append('_'.join([str(coo[0]), str(coo[1]), 'LA', 'RA']))
        linesToDraw.append('_'.join([str(coo[0]), str(coo[1]), 'RA', 'RB']))
        linesToDraw.append('_'.join([str(coo[0]), str(coo[1]), 'RB', 'LB']))
        linesToDraw.append('_'.join([str(coo[0]), str(coo[1]), 'LB', 'LA']))
    # remove the lines that boxes share
    linesCommon = get_common_lines(coordinates, codeSpecialCase)
    linesToDraw = [item for item in linesToDraw if item not in linesCommon]
    #print(linesToDraw)
    for item in linesToDraw:
        item = item.split('_')
        draw_line('_'.join([item[0],item[1],item[2]]), '_'.join([item[0],item[1],item[3]]))

    # draw_line('0_0_LA','0_0_RA')
    # draw_line('2_1_RA', '2_1_RB')
    # draw_line('3_3_RB', '3_3_LB')
    # draw_line('4_4_LB', '4_4_LA')

# put a text somewhere in the screen
def display_text(text, x_, y_, color=BLACK):
    cellSurf = BASICFONT.render('%s' % (str(text)), True, color)
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (math.floor(x_), math.floor(y_))
    screen.blit(cellSurf, cellRect)

# display one number in the given position
def put_single_numbers(coo, Num, gridPos, cellSize):
    if Num != '0':
        x_pos = gridPos[1]+coo[1]*cellSize+(cellSize-BASICFONTSIZE)/2
        y_pos = gridPos[0]+coo[0]*cellSize + (cellSize - BASICFONTSIZE)/2
        display_text(Num, x_pos, y_pos)

# display the numbers in the grid according to the number of matrix
# [[3,4],[3,4]]
def display_numbers(matrix, gridPos, cellSize):
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            put_single_numbers([row,col], str(matrix[row][col]), gridPos, cellSize)

# compare the consistency of 2 matrix
def compareMatrix(matrixA, matrixB):
    for i in range(side_size):
        for j in range(side_size):
            if int(matrixA[i][j]) != int(matrixB[i][j]):
                return False
    return True



pygame.init()

# Set the width and height of the screen [width, height]
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Kemaru - by Weichen Liao")

# Loop until the user clicks the close button.
done = False
# decide to stay in the welcome page or in the game page
stayInWelcomePage = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# define panel buttons here
buttonPlay = button(color=GREEN, x=800, y=400, width=100, height=40, text='Play')
buttonQuit = button(color=LIGHT_GRAY, x=800, y=460, width=100, height=40, text='Quit')
button3x3 = button(color=LIGHT_GRAY, x=250, y=460, width=100, height=40, text='3 x 3')
button6x6 = button(color=LIGHT_GRAY, x=400, y=460, width=100, height=40, text='6 x 6')
button9x9 = button(color=ORANGE, x=550, y=460, width=100, height=40, text='9 x 9')

button1 = button(color=LIGHT_GRAY, x=600, y=100, width=40, height=40, text='1')
button2 = button(color=LIGHT_GRAY, x=600, y=180, width=40, height=40, text='2')
button3 = button(color=LIGHT_GRAY, x=600, y=260, width=40, height=40, text='3')
button4 = button(color=LIGHT_GRAY, x=600, y=340, width=40, height=40, text='4')
button5 = button(color=LIGHT_GRAY, x=600, y=420, width=40, height=40, text='5')

buttonShowSolution = button(color=LIGHT_GRAY, x=700, y=100, width=200, height=40, text='show solution')
buttonReset = button(color=LIGHT_GRAY, x=700, y=170, width=200, height=40, text='reset')
buttonHint = button(color=LIGHT_GRAY, x=700, y=240, width=200, height=40, text='hint')
buttonNewGame = button(color=LIGHT_GRAY, x=700, y=310, width=200, height=40, text='new game')
buttonSubmit = button(color=YELLOW, x=700, y=380, width=200, height=40, text='submit')
buttonReturn = button(color=LIGHT_GRAY, x=700, y=450, width=200, height=40, text='return')


flagShowSolution = False
flagNewGame = False
flagReset = False
cooChosen = None
flagHint = False
flagSubmit = False
isCorrect = False
# a dict storing the number a player decides to put in the grid. eg:['0_0':'1','0_1':'5']
dictNumFromPlayer = {}
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        # get the position of mouse
        posMouse = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonPlay.isMouseOverTheButton(posMouse):
                stayInWelcomePage = False

            if buttonQuit.isMouseOverTheButton(posMouse):
                done = True

            if button3x3.isMouseOverTheButton(posMouse):
                button3x3.color = ORANGE
                button6x6.color = LIGHT_GRAY
                button9x9.color = LIGHT_GRAY
                side_size = 3
                cellSize = 150
                # every time you  enter the game, the game is always initialized as the same. it randomly changes when u click on the "New game" button
                coordinatesList = ['0_0_2_2', '0_2_3_2', '1_0_4_11']
                matrixAnswer = [list(map(str, [1, 2, 1])),
                                list(map(str, [3, 4, 3])),
                                list(map(str, [2, 1, 2]))]
                fixedNumbers = ['0_0_1']

            if button6x6.isMouseOverTheButton(posMouse):
                button3x3.color = LIGHT_GRAY
                button6x6.color = ORANGE
                button9x9.color = LIGHT_GRAY
                side_size = 6
                cellSize = 75
                coordinatesList = ['0_0_3_1', '0_3_4_5', '0_4_4_11', '1_0_5_18', '2_4_5_11', '3_0_5_11', '3_2_4_11', '4_5_2_1', '5_1_4_1']
                matrixAnswer = [list(map(str, [3, 2, 1, 4, 1, 2])),
                                list(map(str, [1, 4, 5, 2, 3, 4])),
                                list(map(str, [3, 2, 3, 1, 5, 2])),
                                list(map(str, [4, 1, 4, 2, 3, 1])),
                                list(map(str, [3, 2, 3, 1, 4 ,2])),
                                list(map(str, [5, 1, 4, 2, 3, 1]))]
                fixedNumbers = ['0_1_2', '0_3_4', '1_0_1', '2_2_3', '3_5_1', '4_4_4', '5_0_5']

            if button9x9.isMouseOverTheButton(posMouse):
                button3x3.color = LIGHT_GRAY
                button6x6.color = LIGHT_GRAY
                button9x9.color = ORANGE
                side_size = 9
                cellSize = 50
                # use the template from the project pdf
                coordinatesList = ['0_0_4_11', '0_2_5_14', '0_4_5_1', '2_4_4_13', '1_7_4_11', '2_0_4_1', '2_6_3_6',
                                   '3_0_4_9', '3_1_5_18', '3_4_5_16', '3_8_5_13', '4_6_5_19', '5_2_4_11', '6_0_4_3',
                                   '6_5_5_16', '6_7_4_11', '7_1_5_18', '8_3_2_2', '8_5_4_1']

                # use the standard answer from the project pdf
                matrixAnswer = [list(map(str, [3, 1, 2, 4, 2, 1, 5, 4, 3])),
                                list(map(str, [2, 4, 3, 1, 5, 4, 3, 1, 2])),
                                list(map(str, [3, 1, 2, 4, 2, 1, 2, 4, 3])),
                                list(map(str, [2, 4, 3, 1, 3, 5, 3, 1, 2])),
                                list(map(str, [1, 5, 2, 4, 2, 1, 2, 4, 3])),
                                list(map(str, [4, 3, 1, 3, 5, 4, 3, 5, 1])),
                                list(map(str, [1, 2, 4, 2, 1, 2, 1, 4, 3])),
                                list(map(str, [4, 5, 1, 3, 4, 5, 3, 2, 1])),
                                list(map(str, [3, 2, 4, 2, 1, 2, 1, 4, 3]))]

                # show a few fixed numbers at the beginning, eg:['0_4_2', '0_5_1']
                # use the fixed numbers from the project pdf
                fixedNumbers = ['0_4_2', '0_5_1', '1_2_3', '3_1_4', '3_4_3', '4_2_2', '5_4_5', '6_6_1', '7_3_3',
                                '7_5_5', '7_8_1', '8_0_3', '8_5_2']

    screen.fill(WHITE)
    screen.blit(imageWelcome, (200, 0))
    buttonPlay.draw(window=screen)
    buttonQuit.draw(window=screen)
    button3x3.draw(window=screen)
    button6x6.draw(window=screen)
    button9x9.draw(window=screen)
    display_text("choose a size", 370, 400, color=BLACK)

    # '''
    # define grid buttons, eg: button_0_1
    dictButtonGrids = {}
    # store the button of fixed numvers, eg: button_0_2
    dictButtonGridFixed = {}
    for i in range(side_size):
        for j in range(side_size):
            buttonName = '_'.join(['button', str(i), str(j)])
            # for every box except the fixed ones, make a button for it
            if '_'.join([str(i), str(j)]) not in ['_'.join(item.split('_')[:2]) for item in fixedNumbers]:
                dictButtonGrids[buttonName] = button(color=WHITE, x=gridPos[0] + j * cellSize,
                                                     y=gridPos[1] + i * cellSize, width=cellSize, height=cellSize)
            else:
                dictButtonGridFixed[buttonName] = button(color=GREEN, x=gridPos[0] + j * cellSize,
                                                         y=gridPos[1] + i * cellSize, width=cellSize, height=cellSize)

    # the matrix of solution provided by player
    matrixFromPlay = [[0 for i in range(side_size)] for j in range(side_size)]
    # load the fixed numbers
    for item in fixedNumbers:
        item = list(map(int, item.split('_')))
        matrixFromPlay[item[0]][item[1]] = item[2]
    # '''

    # go into the play page)
    cooChosen = None
    while stayInWelcomePage == False:

        # --- Main event loop
        for event in pygame.event.get():
            # get the position of mouse
            posMouse = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                done = True
                stayInWelcomePage = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.isMouseOverTheButton(posMouse):
                    # print('button 1 clicked')
                    button1.color = ORANGE
                    if cooChosen:
                        #buttonClicked.color = RED
                        key = '_'.join(map(str,[cooChosen[0],cooChosen[1]]))
                        dictNumFromPlayer[key] = '1'
                        matrixFromPlay[cooChosen[1]][cooChosen[0]] = 1
                else:
                    button1.color = LIGHT_GRAY
                if button2.isMouseOverTheButton(posMouse):
                    # print('button 2 clicked')
                    button2.color = ORANGE
                    if cooChosen:
                        key = '_'.join(map(str,[cooChosen[0],cooChosen[1]]))
                        dictNumFromPlayer[key] = '2'
                        matrixFromPlay[cooChosen[1]][cooChosen[0]] = 2
                else:
                    button2.color = LIGHT_GRAY
                if button3.isMouseOverTheButton(posMouse):
                    # print('button 3 clicked')
                    button3.color = ORANGE
                    if cooChosen:
                        key = '_'.join(map(str,[cooChosen[0],cooChosen[1]]))
                        dictNumFromPlayer[key] = '3'
                        matrixFromPlay[cooChosen[1]][cooChosen[0]] = 3
                else:
                    button3.color = LIGHT_GRAY
                if button4.isMouseOverTheButton(posMouse):
                    # print('button 4 clicked')
                    button4.color = ORANGE
                    if cooChosen:
                        key = '_'.join(map(str,[cooChosen[0],cooChosen[1]]))
                        dictNumFromPlayer[key] = '4'
                        matrixFromPlay[cooChosen[1]][cooChosen[0]] = 4
                else:
                    button4.color = LIGHT_GRAY
                if button5.isMouseOverTheButton(posMouse):
                    # print('button 5 clicked')
                    button5.color = ORANGE
                    if cooChosen:
                        key = '_'.join(map(str,[cooChosen[0],cooChosen[1]]))
                        dictNumFromPlayer[key] = '5'
                        matrixFromPlay[cooChosen[1]][cooChosen[0]] = 5
                else:
                    button5.color = LIGHT_GRAY

                # if you click on the "show solution" button
                if buttonShowSolution.isMouseOverTheButton(posMouse):
                    # print('buttonShowSolution clicked')
                    buttonShowSolution.color = ORANGE
                    flagShowSolution = True
                else:
                    buttonShowSolution.color = LIGHT_GRAY
                    flagShowSolution = False

                # if you click on the "reset" button
                if buttonReset.isMouseOverTheButton(posMouse):
                    buttonReset.color = ORANGE
                    flagReset = True
                else:
                    buttonReset.color = LIGHT_GRAY
                    flagReset = False

                # if you click on the "submit" button
                if buttonSubmit.isMouseOverTheButton(posMouse):
                    buttonSubmit.color = ORANGE
                    flagSubmit = True
                else:
                    buttonSubmit.color = YELLOW
                    flagSubmit = False

                # if you click on the "hint" button
                if buttonHint.isMouseOverTheButton(posMouse):
                    buttonHint.color = ORANGE
                    flagHint = True
                else:
                    buttonHint.color = LIGHT_GRAY

                if buttonNewGame.isMouseOverTheButton(posMouse):
                    buttonNewGame.color = ORANGE
                    flagNewGame = True
                    cooChosen = None
                    if side_size == 3:
                        # randomly update the grid
                        coordinatesList, matrixAnswer, fixedNumbers = cut_grid_into_shapes(side_size)
                    elif side_size == 6:
                        pass
                    elif side_size == 9:
                        pass
                    else:
                        raise Exception('unexpected side_size')
                    # when click New Game, reset the grid'
                    flagReset = True
                    flagShowSolution = False

                else:
                    flagNewGame = False
                    buttonNewGame.color = LIGHT_GRAY

                # if you click on the "return" button
                if buttonReturn.isMouseOverTheButton(posMouse):
                    stayInWelcomePage = True

                # mouse clicked in the grid boxes, identify which box is clicked
                if posMouse[0] >= 75 and posMouse[0] <= 525 and posMouse[1] >=75 and posMouse[1] <= 525:
                    # locate the box clicked
                    x_ = math.floor((posMouse[0]-75)/cellSize)
                    y_ = math.floor((posMouse[1]-75)/cellSize)
                    cooChosen = [x_, y_]
                    # here x and y must be in opposite position, as the defined axis and axis of pygame are opposite
                    if '_'.join(['button', str(y_), str(x_)]) in list(dictButtonGridFixed.keys()):
                        cooChosen = None
                    else:
                        # set the box clicked into LIGHT_BLUE color, and the rest in WHITE
                        buttonClicked = dictButtonGrids['_'.join(['button', str(y_), str(x_)])]
                        buttonClicked.color = LIGHT_BLUE
                        for item in dictButtonGrids.values():
                            if item != buttonClicked:
                                item.color = WHITE


        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # panel buttons
        button1.draw(window=screen)
        button2.draw(window=screen)
        button3.draw(window=screen)
        button4.draw(window=screen)
        button5.draw(window=screen)
        buttonShowSolution.draw(window=screen)
        buttonReset.draw(window=screen)
        buttonHint.draw(window=screen)
        buttonNewGame.draw(window=screen)
        buttonSubmit.draw(window=screen)
        buttonReturn.draw(window=screen)

        dictButtonGrids = {}
        # store the button of fixed numvers, eg: button_0_2
        dictButtonGridFixed = {}
        for i in range(side_size):
            for j in range(side_size):
                buttonName = '_'.join(['button', str(i), str(j)])
                # for every box except the fixed ones, make a button for it
                if '_'.join([str(i), str(j)]) not in ['_'.join(item.split('_')[:2]) for item in fixedNumbers]:
                    if cooChosen and '_'.join([str(i), str(j)])=='_'.join([str(cooChosen[1]), str(cooChosen[0])]):
                        dictButtonGrids[buttonName] = button(color=LIGHT_BLUE, x=gridPos[0] + j * cellSize,
                                                             y=gridPos[1] + i * cellSize, width=cellSize,
                                                             height=cellSize)
                    else:
                        dictButtonGrids[buttonName] = button(color=WHITE, x=gridPos[0] + j * cellSize,
                                                         y=gridPos[1] + i * cellSize, width=cellSize, height=cellSize)
                else:
                    dictButtonGridFixed[buttonName] = button(color=GREEN, x=gridPos[0] + j * cellSize,
                                                             y=gridPos[1] + i * cellSize, width=cellSize,
                                                             height=cellSize)


        # the matrix of solution provided by player
        # matrixFromPlay = [[0 for i in range(side_size)] for j in range(side_size)]
        # load the fixed numbers
        for item in fixedNumbers:
            item = list(map(int, item.split('_')))
            matrixFromPlay[item[0]][item[1]] = item[2]

        # grid buttons
        for bt in dictButtonGrids.values():
            bt.draw(window=screen)
        for bt in dictButtonGridFixed.values():
            bt.draw(window=screen)
        # button_0_0.draw(window=screen)
        # button_0_1.draw(window=screen)

        # draw a blank grid
        # draw a square
        pygame.draw.rect(screen, LIGHT_GRAY, (gridPos[0], gridPos[1], 450, 450), 2)
        # draw lines
        for x in range(side_size):
            # vertical lines
            pygame.draw.line(screen, LIGHT_GRAY, (gridPos[0] + (x * cellSize), gridPos[1]),
                             (gridPos[0] + (x * cellSize), gridPos[1] + 450))
            # horizontal lines
            pygame.draw.line(screen, LIGHT_GRAY, (gridPos[0], gridPos[1] + (x * cellSize)),
                             (gridPos[0] + 450, gridPos[1] + +(x * cellSize)))



        # coordinates = define_shapes(coordinate=[0,2], num_squares=5, num_serial=16)
        # draw_shapes(coordinates, codeSpecialCase='5_16')
        #'''
        # draw the shapes based on the coordinatesList
        for item in coordinatesList:
            item = item.split('_')
            coordinate = [int(item[0]),int(item[1])]
            numSquares = int(item[2])
            numSerial = int(item[3])
            codeSpecialCase = '_'.join([item[2],item[3]])
            coordinates = define_shapes(coordinate=coordinate, num_squares=numSquares, num_serial=numSerial)
            draw_shapes(coordinates, codeSpecialCase=codeSpecialCase)
        #'''

        # if the button "show solution" is clicked
        if flagShowSolution == True:
            # show the answers
            for i in range(side_size):
                for j in range(side_size):
                    matrixFromPlay[i][j] = int(matrixAnswer[i][j])

        # if the button "reset" is clicked
        if flagReset == True:
            # reset the matrixFromPlay
            matrixFromPlay = [[0 for i in range(side_size)] for j in range(side_size)]
            for item in fixedNumbers:
                item = list(map(int, item.split('_')))
                matrixFromPlay[item[0]][item[1]] = item[2]
            # update the dictNumFromPlayer, so that numbers get cleaned in the grid
            for item in dictNumFromPlayer:
                dictNumFromPlayer[item] = '0'
            flagReset = False
            # even if the button "show solution" is clicked, you can still reset
            flagShowSolution = False

        if flagSubmit == True:
            # compare with the standard answer
            isCorrect = compareMatrix(matrixAnswer, matrixFromPlay)
            print('matrixAnswer:')
            display_matrix(matrixAnswer)
            print('matrixFromPlay:')
            display_matrix(matrixFromPlay)
            if isCorrect == True:
                display_text('Bingo!', 270, 30, color=RED)
            else:
                display_text('Nope...', 270, 30, color=RED)

        # if you click on the "hint" button, randomly give a box with correct answer
        if flagHint == True:
            # randomly choose a box from matrixFromPlay, choose from those either not chosen or chosen wrong eg: button_0_1
            randomPool = []
            for ii in range(side_size):
                for jj in range(side_size):
                    if matrixFromPlay[ii][jj] == 0 or int(matrixFromPlay[ii][jj]) != int(matrixAnswer[ii][jj]):
                        randomPool.append([ii, jj])
            #print(randomPool)
            if randomPool:
                boxChosen = random.choice(randomPool)
                # update matrixFromPlay
                matrixFromPlay[boxChosen[0]][boxChosen[1]] = int(matrixAnswer[boxChosen[0]][boxChosen[1]])
            flagHint = False

        if flagNewGame == True:
            if side_size in [6, 9]:
                display_text('sorry, random new game is only available for 3x3 game', 100, 30, color=RED)

        # display the numbers according to the latest matrixFromPlay
        display_numbers(matrixFromPlay, gridPos, cellSize)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit
pygame.quit()
