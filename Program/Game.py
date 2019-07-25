
class Game():
    def __init__(self, code, opponent, opponentNumber):
        """Maakt data aan voor een nieuw spel."""
        self.secretCode = code
        self.opponent = opponent
        self.opponentInNumber = opponentNumber
        self.beurt = 0
        self.lastGuess = ''
        self.lastFeedback = (0, 0)
        self.codeInColor = []
        self.firstRound = True
        self.playerCheat = False
        self.gameWon = False

    def nextMove(self):
        """Bij het aanklikken van de knop 'OFF' in een spel Mastermind, zal deze functie worden aangeroepen. nextMove()
        zal een keer een algoritme vragen om een gok te doen en vraagt na deze functie weer aan te roepen datzelfde
        algoritme nog een keer een gok te wagen."""
        if not self.gameWon:
            self.lastGuess = self.opponent.calculateNextMove(self.lastGuess, self.lastFeedback, self.beurt)
            if str(self.secretCode) in self.opponent.possibleMoves or self.lastGuess == str(self.secretCode):
                self.beurt += 1
                print(self.secretCode)
                print(self.opponent.possibleMoves)
            else:
                self.playerCheat = True
        return self.convertToColors(self.lastGuess), self.playerCheat, self.gameWon

    def nextMoveWithAutoFeedback(self):
        """Bij het aanklikken van de knop 'ON' in een spel Mastermind, zal deze functie worden aangeroepen.
        nextMoveWithAutoFeedback() zal een algoritme om een gok vragen en daar vervolgens zelf feedback op geven tot de
        code geraden is."""
        if not self.gameWon:
            if self.opponentInNumber == 1:
                while not self.lastGuess == self.secretCode or self.lastGuess == []:  # TODO: check of self.secretCOde in zelfde format als guess
                    self.lastGuess = self.opponent.calculateNextMove(self.lastGuess, self.lastFeedback, self.beurt)
                    self.beurt += 1
                self.gameWon = True
            else:
                if not self.firstRound:
                    self.beurt += 1
                    # [] geeft aan dat opponent niets meer te gokken heeft
                    #TODO: voor iteratief spelen met slimme tegenstander is een functie nodig om self.lastFeedback te berekenen a.h.v. self.lastGuess
                self.lastGuess = self.opponent.calculateNextMove(self.lastGuess, self.lastFeedback, self.beurt)
                self.lastFeedback = self.autoFeedback()
        return self.convertToColors(self.lastGuess), self.lastFeedback, self.beurt, self.gameWon

    def autoFeedback(self):
        """Deze functie geeft automatisch feedback op een gok van een algoritme."""
        codeA = {'1': 0,
                 '2': 0,
                 '3': 0,
                 '4': 0,
                 '5': 0,
                 '6': 0
                 }
        codeB = {'1': 0,
                 '2': 0,
                 '3': 0,
                 '4': 0,
                 '5': 0,
                 '6': 0
                 }
        black = 0
        white = 0
        index = 0

        for kleur in self.secretCode:
            codeA['{}'.format(kleur)] += 1

        for kleur in self.lastGuess:
            codeB['{}'.format(kleur)] += 1

        for kleur in self.secretCode:
            if int(self.secretCode[index]) == int(self.lastGuess[index]):
                codeA['{}'.format(kleur)] -= 1
                codeB['{}'.format(kleur)] -= 1
                black += 1
            index += 1

        for key in codeA.keys():
            white += min(codeA['{}'.format(key)], codeB['{}'.format(key)])
        return (black, white)

    def convertToColors(self, guess):
        """Veranderd kleur codes in getal naar de bijbehorende kleur."""
        guessInColorsList = []
        for item in guess:
            if item == '0':
                guessInColorsList.append('grey')
            elif item == '1':
                guessInColorsList.append('white')
            elif item == '2':
                guessInColorsList.append('black')
            elif item == '3':
                guessInColorsList.append('yellow')
            elif item == '4':
                guessInColorsList.append('red')
            elif item == '5':
                guessInColorsList.append('green')
            elif item == '6':
                guessInColorsList.append('blue')
            else:
                print("colorCode error")
        return guessInColorsList

    def update(self, feedback, autofeedback):
        """Wordt aangeroepen wanneer de GUI interactie maakt met het spelverloop. (Game.py)"""
        self.lastFeedback = feedback

        if self.lastFeedback == (4, 0):
            self.gameWon = True

        # vraag opponent om volgende zet
        if autofeedback:
            GUIReturnValue = self.nextMoveWithAutoFeedback()
        elif autofeedback == False:
            GUIReturnValue = self.nextMove()
        else:
            GUIReturnValue = ''

        self.firstRound = False

        return GUIReturnValue