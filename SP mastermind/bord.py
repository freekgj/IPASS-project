import os
import sys
import pydoc
import tkinter as tk
from AIvsPlayerGame import changeColor, setCode, theCode, setRow, getRow, changeGoodOrBad, colorCode, setGoodOrBad, \
    goodBadClickedFinal, setGoodOrBadToZero, setPinsClickedToZero, masterReset, possibleCodes
from bad_algorithm import responseAlgorithm1
from good_algorithm import theAlgorithm

possibleCodesLeft = []
lastGuess = []

class Program(tk.Tk):
    """__init__ is een speciale functie. Wanneer je een object van deze class aanmaakt hoef je deze functie niet
    expliciet te noemen. Deze functie wordt automatisch aangeroepen op het moment dat het programma deze class laad.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        """Het programma krijgt een titel toegewezen"""
        self.title('Mastermind')

        """Op deze manier zal het scherm altijd in full screen worden uitgebeeld."""
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        self.geometry("{}x{}+-7+0".format(screenWidth, screenHeight-27))

        """dit vormt de omgeving waarin frames geplaatst kunnen worden."""
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        """check dit youtubefilmpje en aan de hand daarvan uit hoe onderstaande werkt. Heeft te maken met het opheffen 
         van een pagina. --> https://www.youtube.com/watch?v=jBUpjijYtCk&t=105s <--"""

        self.frames = {}
        for page in (MainPage, AIvsPlayer, SpelUitleg):
            pageName = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[pageName] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("MainPage")

    def showFrame(self, pageName):
        """Plaatst de gewenste frame voor de andere frames."""
        frame = self.frames[pageName]
        frame.tkraise()

