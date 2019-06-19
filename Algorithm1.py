import random

from AIvsPlayerGame import theCode
quessedCode = []

def responseAlgorithm1():
    """value moet gelijk zijn aan een lijst met 4 integer elementen"""
    beurtenteller = 0
    theCodeList = [theCode['pin1'], theCode['pin2'], theCode['pin3'], theCode['pin4']]
    global quessedCode
    while quessedCode != theCodeList:
        quessList = []
        for number in range(4):
            quessList.append(random.randrange(1, 7))
        if quessList not in quessedCode:
            quessedCode.append(quessList)
            beurtenteller += 1
            if quessList == theCodeList:
                break

    return [quessList, beurtenteller]

