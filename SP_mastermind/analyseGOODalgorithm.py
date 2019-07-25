import numpy

from AIvsPlayerGame import possibleCodes, colorCode, theCode
from good_algorithm import theAlgorithm

countPlayed = 0
lastGuess = '0000'
listPossibleCodes = []
listBeurtCount = []
total = 0

theCodeOfPlayer = {'pin1':0,
                   'pin2':0,
                   'pin3':0,
                   'pin4':0}

codeA = {'white':0,
         'black':0,
         'yellow':0,
         'red':0,
         'green':0,
         'blue':0
         }

codeB = {'white':0,
         'black':0,
         'yellow':0,
         'red':0,
         'green':0,
         'blue':0
         }

def feedbackPins(stringTheCodeOfPlayer, lastGuess):
    black = 0
    white = 0
    index = 0
    if theCode['firstRound']:
        black = 0
        white = 0
    else:
        for kleur in stringTheCodeOfPlayer:
            codeA['{}'.format(colorCode(int(kleur)))] +=1
        for kleur in lastGuess:
            codeB['{}'.format(colorCode(int(kleur)))] +=1
        for kleur in theCodeOfPlayer.values():
            if stringTheCodeOfPlayer[index] == lastGuess[index]:
                codeA['{}'.format(colorCode(int(kleur)))] -= 1
                codeB['{}'.format(colorCode(int(kleur)))] -= 1
                black += 1
            index += 1

        for key in codeA.keys():
            white += min(codeA['{}'.format(key)], codeB['{}'.format(key)])
    return (black, white)

def setFeedbackZero():
    global codeA
    global codeB
    codeA = {'white': 0,
             'black': 0,
             'yellow': 0,
             'red': 0,
             'green': 0,
             'blue': 0
             }

    codeB = {'white': 0,
             'black': 0,
             'yellow': 0,
             'red': 0,
             'green': 0,
             'blue': 0
             }

while countPlayed != 100:
    theCode['firstRound'] = True
    kleuren = 6
    pins = 4
    listPossibleCodes = possibleCodes(kleuren, pins)
    beurtCount = 0
    stringTheCodeOfPlayer = numpy.random.choice(listPossibleCodes)
    theCodeOfPlayer['pin1'] = int(stringTheCodeOfPlayer[0])
    theCodeOfPlayer['pin2'] = int(stringTheCodeOfPlayer[1])
    theCodeOfPlayer['pin3'] = int(stringTheCodeOfPlayer[2])
    theCodeOfPlayer['pin4'] = int(stringTheCodeOfPlayer[3])
    while True:

        feedback = feedbackPins(stringTheCodeOfPlayer, lastGuess)

        setFeedbackZero()
        AIfeedback = theAlgorithm(listPossibleCodes, feedback, lastGuess)
        guess = '{}{}{}{}'.format(AIfeedback[0][0], AIfeedback[0][1], AIfeedback[0][2], AIfeedback[0][3])
        if guess == stringTheCodeOfPlayer:
            beurtCount += 1
            listBeurtCount.append(beurtCount)
            break
        else:
            beurtCount += 1
            lastGuess = guess
        theCode['firstRound'] = False

    countPlayed += 1

for item in listBeurtCount:
    total += item

average = total / 100

print('gemiddeld heeft de AI over 100 spelletjes {} beurten nodig om de code te raden.'.format(average))