class MainPage(tk.Frame):
    """In deze class vind je het hoofdmenu"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller
        frameBovenMainpage = tk.Frame(self, bg="red")
        frameOnderMainpage = tk.Frame(self, bg="white")
        titel = tk.Label(frameBovenMainpage, text="Welkom bij Freek's mastermind super solver!", fg='black', bg="white")
        titel.config(font='Arial 35 bold')
        """wat doet SUNKEN????"""

        photo_image = tk.PhotoImage(file='mastermind.png')
        photo_label = tk.Label(frameBovenMainpage, image=photo_image, width=100, height=290)
        photo_label.image = photo_image
        startGameButton = tk.Button(frameOnderMainpage, text="start game AI vs player", height=5, width=23, fg="white", bg="black",
                            command=lambda: controller.showFrame("AIvsPlayer"))
        uitlegSpelButton = tk.Button(frameOnderMainpage, text="Uitleg van het spel", height=5, width=23, fg='white', bg='black',
                            command=lambda: controller.showFrame("SpelUitleg"))
        exitGameButton = tk.Button(frameOnderMainpage, text="Exit game", height=5, width=23, fg='white', bg='black', command=frameBovenMainpage.quit)
        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        frameBovenMainpage.pack(pady=0, expand=tk.TRUE)
        frameOnderMainpage.pack(expand=tk.TRUE)
        titel.pack(side=tk.TOP, fill=tk.X)
        photo_label.pack(side=tk.TOP, fill=tk.X)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        startGameButton.pack(side=tk.LEFT, fill=tk.X, padx=5)
        uitlegSpelButton.pack(side=tk.LEFT, fill=tk.X, padx=5)
        exitGameButton.pack(side=tk.LEFT, fill=tk.X, padx=5)

class AIvsPlayer(tk.Frame):
    """In deze class vind"""
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg="grey")
        self.controller = controller

        frame3 = tk.Frame(self, bg="grey", height=200, width=200)
        frame4 = tk.Frame(self, bg="grey", height=200, width=200)
        frame5 = tk.Frame(self, bg="grey")

        """in frame 3 is alleen het antwoord van het langste algoritme te vinden."""
        uitkomstAlgorithm = tk.Label(frame3, text="", bg='grey', font="Arial 18 bold")

        """In frame 4 is een tabel met 4 x 10 buttons te vinden waarin de speler kan aangegeven in hoeverre de pinnen
        ingevuld door de AI goed zijn."""

        chooseAlgorithm1Button = tk.Button(frame5, font='bold', text='BAD algorithm', height=2, width=16, command=lambda: algorithmConfig(1), bg='red')
        chooseAlgorithm2Button = tk.Button(frame5, font='bold', text='REGULAR algorithm', height=2, width=16, command=lambda: algorithmConfig(2), bg='white')
        chooseAlgorithm3Button = tk.Button(frame5, font='bold', text='GOOD algorithm', height=2, width=16, command=lambda: algorithmConfig(3), bg='white')

        f4grid = []
        for row in range(10):
            current_row = []
            for column in range(8):
                f4square = tk.Label(frame4, text='    ', borderwidth=1, relief=tk.SUNKEN, bg='grey')
                f4square.grid(row=row, column=column)
                current_row.append(f4square)
            f4grid.append(current_row)

        f5grid = []
        for row in range(11):
            current_row = []
            for column in range(4):
                f5square = tk.Label(frame4, text='    ', borderwidth=5, relief=tk.SUNKEN, bg='grey')
                f5square.grid(row=row, column=column)
                current_row.append(f5square)
            f5grid.append(current_row)

        """In frame 5 zijn de knoppen te vinden voor het bepalen van de geheime code en de enter button"""
        label2 = tk.Label(frame5, text="Jouw geheime code:", font="Arial 18 bold", fg='black', bg="grey")
        label3 = tk.Label(frame5, text="pin1   pin2    pin3    pin4", padx=10, font="Arial 14", bg='grey')

        """filmpje hoe command werkt zonder dat hij direct wat uitprint d.m.v. lambda.
        --> https://www.youtube.com/watch?v=Y6cir7P3YUk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=3 <--"""

        returnToHomepageButton = tk.Button(frame5, text="Return to mainpage", height=5, width=23, fg="white", bg="black",
                            command=lambda: masterReset())
        codeSetPin1Button = tk.Button(frame5, height=2, width=5, command=lambda: configBut(1), bg='grey')
        codeSetPin2Button = tk.Button(frame5, height=2, width=5, command=lambda: configBut(2), bg='grey')
        codeSetPin3Button = tk.Button(frame5, height=2, width=5, command=lambda: configBut(3), bg='grey')
        codeSetPin4Button = tk.Button(frame5, height=2, width=5, command=lambda: configBut(4), bg='grey')
        enterButton = tk.Button(frame5, text='ENTER', height=2, width=5, fg='black', command=lambda: configEnter(), bg='grey')

        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        returnToHomepageButton.pack(side=tk.RIGHT, anchor='e')
        uitkomstAlgorithm.pack(side=tk.TOP)
        frame3.pack(side=tk.TOP,  expand=tk.TRUE)

        chooseAlgorithm1Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        chooseAlgorithm2Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        chooseAlgorithm3Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        frame4.pack(side=tk.TOP, expand=tk.FALSE)

        label2.pack(side=tk.TOP, anchor="w", padx=0, pady=0)
        label3.pack(side=tk.TOP, anchor="w", padx=0, pady=0)
        codeSetPin1Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        codeSetPin2Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        codeSetPin3Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        codeSetPin4Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        enterButton.pack(side=tk.LEFT, padx=100, pady=10)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        frame5.pack(side=tk.TOP, anchor='s', expand=tk.TRUE)

        def algorithmConfig(algorithmNumber):
            if theCode['codeSet'] == False:
                chooseAlgorithm1Button.config(bg='white')
                chooseAlgorithm2Button.config(bg='white')
                chooseAlgorithm3Button.config(bg='white')
                theCode['setAlgorithm'] = algorithmNumber

                if algorithmNumber == 1:
                    chooseAlgorithm1Button.config(bg='red')
                elif algorithmNumber == 2:
                    chooseAlgorithm2Button.config(bg='red')
                elif algorithmNumber == 3:
                    chooseAlgorithm3Button.config(bg='red')

        def configBut(pinNumber):
            if theCode['codeSet'] == False:
                changeButtonToColor = changeColor(pinNumber)
                if pinNumber == 1:
                    f5grid[10][0].config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 2:
                    f5grid[10][1].config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 3:
                    f5grid[10][2].config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 4:
                    f5grid[10][3].config(bg="{}".format(changeButtonToColor))

            else:
                blackWhiteBlanco = changeGoodOrBad(pinNumber)
                if pinNumber == 1:
                    f4grid[getRow()][4].config(bg="{}".format(blackWhiteBlanco))
                elif pinNumber == 2:
                    f4grid[getRow()][5].config(bg="{}".format(blackWhiteBlanco))
                elif pinNumber == 3:
                    f4grid[getRow()][6].config(bg="{}".format(blackWhiteBlanco))
                elif pinNumber == 4:
                    f4grid[getRow()][7].config(bg="{}".format(blackWhiteBlanco))

        def configEnter():
            global possibleCodesLeft
            global lastGuess
            if theCode['firstRound'] == False:
                setRow()
            setGoodOrBad()
            finalState = (goodBadClickedFinal['black'], goodBadClickedFinal['white'])
            codeOfPlayer = (str(theCode['pin1']) + str(theCode['pin2']) + str(theCode['pin3']) + str(theCode['pin4']))

            """https://www.youtube.com/watch?v=TQJRM8hIbXA&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=12"""
            if finalState == (4, 0):
                uitkomstAlgorithm.config(text="""The AI have guessed the game!""", font="Arial 25 bold")

            if theCode['codeSet'] == False:
                setCode()

            """
            Het eerste algoritme
            ___________________________________________________________________________________________________
            """

            if theCode['setAlgorithm'] == 1:
                AIquessesInColor = []
                AIquesses = responseAlgorithm1()
                for colorNumber in AIquesses[0]:
                    AIquessesInColor.append(colorCode(colorNumber))

                uitkomstAlgorithm.config(text="""De code is {}, {}, {}, {} en dit heeft het algoritme {} beurten
                gekost.""".format(AIquessesInColor[0], AIquessesInColor[1], AIquessesInColor[2], AIquessesInColor[3], AIquesses[1]))


            """                                                                                                
            Het tweede algoritme                                                                               
            ___________________________________________________________________________________________________
            """

            if theCode['setAlgorithm'] == 2:
                colorResponseAI2 = []
                responseAI2 = algorithmIn5Steps((goodBadClickedFinal['black'], goodBadClickedFinal['white']))
                for item in responseAI2:
                    colorResponseAI2.append(colorCode(item))

                for pin in range(4):
                    f5grid[getRow()][pin].config(bg='{}'.format(colorResponseAI2[pin]))

            if theCode['setAlgorithm'] == 3:
                colorResponseAI2X = []
                responseAI2X = theAlgorithm(possibleCodesLeft, (goodBadClickedFinal['black'], goodBadClickedFinal['white']), lastGuess)

                for item in responseAI2X[0]:
                    colorResponseAI2X.append(colorCode(item))
                for pin in range(4):
                    f5grid[getRow()][pin].config(bg='{}'.format(colorResponseAI2X[pin]))

                possibleCodesLeft = responseAI2X[1]
                lastGuessInt = [responseAI2X[0][0], responseAI2X[0][1], responseAI2X[0][2], responseAI2X[0][3]]
                lastGuess = ""
                for item in lastGuessInt:
                    lastGuess += str(item)

            setPinsClickedToZero()
            setGoodOrBadToZero()
            if theCode['firstRound'] == False and codeOfPlayer not in possibleCodesLeft and codeOfPlayer != lastGuess and finalState != (4,0):
                uitkomstAlgorithm.config(text="""Oh oh, you cheated, don't do that again!""", font="Arial 25 bold")
            theCode['firstRound'] = False

        def masterReset():
            python = sys.executable
            os.execl(python, python, *sys.argv)

