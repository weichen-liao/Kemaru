# -*- coding: utf-8 -*-
# Author: Weichen Liao

from shapes import define_shapes, get_all_conditions, SHAPE_LONG
import random
import numpy
import time
import signal
import copy
import math
import datetime

TIMEOUT = 2   # in second


# display the matrix
def display_matrix(matrix):
    for item in matrix:
        print(' '.join(map(str, item)))

# get to see how many coordinates left unused
def get_coor_number(matrix):
    total = 0
    for item in matrix:
        total += len(item)
    return total

# check if put the shape at pos is legal or not
def is_legal(matrix, shapeChosen, matrixAnswer, numberAssign):
    # check if the shape itself is ok
    for coo in shapeChosen:
        try:
            if coo not in matrix[coo[0]]:
                return False
        except:
            return False

    # check the assignment of numbers:
    try:
        for ii, item in enumerate(shapeChosen):
            x_, y_ = item[0], item[1]
            matrixAnswer[x_][y_] = str(numberAssign[ii])

        ss = len(matrixAnswer)
        for ii in range(ss):
            for jj in range(ss):
                if matrixAnswer[ii][jj] != '0':
                    aroundCoo = [[max(ii-1,0),jj], [max(ii-1,0), min(jj+1,ss-1)], [ii, min(jj+1,ss-1)], [min(ii+1,ss-1), min(jj+1,ss-1)], [min(ii+1,ss-1), jj], [min(ii+1,ss-1), max(jj-1,0)], [ii, max(jj-1,0)], [max(ii-1,0), max(jj-1,0)]]
                    aroundCoo = [item for item in aroundCoo if item != [ii,jj]]
                    if matrixAnswer[ii][jj] in [matrixAnswer[item[0]][item[1]] for item in aroundCoo]:
                        # recover the matrixAnswer, or it will be serious problem,
                        for ii, item in enumerate(shapeChosen):
                            x_, y_ = item[0], item[1]
                            matrixAnswer[x_][y_] = '0'
                        return False

        # isolation check: many times a shape has cut 0 box into isolation, check this and it saves a lot of computation


        # here is alreay legal, but we must recover the matrixAnswer, or it will be serious problem,
        for ii, item in enumerate(shapeChosen):
            x_, y_ = item[0], item[1]
            matrixAnswer[x_][y_] = '0'
    except:
        raise Exception('is_assign_legal error')


    return True

# remove coordinates from the matrix
def take_places(matrix, shapeChosen):
    for coo in shapeChosen:
        matrix[coo[0]].remove(coo)
    return matrix

def recover(matrix, shapeChosen):
    for coo in shapeChosen:
        # the order seems doesnt matter
        matrix[coo[0]].append(coo)
    return matrix


