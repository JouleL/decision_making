#!/usr/bin/python

import sys
import re
import string
from prettytable import PrettyTable
from simplex_method import Simplex

def open_file():
    try:
        return open("yatsynych.txt")
    except FileNotFoundError:
        print("Error: no such file")
        exit()


def get_matrix_table(matrix):
    if len(matrix) < 1: return ''

    x = PrettyTable()
    fields = ['']
    for i in range(len(matrix[0])):
        fields.append("B" + str(i + 1))

    x.field_names = fields
    for i in range(len(matrix)):
        x.add_row(['A' + str(i + 1)] + matrix[i])
    return x


def check_saddle_point(minA, maxB):
    maxFromMatrixA = minA[max(minA, key = minA.get)]
    minFromMatrixB = maxB[min(maxB, key = maxB.get)]
    return [maxFromMatrixA, minFromMatrixB]


def check_rows(firstRow, secondRow):
    equalElements = 0
    for i in range(len(firstRow)):
        if firstRow[i] < secondRow[i]: return 0
        if firstRow[i] == secondRow[i]: equalElements += equalElements

    return 0 if equalElements == len(firstRow) else 1


def check_dominant_rows(matrix):
    matrixAfterExcludingRows = []
    deletedRows = []

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j: continue
            result = check_rows(matrix[i], matrix[j])
            if result != 0 and j not in deletedRows:
                deletedRows.append(j)
                print("Strategy А" + str(i + 1), " is dominant over strategy А" + str(j + 1), "so the chosen row is ", j + 1)

    for i in range(len(matrix)):
        if i in deletedRows: continue
        matrixAfterExcludingRows.append(matrix[i])

    return matrixAfterExcludingRows


def check_dominant_columns(matrix):
    matrixAfterExcludingColumns = []
    deletedColumns = []
    transposedMatrix = [list(x) for x in zip(*matrix)]

    for i in range(len(transposedMatrix)):
        for j in range(len(transposedMatrix)):
            if i == j: continue
            result = check_rows(transposedMatrix[j], transposedMatrix[i])
            if result != 0 and j not in deletedColumns:
                deletedColumns.append(j)
                print("Strategy В" + str(i + 1), "is dominant over strategy В" + str(j + 1), "so the chosen column is", j + 1)
    
    for i in range(len(matrix)):
        matrixAfterExcludingColumns.append([])
        for j in range(len(matrix[i])):
            if j in deletedColumns: continue
            matrixAfterExcludingColumns[i].append(matrix[i][j])

    return matrixAfterExcludingColumns


file = open_file()

matrix = []
for line in file:
    matrix.append([int(d) for d in re.split(';', re.sub('\n', '', line))])

if len(matrix) < 2: exit()
print("Data")
print(get_matrix_table(matrix))

print("Checking the existence of saddle point")
x = PrettyTable()
fields = ['']
for i in range(len(matrix)):
    fields.append("B" + str(i + 1))

fields.append('a = min(Ai)')
x.field_names = fields

minA = {}
maxB = {}

for i in range(len(matrix)):
    minA[i] = min(matrix[i])
    x.add_row(['A' + str(i + 1)] + matrix[i] + [str(minA[i])])
    for j in range(len(matrix[i])):
        if j not in maxB or maxB[j] < matrix[i][j]:
            maxB[j] = matrix[i][j]

x.add_row(['b = max(Bi)'] + [maxB[element] for element in maxB] + [''])
print(x)

[maxFromMatrixA, minFromMatrixB] = check_saddle_point(minA, maxB)
if maxFromMatrixA == minFromMatrixB:
    print("Saddle point exists")
else:
    print("a = max(min(Ai)) =", maxFromMatrixA)
    print("b = min(max(Bi)) =", minFromMatrixB)
    print("Saddle point is abcent, because a != b")
    print("The price of the game is situated in such boundaries:", maxFromMatrixA, "<= y <=", minFromMatrixB)


