# -*- coding: utf-8 -*-
# Author: Weichen Liao
import itertools

# here we will define 70 possible shapes
# the first argument is the Coordinates of the upper left corner square, it means this shape will be put here, eg:[0,0]
def define_shapes(coordinate, num_squares, num_serial):
    res = []
    # for this case, there are only 2 possible shapes
    x_axis, y_axis= coordinate[0], coordinate[1]
    if num_squares == 2:
        # *
        # *
        if num_serial == 1:
            res = [[x_axis, y_axis],[x_axis+1, y_axis]]
        # **
        elif num_serial == 2:
            res = [[x_axis, y_axis], [x_axis, y_axis+1]]
        else:
            raise Exception("Sorry, the num_serial limited to 1 to 2  ",num_serial)
    # for this case, there are 6 possible shapes
    elif num_squares == 3:
        # ***
        if num_serial == 1:
            res = [[x_axis, y_axis],[x_axis, y_axis+1],[x_axis, y_axis+2]]
        # *
        # *
        # *
        elif num_serial == 2:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis]]
        # **
        # *
        elif num_serial == 3:
            res = [[x_axis, y_axis+1], [x_axis, y_axis], [x_axis+1, y_axis]]
        # **
        #  *
        elif num_serial == 4:
            res = [[x_axis, y_axis],[x_axis, y_axis+1],[x_axis+1, y_axis+1]]
        #  *
        # **
        elif num_serial == 5:
            res = [[x_axis, y_axis],[x_axis+1, y_axis],[x_axis+1, y_axis-1]]
        # *
        # **
        elif num_serial == 6:
            res = [[x_axis, y_axis],[x_axis+1, y_axis],[x_axis+1, y_axis+1]]
        else:
            raise Exception("Sorry, the num_serial limited to 1 to 6  ",num_serial)
    # for this case, there are 19 possible shapes
    elif num_squares == 4:
        # ****
        if num_serial == 1:
            res = [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis, y_axis+2], [x_axis, y_axis+3]]
        # *
        # *
        # *
        # *
        elif num_serial == 2:
            res = [[x_axis, y_axis],[x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+3, y_axis]]
        # **
        # *
        # *
        elif num_serial == 3:
            res = [[x_axis, y_axis+1], [x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis]]
        # ***
        #   *
        elif num_serial == 4:
            res = [[x_axis, y_axis],[x_axis, y_axis+1], [x_axis, y_axis+2], [x_axis+1, y_axis+2]]
        #  *
        #  *
        # **
        elif num_serial == 5:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+2, y_axis-1]]
        # *
        # ***
        elif num_serial == 6:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis+1], [x_axis+1, y_axis+2]]
        # **
        #  *
        #  *
        elif num_serial == 7:
            res = [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis+1, y_axis+1], [x_axis+2, y_axis+1]]
        # ***
        # *
        elif num_serial == 8:
            res = [[x_axis+1, y_axis], [x_axis, y_axis], [x_axis, y_axis+1], [x_axis, y_axis+2]]
        # *
        # *
        # **
        elif num_serial == 9:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+2, y_axis+1]]
        #   *
        # ***
        elif num_serial == 10:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis-1], [x_axis+1, y_axis-2]]
        # **
        # **
        elif num_serial == 11:
            res = [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis+1, y_axis], [x_axis+1, y_axis+1]]
        # *
        # **
        #  *
        elif num_serial == 12:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis+1], [x_axis+2, y_axis+1]]
        #  **
        # **
        elif num_serial == 13:
            res = [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis-1, y_axis+1], [x_axis-1, y_axis+2]]
        #  *
        # **
        # *
        elif num_serial == 14:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis-1], [x_axis+2, y_axis-1]]
        # **
        #  **
        elif num_serial == 15:
            res = [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis+1, y_axis+1], [x_axis+1, y_axis+2]]
        # *
        # **
        # *
        elif num_serial == 16:
            res = [[x_axis, y_axis], [x_axis+1, y_axis],[x_axis+2, y_axis],[x_axis+1, y_axis+1]]
        # ***
        #  *
        elif num_serial == 17:
            res = [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis, y_axis+2], [x_axis+1, y_axis+1]]
        #  *
        # **
        #  *
        elif num_serial == 18:
            res = [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+1, y_axis-1]]
        #  *
        # ***
        elif num_serial == 19:
            res = [[x_axis, y_axis], [x_axis+1, y_axis-1],[x_axis+1, y_axis],[x_axis+1, y_axis+1]]

        else:
            raise Exception("Sorry, the num_serial limited to 1 to 19  ",num_serial)
    # for this case, there are 19 possible shapes
    elif num_squares == 5:
        # *****
        if num_serial == 1:
            return [[x_axis, y_axis],[x_axis, y_axis+1],[x_axis, y_axis+2],[x_axis, y_axis+3],[x_axis, y_axis+4]]
        # *
        # *
        # *
        # *
        # *
        elif num_serial == 2:
            return [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+3, y_axis], [x_axis+4, y_axis]]
        # **
        # *
        # *
        # *
        elif num_serial == 3:
            return [[x_axis, y_axis+1],[x_axis, y_axis],[x_axis+1, y_axis],[x_axis+2, y_axis],[x_axis+3, y_axis]]
        # ****
        #    *
        elif num_serial == 4:
            return [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis, y_axis+2], [x_axis, y_axis+3], [x_axis+1, y_axis+3]]
        #  *
        #  *
        #  *
        # **
        elif num_serial == 5:
            return [[x_axis, y_axis], [x_axis+1, y_axis],[x_axis+2, y_axis],[x_axis+3, y_axis], [x_axis+3, y_axis-1]]
        # *
        # ****
        elif num_serial == 6:
            return [[x_axis, y_axis], [x_axis+1, y_axis],[x_axis+1, y_axis+1], [x_axis+1, y_axis+2], [x_axis+1, y_axis+3]]
        # **
        #  *
        #  *
        #  *
        elif num_serial == 7:
            return [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis+1, y_axis+1], [x_axis+2, y_axis+1], [x_axis+3, y_axis+1]]
        #    *
        # ****
        elif num_serial == 8:
            return [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis-1], [x_axis+1, y_axis-2], [x_axis+1, y_axis-3]]
        # *
        # *
        # *
        # **
        elif num_serial == 9:
            return [[x_axis, y_axis],[x_axis+1, y_axis],[x_axis+2, y_axis],[x_axis+3, y_axis],[x_axis+3, y_axis+1]]
        # ****
        # *
        elif num_serial == 10:
            return [[x_axis+1, y_axis], [x_axis, y_axis], [x_axis, y_axis+1], [x_axis, y_axis+2], [x_axis, y_axis+3]]
        # **
        # **
        # *
        elif num_serial == 11:
            return [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis+1, y_axis+1], [x_axis+1, y_axis], [x_axis+2, y_axis]]
        # ***
        #  **
        elif num_serial == 12:
            return [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis, y_axis+2], [x_axis+1, y_axis+2], [x_axis+1, y_axis+1]]
        #  *
        # **
        # **
        elif num_serial == 13:
            return [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+2, y_axis-1], [x_axis+1, y_axis-1]]
        # **
        # ***
        elif num_serial == 14:
            return [[x_axis, y_axis], [x_axis, y_axis+1], [x_axis+1, y_axis+1], [x_axis+1, y_axis], [x_axis+1, y_axis+2]]
        # **
        # **
        #  *
        elif num_serial == 15:
            return [[x_axis, y_axis],[x_axis, y_axis+1], [x_axis+1, y_axis+1], [x_axis+2, y_axis+1], [x_axis+1, y_axis]]
        #  **
        # ***
        elif num_serial == 16:
            return [[x_axis, y_axis],[x_axis, y_axis+1],[x_axis+1, y_axis+1],[x_axis+1, y_axis], [x_axis+1, y_axis-1]]
        # *
        # **
        # **
        elif num_serial == 17:
            return [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+2, y_axis], [x_axis+2, y_axis+1], [x_axis+1, y_axis+1]]
        # ***
        # **
        elif num_serial == 18:
            return [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis+1], [x_axis, y_axis+1], [x_axis, y_axis+2]]
        #   *
        # ***
        # *
        elif num_serial == 19:
            return [[x_axis, y_axis], [x_axis+1, y_axis], [x_axis+1, y_axis-1], [x_axis+1, y_axis-2], [x_axis+2, y_axis-2]]
        else:
            raise Exception("Sorry, the num_serial limited to 1 to 19  ",num_serial)

    else:
        raise Exception("Sorry, the num_squares limited to 2 to 5  ",num_squares)

    return res