def random_cut_recursive(matrix, matrixAnswer, coordinatesList, sideSize, startTime):
    # given a postion, get its neighboring shapes from the existing coordinatesList
    def get_neighbor_shapes(pos, coordinatesList):
        # cal the distance between 2 coordinate, eg: [0,1] and [1,1]: dis=1
        def cal_distance(cooA, cooB):
            dis = math.sqrt((cooA[0]-cooB[0])**2 + (cooA[1]-cooB[1])**2)
            return dis
        res = []
        if coordinatesList == []:
            return []
        for item in coordinatesList:
            p_x, p_y, nSq, nSe = map(int, item.split('_'))
            thisShape = define_shapes([p_x, p_y], nSq, nSe)
            for coo in thisShape:
                if cal_distance(coo, pos) <= 1:
                    res.append(item)
                    break
        return res

    #print('------------------------------------------------------------------------------------')
    #if all the grid is filled, the recursive progress ends
    if get_coor_number(matrix) == 0:
        return True

    # a list of all the possible combination of num_squares and num_serial and assignments, eg['2_1|1_2']
    allConditions = get_all_conditions()

    # these number of Squares is no more available for this position
    badNumSquares = []

    for i in range(sideSize):
        if matrix[i]:
            pos = matrix[i][0]
            break

    # find the neighboring shapes from the existing coordinatesList
    neighborShapes = get_neighbor_shapes(pos, coordinatesList)
    neighborShapes = ['_'.join(item.split('_')[2:]) for item in neighborShapes if item]

    # a counter to record the loop
    loopCounter = 0
    while True:
        now = datetime.datetime.now()
        if (now - startTime).seconds >= TIMEOUT:
            return 'timeOut'
        # if no shape is possible to satisfy the current condition, go back to the last iteration
        if allConditions == []:
            return False
        loopCounter += 1
        # randomly choose the shape
        choiceForNumSquare = [item for item in [2,3,4,5] if item not in badNumSquares]
        if choiceForNumSquare == []:
            return False
        try:
            if get_coor_number(matrix) > 6:
                numSquares = numpy.random.choice(choiceForNumSquare)
                # numSquares = numpy.random.choice([2, 3, 4, 5], p=[0.1, 0.1, 0.4, 0.4])
                # numSquares = numpy.random.choice([2, 3, 4, 5], p=[0, 0, 0, 1.0])
            elif get_coor_number(matrix) == 6:
                choiceForNumSquare = [item for item in choiceForNumSquare if item != 5]
                numSquares = numpy.random.choice(choiceForNumSquare)
                # numSquares = numpy.random.choice([2, 3, 4], p=[0.3, 0.3, 0.4])
            elif get_coor_number(matrix) == 5:
                choiceForNumSquare = [item for item in choiceForNumSquare if item != 4]
                numSquares = numpy.random.choice(choiceForNumSquare)
                # numSquares = numpy.random.choice([2, 3, 5], p=[0.3, 0.3, 0.4])
                # numSquares = numpy.random.choice([2, 3, 5], p=[0.3, 0.7, 0])
            elif get_coor_number(matrix) == 4:
                choiceForNumSquare = [item for item in choiceForNumSquare if item not in [3, 5]]
                numSquares = numpy.random.choice(choiceForNumSquare)
                # numSquares = random.choice([4, 2])
            elif get_coor_number(matrix) == 3:
                choiceForNumSquare = [item for item in choiceForNumSquare if item not in [2, 4, 5]]
                numSquares = numpy.random.choice(choiceForNumSquare)
                # numSquares = 3
            elif get_coor_number(matrix) == 2:
                choiceForNumSquare = [item for item in choiceForNumSquare if item not in [3, 4, 5]]
                numSquares = numpy.random.choice(choiceForNumSquare)
                # numSquares = 2
            elif get_coor_number(matrix) == 0:
                return True
            else:
                raise Exception('unexpected error: ', get_coor_number(matrix))
        except:
            print('choiceForNumSquare is empty, return False')
            return False

        # '2_1|1_2' -> shape|permutations
        randomPool = [item for item in allConditions if item[0] == str(numSquares)]

        # '''
        # if the current position has a existing neighbor in long shapes, then it'd better avoid choosing another long shape
        for item in neighborShapes:
            if item in SHAPE_LONG:
                randomPool = [s for s in randomPool if s not in SHAPE_LONG]
                break
        # '''
        # '''
        # further reduce the scale of randomPool, based on the existing matrixAnswer
        # get the surrounding coordinates of pos
        aroundCoo = [[max(pos[0] - 1, 0), pos[1]], [max(pos[0] - 1, 0), min(pos[1] + 1, sideSize - 1)], [pos[0], min(pos[1] + 1, sideSize - 1)],
                     [min(pos[0] + 1, sideSize - 1), min(pos[1] + 1, sideSize - 1)], [min(pos[0] + 1, sideSize - 1), pos[1]],
                     [min(pos[0] + 1, sideSize - 1), max(pos[1] - 1, 0)], [pos[0], max(pos[1] - 1, 0)], [max(pos[0] - 1, 0), max(pos[1] - 1, 0)]]
        # get the surounding numbers
        existingSuround = []
        for item in aroundCoo:
            if matrixAnswer[item[0]][item[1]] != '0':
                existingSuround.append(matrixAnswer[item[0]][item[1]])
        existingSuround = list(set(existingSuround))
        # exclude those numbers from the choice of randomPool, '2_1|1_2' -> shape|permutations
        randomPool = [item for item in randomPool if item.split('|')[1].split('_')[0] not in existingSuround]
        # '''

        if allConditions == []:
            return False

        if randomPool == []:
            badNumSquares.append(numSquares)
            badNumSquares = list(set(badNumSquares))
            # the numSquares is running into a dead end, must jump out of the loop
            # if len(selectedNumSquares) >= 30 and len(set(selectedNumSquares)) <= 3:
            #     return False
            # return False
            # try to choose another numSquares
            continue
        itemChosen = random.choice(randomPool)
        numSerial = int(itemChosen.split('|')[0].split('_')[1])
        numberAssign = itemChosen.split('|')[1].split('_')

        shapeChosen = define_shapes(coordinate=pos,num_squares=numSquares,num_serial=numSerial)


        # check if put the shape&assign at pos is legal or not
        # print('matrixAnswer before ilegal check:')
        # display_matrix(matrixAnswer)
        isLegal = is_legal(matrix, shapeChosen, matrixAnswer, numberAssign)
        # print('matrixAnswer after ilegal check:')
        # display_matrix(matrixAnswer)
        # print('pos: ', pos)
        # print('coordinatesList:',coordinatesList)
        # print('itemChosen:' ,itemChosen)
        # print('isLegal:', isLegal)
        #time.sleep(1)
        if isLegal == False:
            # print('------------ilegal check-----------')
            # print('pos: ',pos)
            # print('coordinatesList:',coordinatesList)
            # display_matrix(matrixAnswer)
            # print('itemChosen:' ,itemChosen)
            allConditions.remove(itemChosen)

        if isLegal == True:
            # if puting here is legal, do the following steps
            # put it here and update matrix
            matrix = take_places(matrix, shapeChosen)

            #coordinatesList.append(shapeChosen)
            coordinatesList.append('_'.join([str(pos[0]),str(pos[1]),str(numSquares),str(numSerial)]))
            # record the index of this element
            curLength = len(coordinatesList)-1

            # update the matrixAnswer
            for ii, item in enumerate(shapeChosen):
                x_, y_ = item[0], item[1]
                matrixAnswer[x_][y_] = str(numberAssign[ii])

            if get_coor_number(matrix) == 0:
                return True

            # enter the next iteration
            res = random_cut_recursive(matrix, matrixAnswer, coordinatesList, sideSize, startTime)
            if res == True:
                return True
            elif res == 'timeOut':
                return 'timeOut'
            else:
                #print('##############     bad choice, re choose in this iteration       ###################')
                # remove it from the random pool
                allConditions.remove(itemChosen)
                # recover the matrix and coordinatesList:
                matrix = recover(matrix, shapeChosen)
                coordinatesList.pop(curLength)
                #display_matrix(matrix)
                #print(get_coor_number(matrix))

                # recover the matrixAnswer also
                for ii, item in enumerate(shapeChosen):
                    x_, y_ = item[0], item[1]
                    matrixAnswer[x_][y_] = '0'


