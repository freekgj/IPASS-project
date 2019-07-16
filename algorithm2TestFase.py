import random
from AIvsPlayerGame import theCode, setListWithPosibbleCodes

#mijnCode 21

listPosibbleCodes = []
previousGuess = []
previousFeedback = []
turn = 1

def algorithmIn5Steps(feedbackBlackWhitePins):
    global turn
    if theCode['firstRound']:
        listPosibbleCodes = setListWithPosibbleCodes()
        quess1 = random.randrange(1, 3)
        quess2 = quess1
        quess3 = random.randrange(1, 3, quess1)
        quess4 = quess3
        ## !!!!dit wordt gedaan bij bord.py!!!! theCode['firstRound'] = False
    else:
        previousFeedback.append(feedbackBlackWhitePins)
        if turn == 2:
            if feedbackBlackWhitePins == (2,0):
                quess1 = 1
                quess2 = 1
                quess3 = 1
                quess4 = 1
            elif feedbackBlackWhitePins == (3,0):
                quess1 = 1
                quess2 = 1
                quess3 = 1
                quess4 = 2
            elif feedbackBlackWhitePins == (0,4):
                quess1 = 2
                quess2 = 2
                quess3 = 1
                quess4 = 1
            elif feedbackBlackWhitePins == (1,2):
                quess1 = 1
                quess2 = 2
                quess3 = 1
                quess4 = 1
            elif feedbackBlackWhitePins == (2,2):
                quess1 = 1
                quess2 = 2
                quess3 = 1
                quess4 = 2
        elif turn == 3:
            print('it works!')


    AIguess = [quess1, quess2, quess3, quess4]
    global previousGuess
    previousGuess.append(AIguess)
    turn +=1
    return AIguess