# '''
# return a list of all the possible combination of num_squares and num_serial, and assignment of numbers
# eg: ['2_2|1_2', '2_2|2_1'], which means all the permutations of shape 2_2
def get_all_conditions():
    res = []
    for i in range(1,3):
        shape = '_'.join(['2', str(i)])
        # eg: [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
        permutations = list(itertools.permutations(['1', '2']))
        # eg:['1_2_3', '1_3_2', '2_1_3', '2_3_1', '3_1_2', '3_2_1']
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape,item]))
    for i in range(1,7):
        shape = '_'.join(['3', str(i)])
        permutations = list(itertools.permutations(['1', '2', '3']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape, item]))
    for i in range(1,20):
        shape = '_'.join(['4', str(i)])
        permutations = list(itertools.permutations(['1', '2', '3', '4']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape, item]))
    for i in range(1,20):
        shape = '_'.join(['5', str(i)])
        permutations = list(itertools.permutations(['1', '2', '3', '4', '5']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape, item]))
    return res
# '''

'''
def get_all_conditions():
    res = []
    for i in range(1,3):
        shape = '_'.join(['2', str(i)])
        permutations = list(itertools.permutations(['1', '2']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape,item]))
    for i in range(1,7):
        shape = '_'.join(['3', str(i)])
        permutations = list(itertools.permutations(['1', '2', '3']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape, item]))
    for i in [1, 2, 4, 8, 11, 15, 18]:
        shape = '_'.join(['4', str(i)])
        permutations = list(itertools.permutations(['1', '2', '3', '4']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape, item]))
    for i in [1, 2, 4, 7, 11, 12, 13, 17]:
        shape = '_'.join(['5', str(i)])
        permutations = list(itertools.permutations(['1', '2', '3', '4', '5']))
        permutations = ['_'.join(item) for item in permutations]
        for item in permutations:
            res.append('|'.join([shape, item]))
    return res
'''

# shapes in long long long shape
SHAPE_LONG = ['3_1', '3_2',
              '4_1', '4_2', '4_3', '4_4', '4_5', '4_6', '4_7', '4_8', '4_9', '4_10',
              '5_1', '5_2', '5_3', '5_4', '5_5', '5_6', '5_7', '5_8', '5_9', '5_10']



# 2776 oh my fucking god!
print(len(get_all_conditions()))
print('2: ',len([item for item in get_all_conditions() if item[0]=='2']))   #4
print('3: ',len([item for item in get_all_conditions() if item[0]=='3']))   #36
print('4: ',len([item for item in get_all_conditions() if item[0]=='4']))   #456
print('5: ',len([item for item in get_all_conditions() if item[0]=='5']))   #2280