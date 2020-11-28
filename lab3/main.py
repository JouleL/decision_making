#!/usr/bin/python

import re
from condorcet_method import condorcet_method
from borda_method import borda_method


def open_file():
    try:
        return open("yatsynych_31(1).txt")
    except FileNotFoundError:
        print("Error, no such file!")
        exit()


file = open_file()
lines = []
benefits = []

for line in file:
    if not (line and not line.isspace()):
        continue
    row = re.split(';', re.sub('\n', '', line))
    new_benefits = re.split(',', row[1])
    for benefit in new_benefits:
        if benefit not in benefits:
            benefits.append(benefit)

    lines.append([row[0], new_benefits])

print("\nМетод Кондорсе:")
condorcet_result = condorcet_method(lines, benefits)
print("Звідси найкраще рішення:", ">".join(condorcet_result["places"]))

print("\nМетод Борда:")
borda_result = borda_method(lines, benefits)
print("Рахуємо голоси: \n_________________________________")
for note in borda_result['note'].keys():
    print(note, ":", borda_result["note"][note], "=", borda_result["sum"][note])
    print("_________________________________")
print("Звідси накраще рішення:", ">".join(condorcet_result["places"]))