# def signal_handler(signum, frame):
#     raise Exception("Timed out!")
#
# while True:
#     signal.signal(signal.SIGALRM, signal_handler)
#     signal.alarm(2)   # two seconds
#     try:
#         random_cut_recursive(matrixCoordinates)
#         break
#     except:
#         print ("Timed out! restart")

def cut_grid_into_shapes(sideSize):
    tryCounter = 0
    # this is a time out mechanism. in occasions, creating a random game takes too much time which is a , if time out, restart the process
    zeroTime = datetime.datetime.now()
    while True:
        tryCounter += 1
        matrixCoordinates = [[] for i in range(sideSize)]
        for i in range(sideSize):
            for j in range(sideSize):
                matrixCoordinates[i].append([i, j])


        matrixAnswer = [['0' for i in range(sideSize)] for j in range(sideSize)]
        # this is supposed to store the coordinate combinations regarding to the shapes. eg:[[[0,0],[0,1],[1,1]], [[1,1],[2,1],[3,1]]]
        coordinatesList = []

        # '''
        # initialize matrixAnswer, cut the possibilities for the first choice, so that the total possibilities are greatly reduces.
        initialChoice = random.choice([1,2,3,4,5])
        if initialChoice == 1:
            matrixAnswer[0][0] = '4'
            matrixAnswer[0][1] = '1'
            matrixAnswer[1][0] = '2'
            matrixAnswer[1][1] = '5'
            matrixAnswer[2][0] = '3'
            coordinatesList = ['0_0_5_11']
            matrixCoordinates[0].remove([0, 0])
            matrixCoordinates[0].remove([0, 1])
            matrixCoordinates[1].remove([1, 0])
            matrixCoordinates[1].remove([1, 1])
            matrixCoordinates[2].remove([2, 0])
        elif initialChoice == 2:
            matrixAnswer[0][0] = '1'
            matrixAnswer[0][1] = '2'
            coordinatesList = ['0_0_2_2']
            matrixCoordinates[0].remove([0, 0])
            matrixCoordinates[0].remove([0, 1])
        elif initialChoice == 3:
            matrixAnswer[0][0] = '4'
            matrixAnswer[0][1] = '1'
            matrixAnswer[0][2] = '3'
            matrixAnswer[1][0] = '2'
            matrixAnswer[1][1] = '5'
            coordinatesList = ['0_0_5_18']
            matrixCoordinates[0].remove([0, 0])
            matrixCoordinates[0].remove([0, 1])
            matrixCoordinates[0].remove([0, 2])
            matrixCoordinates[1].remove([1, 0])
            matrixCoordinates[1].remove([1, 1])
        elif initialChoice == 4:
            matrixAnswer[0][0] = '4'
            matrixAnswer[0][1] = '3'
            matrixAnswer[0][2] = '2'
            matrixAnswer[1][2] = '1'
            coordinatesList = ['0_0_4_4']
            matrixCoordinates[0].remove([0, 0])
            matrixCoordinates[0].remove([0, 1])
            matrixCoordinates[0].remove([0, 2])
            matrixCoordinates[1].remove([1, 2])
        else:
            matrixAnswer[0][0] = '2'
            matrixAnswer[0][1] = '3'
            matrixAnswer[0][2] = '1'
            matrixAnswer[1][1] = '4'
            coordinatesList = ['0_0_4_17']
            matrixCoordinates[0].remove([0, 0])
            matrixCoordinates[0].remove([0, 1])
            matrixCoordinates[0].remove([0, 2])
            matrixCoordinates[1].remove([1, 1])
        # '''

        startTime = datetime.datetime.now()
        res = random_cut_recursive(matrixCoordinates, matrixAnswer, coordinatesList, sideSize, startTime)
        now = datetime.datetime.now()
        print('-----------------------single process time cost:', (now-startTime).seconds)
        if res == 'timeOut':
            print('time out!!!, remaking the grid')
            continue
        if len(coordinatesList) <= 1:
            continue

        break
    now = datetime.datetime.now()
    print('tryCounter:',tryCounter, ' total time cost: ',(now - zeroTime).seconds)

    # get the fixedNumbers also, format:['0_4_2', '0_5_1']
    fixedNumbers = []
    # get 2 different coordinates
    cooChosen = random.sample(coordinatesList,2)
    for item in cooChosen:
        item = item.split('_')
        x_, y_ = item[0], item[1]
        fixedNumbers.append('_'.join([x_, y_, matrixAnswer[int(x_)][int(y_)]]))

    return coordinatesList, matrixAnswer, fixedNumbers


# coordinatesList = cut_grid_into_shapes(sideSize=9)
#
# print('end!')
# print('coordinatesList:',coordinatesList)
# print(sum([int(item.split('_')[2]) for item in coordinatesList]))