class SpelUitleg(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller

        frame6 = tk.Frame(self, bg="white")
        label3 = tk.Label(frame6, font='Arial 18 bold', bg='white', text='Hoe werkt Mastermind?')
        label4 = tk.Label(frame6, font='Arial 14', bg='white', text="""Het doel van het spel is om de kleurcode van jouw opponent te achterhalen.\nEen van de spelers is de codemaker, deze dient een code te maken met vier\ngekleurde pionnen. Deze code is alleen zichtbaar voor de codemaker, er kan\ngekozen worden uit zes verschillende kleuren. De andere speler of spelers mag\nvervolgens proberen om de code te breken door vier pionnen op de eerste rij te\nplaatsen. De maker van de code moet vervolgens aangeven of pionnen op de juiste \n positie staan, geen enkele pion goed is geplaatst of dat de juiste kleuren aanwezig zijn. \n Dit doet hij door middel van zwarte en witte pinnen in het bord te plaatsen. Vervolgens\nmag de codebreker weer opnieuw een rij opvullen. De speler die de code binnen het\nminst aantal beurten weet te raden is de winnaar. """)
        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")
        button1 = tk.Button(frame6, text="Return to mainpage", height=5, width=23, fg="white", bg="black",
                            command=lambda: controller.showFrame("MainPage"))
        button1.pack(side=tk.BOTTOM)
        label3.pack(side=tk.TOP, fill=tk.X, padx=5)
        label4.pack(side=tk.LEFT, anchor='n', fill=tk.X, padx=5)
        frame6.pack(pady=100, expand=tk.TRUE)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

if __name__ == "__main__":
    game = Program()
    game.mainloop()