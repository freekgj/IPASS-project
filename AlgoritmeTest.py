import random

AIquess1 = 1
AIquess2 = 2
turn = 0
AIquess = []
feedbackPins = ()

def AIconfig(AIquess):
    if AIquess == 2:
        AIquessReturn = 1
    else:
        AIquessReturn = AIquess + 1
    return AIquessReturn

def AI(feedbackPins):
    global AIquess
    global turn
    global returnValue
    AIquessTemp1 = None
    AIquessTemp2 = None
    returnValue = None
    if turn == 0:
        AIquessTemp1 = random.randint(1,2)
        AIquessTemp2 = random.randint(1,2)
        returnValue = [AIquessTemp1, AIquessTemp2]
    else:
        if turn == 1:
            if feedbackPins == (2, 0):
                returnValue = ("geraden!")

            elif feedbackPins == (0, 0):
                AIquessTemp1 = AIconfig(AIquess[turn-1][0])
                AIquessTemp2 = AIconfig(AIquess[turn-1][1])

            elif feedbackPins == (1, 0):
                AIquessTemp1 = AIquess[turn-1][0]
                AIquessTemp2 = AIconfig(AIquess[turn-1][1])

            returnValue = [AIquessTemp1, AIquessTemp2]

        elif turn == 2:
            if feedbackPins == (2, 0):
                returnValue = "geraden!"

            elif feedbackPins == (0, 2):
                AIquessTemp1 = AIquess[turn-1][1]
                AIquessTemp2 = AIquess[turn-1][0]

            elif feedbackPins == (0, 0):
                AIquessTemp1 = AIconfig(AIquess[turn-1][0])
                AIquessTemp2 = AIconfig(AIquess[turn-1][1])

            returnValue = [AIquessTemp1, AIquessTemp2]

        elif turn == 3:
            if feedbackPins == (2, 0):
                returnValue = "geraden!"
            else:
                returnValue = "dit klopt niet."
    AIquess.append(returnValue)
    turn += 1
    print("turn = " + str(turn))
    return returnValue