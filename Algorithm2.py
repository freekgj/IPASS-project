from AIvsPlayerGame import goodBadClickedFinal, setGoodOrBadToZero
"""pinWeKnow staan cijfers ieder reprecenteert de kleurcode die zeker zijn"""
PinWeKnow = [0, 0, 0, 0]
lastQuess = []
howManyBlackWhite = []
firstRound = True
def responseAlgorithm2():
    #feedback = [goodBadClickedFinal['pin1'], goodBadClickedFinal['pin2'], goodBadClickedFinal['pin3'], goodBadClickedFinal['pin4']]
    global firstRound
    if firstRound == False:
        howManyBlackWhite.append([goodBadClickedFinal['black'], goodBadClickedFinal['white'], goodBadClickedFinal['grey']])
        setGoodOrBadToZero()
    firstRound = False

    """Het Algoritme"""



    quess1 = 5
    quess2 = 6
    quess3 = 2
    quess4 = 4
    AIquess = [quess1, quess2, quess3, quess4]
    lastQuess.append([quess1, quess2, quess3, quess4])

    return AIquess