print("\nChecking the matrix on dominant rows and columns:")
print("From the standpoint of winning player A")
matrixAfterExcludingRows = check_dominant_rows(matrix)
print("After checking dominant rows, the matrix looks like this: ")
print(get_matrix_table(matrixAfterExcludingRows))


print("From the standpoint of winning player В")
matrixAfterExcludingColumns = check_dominant_columns(matrixAfterExcludingRows)
print("After checking dominant columns, the matrix looks like this: ")
print(get_matrix_table(matrixAfterExcludingColumns))

transposedMatrix = [list(x) for x in zip(*matrixAfterExcludingColumns)]
print("\nLet's find solutions to the game in mixed strategies")
print("Find the minimum of the func F(x) under constraints (for player B)")

secondPlayersConditions = []
for i in range(len(transposedMatrix)):
    secondPlayersConditions.append('')
    for j in range(len(transposedMatrix[i])):
        secondPlayersConditions[i] += str(transposedMatrix[i][j]) + 'x_' + str(j + 1) + ' + '

for i in range(len(secondPlayersConditions)):
    print(secondPlayersConditions[i][:-2] + '>= 1')

mainCondition = 'F(x) = '
for i in range(len(matrixAfterExcludingColumns)):
    mainCondition += 'x_' + str(i + 1) + ' + '

print(mainCondition[:-2] + '--> min')

print("Find the minimum of the func Z(y) under constraints (for player A)")
firstPlayersConditions = []

vars_count = 0
for i in range(len(matrixAfterExcludingColumns)):
    firstPlayersConditions.append('')
    columns = len(matrixAfterExcludingColumns[i])
    for j in range(columns):
        firstPlayersConditions[i] += str(matrixAfterExcludingColumns[i][j]) + 'y_' + str(j + 1) + ' + '
        if columns > vars_count:
            vars_count = columns

conditions = ''
for i in range(len(firstPlayersConditions)):
    firstPlayersConditions[i] = firstPlayersConditions[i][:-2] + '<= 1'

mainCondition = ''
for i in range(len(transposedMatrix)):
    mainCondition += '1y_' + str(i + 1) + ' + '

mainCondition = mainCondition[:-2]

for line in firstPlayersConditions:print(line)
print('Z(y) = ' + mainCondition + '--> max')

print("\nSolution to the problem of linear programming with the simplex method")
print("Let's find the maximum of the target function", mainCondition + '--> max', "under the next conditions-restrictions:")
print(conditions)
print("After conversion to the canonical form, let's move on to the basic simplex method algorithm")

simplexResult = Simplex(num_vars=vars_count, constraints=firstPlayersConditions, objective_function=mainCondition)
print("\nWe get the next results:")

x_result = {}
y_result = {}
for key in simplexResult.solution:
    if 'y_' in key:
        y_result[key] = simplexResult.solution[key]
    elif 'x_' in key:
        x_result[key] = simplexResult.solution[key]

yResultCond = 'F(y) = '
yResult = 0
for i in range(vars_count):
    print('y' + str(i + 1) + ' =', y_result['y_' + str(i + 1)], end=' ')
    yResult += 1 * y_result['y_' + str(i + 1)]
    yResultCond += "1 * " + str(y_result['y_' + str(i + 1)]) + ' + '


print("\n" + yResultCond[:-2] + '= ' + str(yResult), '\n')

xResultCond = 'F(x) = '
xResult = 0
for i in range(vars_count):
    print('x' + str(i + 1) + ' =', x_result['x_' + str(i + 1)], end=' ')
    xResult += 1 * x_result['x_' + str(i + 1)]
    xResultCond += "1 * " + str(x_result['x_' + str(i + 1)]) + ' + '


print("\n" + xResultCond[:-2] + '= ' + str(xResult))

print("\nPrice of the game equals g = 1/F(x)")
print( "g = 1/(" + str(xResult), ") =", str(1/xResult))
