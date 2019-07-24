import numpy
import random

from AIvsPlayerGame import theCode
from bad_algorithm import responseAlgorithm1

countPlayed = 0
listWithTurns = []
total = 0
while countPlayed != 100:
    theCode['pin1'] = random.randrange(1, 7)
    theCode['pin2'] = random.randrange(1, 7)
    theCode['pin3'] = random.randrange(1, 7)
    theCode['pin4'] = random.randrange(1, 7)
    AIresponse = responseAlgorithm1()
    listWithTurns.append(AIresponse[1])
    countPlayed += 1

for item in listWithTurns:
    total += item

average = total / 100

print('gemiddeld heeft de AI over 100 spelletjes {} beurten nodig om de code te raden.'.format(average))