from itertools import product

import numpy

from AIvsPlayerGame import theCode, colorCode
import random

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

def theAlgorithm(listPossibleCodesLeft, feedbackpins, lastGuess):
    if theCode['firstRound']:
        print("first round")
        print("lastguess:", lastGuess)
        aantalKleuren = 6
        lengthOfCode = 4
        listPossibleCodesLeft = possibleCodes(aantalKleuren, lengthOfCode)
        pin1 = random.randrange(1, aantalKleuren+1)
        pin2 = pin1
        pin3 = random.randrange(1, aantalKleuren+1)
        while pin3 == pin1:
            pin3 = random.randrange(1, aantalKleuren+1)
        pin4 = pin3
    else:
        deleteItems = []
        listPossibleCodesLeft.remove(lastGuess)
        for code in listPossibleCodesLeft:
            correctCode = checkValidationCode(lastGuess, code)
            if correctCode != feedbackpins:
                deleteItems.append(code)
        for item in deleteItems:
            listPossibleCodesLeft.remove(item)
        print(listPossibleCodesLeft)
        guessCode = numpy.random.choice(listPossibleCodesLeft)
        print(guessCode)
        pin1 = int(guessCode[0])
        pin2 = int(guessCode[1])
        pin3 = int(guessCode[2])
        pin4 = int(guessCode[3])

    return [[pin1, pin2, pin3, pin4], listPossibleCodesLeft]

def possibleCodes(aantalKleuren, lengthOfCode):
    colors = ''
    for color in range(aantalKleuren):
        colors += str(color + 1)
    listWithPossibleCodes = list(product(colors, repeat=lengthOfCode))
    for codeIndex in range(len(listWithPossibleCodes)):
        listWithPossibleCodes[codeIndex] = "".join(listWithPossibleCodes[codeIndex])
    return listWithPossibleCodes

def checkValidationCode(code1, code2):
    setDictValue0()
    black = 0
    white = 0
    index = 0

    for kleur in code1:
        codeA['{}'.format(colorCode(int(kleur)))] +=1
    for kleur in code2:
        codeB['{}'.format(colorCode(int(kleur)))] +=1
    for kleur in code1:
        if int(code1[index]) == int(code2[index]):
            codeA['{}'.format(colorCode(int(kleur)))] -= 1
            codeB['{}'.format(colorCode(int(kleur)))] -= 1
            black += 1
        index += 1

    for key in codeA.keys():
        white += min(codeA['{}'.format(key)], codeB['{}'.format(key)])
    return (black, white)

def setDictValue0():
    for key in codeA:
        codeA['{}'.format(key)] = 0
        codeB['{}'.format(key)] = 0