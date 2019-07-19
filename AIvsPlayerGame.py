from itertools import product

theCode = {'pin1': 0,
           'pin2': 0,
           'pin3': 0,
           'pin4': 0,
           'codeSet': False,
           'firstRound': True,
           'setAlgorithm': 1
           }

timesClicked = {'timesClickedPin1':0,
                'timesClickedPin2':0,
                'timesClickedPin3':0,
                'timesClickedPin4':0}

goodBadClickedFinal = {'black': 0,
                       'white': 0}

goodBadClicked = {'timesClickedPin1':0,
                  'timesClickedPin2':0,
                  'timesClickedPin3':0,
                  'timesClickedPin4':0}

row = 0

listPossibleCodes = []

def masterReset():
    global theCode
    global row
    row = 0
    theCode = {'pin1': 0,
           'pin2': 0,
           'pin3': 0,
           'pin4': 0,
           'codeSet': False,
           'firstRound': True,
           'setAlgorithm': 0
           }
    setGoodOrBadToZero()
    setPinsClickedToZero()

def setListWithPosibbleCodes():
    for number in range(1111, 6667):
        listPossibleCodes.append(number)
    return listPossibleCodes

def colorCode(clicked):
    if clicked == 0:
        return 'grey'
    if clicked == 1:
        return 'white'
    elif clicked == 2:
        return 'black'
    elif clicked == 3:
        return 'yellow'
    elif clicked == 4:
        return 'red'
    elif clicked == 5:
        return 'green'
    elif clicked == 6:
        return 'blue'
    else:
        print("colorCode error")

def changeColor(pinNumber):
    global timesClicked
    if timesClicked['timesClickedPin{}'.format(pinNumber)] == 6:
        timesClicked['timesClickedPin{}'.format(pinNumber)] = 1
    else:
        timesClicked['timesClickedPin{}'.format(pinNumber)] += 1
    clicked = timesClicked['timesClickedPin{}'.format(pinNumber)]
    colorOfPin = colorCode(clicked)
    return colorOfPin

def setCode():
    global theCode
    theCode['pin1'] = timesClicked['timesClickedPin1']
    theCode['pin2'] = timesClicked['timesClickedPin2']
    theCode['pin3'] = timesClicked['timesClickedPin3']
    theCode['pin4'] = timesClicked['timesClickedPin4']
    theCode['codeSet'] = True

def changeGoodOrBad(pinNumber):
    global goodBadClicked
    if goodBadClicked['timesClickedPin{}'.format(pinNumber)] == 2:
        goodBadClicked['timesClickedPin{}'.format(pinNumber)] = 0
    else:
        goodBadClicked['timesClickedPin{}'.format(pinNumber)] += 1
    clicked = goodBadClicked['timesClickedPin{}'.format(pinNumber)]
    colorOfPin = colorCode(clicked)
    return colorOfPin

def setGoodOrBad():
    global goodBadClickedFinal
    for item in goodBadClicked.values():
        if item == 2:
            goodBadClickedFinal['black'] += 1
        elif item == 1:
            goodBadClickedFinal['white'] += 1

def setGoodOrBadToZero():
    global goodBadClickedFinal
    goodBadClickedFinal['black'] = 0
    goodBadClickedFinal['white'] = 0

def setPinsClickedToZero():
    global goodBadClicked
    goodBadClicked = {'timesClickedPin1': 0,
                    'timesClickedPin2': 0,
                    'timesClickedPin3': 0,
                    'timesClickedPin4': 0}

def possibleCodes(aantalKleuren, lengthOfCode):
    colors = ''
    for color in range(aantalKleuren):
        colors += str(color + 1)
    listWithPossibleCodes = list(product(colors, repeat=lengthOfCode))
    for codeIndex in range(len(listWithPossibleCodes)):
        listWithPossibleCodes[codeIndex] = "".join(listWithPossibleCodes[codeIndex])
    return listWithPossibleCodes

def setRow():
    global row
    row +=1

def getRow():
    global row
    return row

