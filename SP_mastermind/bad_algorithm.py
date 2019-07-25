import numpy

from AIvsPlayerGame import theCode, possibleCodes

def responseAlgorithm1():
    """value moet gelijk zijn aan een lijst met 4 integer elementen"""
    beurtenteller = 0
    codeOfPlayer = int(str(theCode['pin1']) + str(theCode['pin2']) + str(theCode['pin3']) + str(theCode['pin4']))
    aantalKleuren = 6
    lengthOfCode = 4
    listPossibleCodesLeft = possibleCodes(aantalKleuren, lengthOfCode)
    while listPossibleCodesLeft != []:
        guessCode = numpy.random.choice(listPossibleCodesLeft)
        if int(guessCode) != codeOfPlayer:
            listPossibleCodesLeft.remove(guessCode)
            beurtenteller +=1
        else:
            pin1 = int(guessCode[0])
            pin2 = int(guessCode[1])
            pin3 = int(guessCode[2])
            pin4 = int(guessCode[3])
            return [[pin1, pin2, pin3, pin4], beurtenteller]

#kijk wat het gemiddelde aantal beurten is van 100 x het spel draaien.
#ook van good algoritme.
#entropie
#minmax
#class maken van de speler