#!/usr/bin/python

import re

def open_file():
    try:
        return open("yatsynych.txt")
    except FileNotFoundError:
        print("Error, no such file!")
        exit()


def set_max_object_length(parameters, objects, maxWidths):
    for parameter in parameters:
        for obj in objects:
            objParamLength = len(str(parameters[parameter][obj]))
            if obj not in maxWidths:
                maxWidths[obj] = len(obj)
            if objParamLength > maxWidths[obj]:
                maxWidths[obj] = objParamLength
    

def draw_header(objects, maxWidths, getStartLength = False):
    return_str = ''
    numberPart = '|' + ('%' + str(maxWidths['NUMBER']) + 's') % "№|"
    parameterPart = ('%' + str(maxWidths['PARAMETER']) + 's') % "Параметр"
    coefficientPart = ('%' + str(maxWidths['COEFFICIENT']) + 's') % "Коефіцієнт"
    objectsPart = ''

    if getStartLength == True: return len(numberPart + parameterPart + '|' + coefficientPart + '|')

    for obj in objects:
        objectsPart += ('%' + str(maxWidths[obj]) + 's') % str(obj)
        objectsPart += '|'

    return numberPart + parameterPart + '|' + coefficientPart + '|' + objectsPart
   


def draw_parameters(parameters, objects, maxWidths):
    return_str = ''
    count = 1

    for parameter in parameters:
        numberPart =  ('%' + str(maxWidths['NUMBER']) + 's') % (str(count) + "|")
        parameterPart = ('%' + str(maxWidths['PARAMETER']) + 's') % parameter
        coefficientPart = ('%' + str(maxWidths['COEFFICIENT']) + 's') % parameters[parameter]['COEFFICIENT']
        objectsPart = ''

        for obj in objects:
            objectsPart += ('%' + str(maxWidths[obj]) + 's') % str(parameters[parameter][obj])
            objectsPart += '|'

        return_str += numberPart + parameterPart + '|' + coefficientPart + '|' + objectsPart + '\n'
        count += 1

    return return_str

def print_result (header, parameters):
    header_line = ''

    for i in range(len(header)):
        header_line += '='

    print(header_line)
    print(header)
    print(header_line)
    print(parameters)
    print(header_line)


def print_total (header, objects, parameters, maxWidths):
    header_line = ''
    for i in range(len(header)):
        header_line += '='

    total = draw_header(objects, maxWidths, True)
    totalPart = '|' + ('%' + str(total - 1) + 's') % ('Сума значень параметрів:' + "|")
    objTotal = {}
    for obj in objects:
        objSum = 0
        for param in parameters:
            objSum += parameters[param][obj]

        objTotal[obj] = objSum
  
    maxValue = max(objTotal, key=objTotal.get)
    for obj in objTotal:
        if maxValue == obj:
            totalPart += ('%' + str(maxWidths[obj]) + 's') % str(round(objTotal[obj], 2))
            totalPart += '|'
            continue
        totalPart += ('%' + str(maxWidths[obj]) + 's') % str(round(objTotal[obj], 2))
        totalPart += '|'
    print(totalPart)
    print(header_line)
    print('Найкращий варіант серед ноутбуків: ' + maxValue )

file = open_file()

parameters = {}
objects = re.split(';', re.sub('\n', '', file.readline()))
maxWidths = { 'PARAMETER': len("Parameter\t|"), 'COEFFICIENT': len('Coefficient|'), 'NUMBER': 2 }


for line in file:
    [parameter, values_str] = re.split(':', re.sub('\n', '', line))
    values = re.split(';', values_str)
    if (len(values) - 1 < len(objects)):
        exit()

    parameters[parameter] = {}
    parameters[parameter]['COEFFICIENT'] = float(values[0])

    if (len(parameter) > maxWidths['PARAMETER']): maxWidths['PARAMETER'] = len(parameter)
    if (len(values[0]) > maxWidths['COEFFICIENT']): maxWidths['COEFFICIENT'] = len(values[0])

    for i in range(0, len(objects)):
        parameters[parameter][objects[i]] = float(values[i + 1])

maxWidths['NUMBER'] = len(str(len(parameters))) + 1

set_max_object_length(parameters, objects, maxWidths)
header = draw_header(objects, maxWidths)
parameter_str = str(draw_parameters(parameters, objects, maxWidths))[:-1]
print_result(header, parameter_str)

print('\nПораховані значення параметрів:')
for param in parameters:
    for obj in objects:
        parameters[param][obj] = float(parameters[param]['COEFFICIENT']) * float(parameters[param][obj])

set_max_object_length(parameters, objects, maxWidths)

header = draw_header(objects, maxWidths)
parameter_str = str(draw_parameters(parameters, objects, maxWidths)[:-1])
print_result(header, parameter_str)
print_total(header, objects, parameters, maxWidths)
