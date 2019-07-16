import random
listPossibleCodes = []
theCode = [5, 2, 3, 6]
quessedPins = []
feedbackPins = []
turn = 0

def goodAI(feedback):
    global guessedPins
    global turn
    if feedbackPins == []:
        quess1 = random.randrange(1, 6)
        quess2 = quess1
        quess3 = random.randrange(1, 6)
        while quess3 == quess1:
            quess3 = random.randrange(1, 6)
        quess4 = quess3

    elif turn == 1:
        print("hi")
    turn += 1
    quessedPins.append([quess1, quess2, quess3, quess4])
    return quessedPins

def makeUniqueCode():
    quess1 = random.randrange(1, 3)
    quess2 = quess1
    quess3 = random.randrange(1, 3, quess1)
    quess4 = quess3
    return [quess1, quess2, quess3, quess4]

quess1 = 1
quess2 = 1
quess3 = 2
quess4 = 2

while quess1 != quess4 and quess2 != quess3 and quess1 == quess2 and quess3 == quess4:
    feedback = makeUniqueCode()
    quess1 = feedback[0]
    quess2 = feedback[1]
    quess3 = feedback[2]
    quess4 = feedback[3]
    print(quess1, quess2, quess3, quess4)