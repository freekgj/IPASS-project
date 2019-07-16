from AIvsPlayerGame import goodBadClickedFinal, setGoodOrBadToZero
import random

"""pinWeKnow staan cijfers ieder reprecenteert de kleurcode die zeker zijn"""
PinWeKnow = [0, 0, 0, 0]
quesses = []
howManyBlackWhite = []
firstRound = True
def responseAlgorithm2(feedbackpins):
    global firstRound
    global quesses
    quess1 = 0
    quess2 = 0
    quess3 = 0
    quess4 = 0
    if firstRound == False:
        howManyBlackWhite.append([goodBadClickedFinal['black'], goodBadClickedFinal['white'], goodBadClickedFinal['grey']])
        print(howManyBlackWhite)
        setGoodOrBadToZero()
    print(quesses)

    """Het Algoritme"""

    if firstRound == True:
        quess1 = random.randrange(1,6)
        quess2 = quess1
        quess3 = random.randrange(1,6)

        while quess3 == quess1:
            quess3 = random.randrange(1,6)
        quess4 = quess3
    else:
        """kijk naar de goed/andere plek/fout pinnen en naar de kleuren die je hebt ingegeven."""


    firstRound = False

    quesses.append([quess1, quess2, quess3, quess4])
    AIquess = [quess1, quess2, quess3, quess4]
    return AIquess

