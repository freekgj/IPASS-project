# imports
import random
from itertools import product
import numpy as np

class Opponent():
    def __init__(self):
        self.aantalKleuren = 6
        self.lengthOfCode = 4
        self.possibleMoves = self.calculateAllPossibleCombinations()

    def calculateAllPossibleCombinations(self):
        # hier de functie die alle mogelijke kleurcombinaties genereerd
        colors = ''
        for color in range(self.aantalKleuren):
            colors += str(color + 1)
        listWithPossibleCodes = list(product(colors, repeat=self.lengthOfCode))
        for codeIndex in range(len(listWithPossibleCodes)):
            listWithPossibleCodes[codeIndex] = "".join(listWithPossibleCodes[codeIndex])
        return listWithPossibleCodes

    def calculateNextMove(self, lastGuess, lastFeedback, beurt):
        return [0, 0, 0, 0]

class NaiefOpponent(Opponent):
    def calculateNextMove(self, lastGuess, lastFeedback, beurt):
        self.lastGuess = np.random.choice(self.possibleMoves)
        self.possibleMoves.remove(self.lastGuess)
        return self.lastGuess

class KnuthOpponent(Opponent):

    def calculateNextMove(self, lastGuess, lastFeedback, beurt):
        self.lastGuess = lastGuess
        self.lastFeedback = lastFeedback
        self.beurt = beurt

        if self.beurt == 0:
            pin1 = random.randrange(1, self.aantalKleuren + 1)
            pin2 = pin1
            pin3 = random.randrange(1, self.aantalKleuren + 1)
            while pin3 == pin1:
                pin3 = random.randrange(1, self.aantalKleuren + 1)
            pin4 = pin3
            nextGuess = '{}{}{}{}'.format(pin1, pin2, pin3, pin4)
        else:
            possibleMovesAfterCheck = []
            for option in self.possibleMoves:
                if self.checkCode(self.lastGuess, option) == self.lastFeedback:
                    possibleMovesAfterCheck.append(option)
            self.possibleMoves = possibleMovesAfterCheck
            nextGuess = np.random.choice(self.possibleMoves)
        self.possibleMoves.remove(str(nextGuess))
        return nextGuess

    def checkCode(self, code1, code2):
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

        for kleur in code1:
            codeA['{}'.format(kleur)] += 1

        for kleur in code2:
            codeB['{}'.format(kleur)] += 1

        for kleur in code1:
            if int(code1[index]) == int(code2[index]):
                codeA['{}'.format(kleur)] -= 1
                codeB['{}'.format(kleur)] -= 1
                black += 1
            index += 1

        for key in codeA.keys():
            white += min(codeA['{}'.format(key)], codeB['{}'.format(key)])
        return (black, white)