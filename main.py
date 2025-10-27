from Game import Game
from Opponent import KnuthOpponent, NaiefOpponent
import os
import sys
import pydoc
import tkinter as tk

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        """Bouwt het aantal GUIpagina's op als wordt ingegeven."""
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('Mastermind')

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        self.geometry("{}x{}+-7+0".format(screenWidth, screenHeight - 27))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (MainPage, AIvsPlayer, PlayervsAI, SpelUitleg):
            pageName = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[pageName] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("MainPage")

    def showFrame(self, pageName):
        """Plaatst de gewenste GUIframe voor de andere GUIframes."""
        frame = self.frames[pageName]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        """Bouwt de GUI op voor de pagina Mainpage."""
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller

        frameBovenMainpage = tk.Frame(self, bg="red")
        frameOnderMainpage = tk.Frame(self, bg="white")

        titel = tk.Label(frameBovenMainpage, text="Welkom bij Freek's mastermind super solver!", fg='black', bg="white")
        titel.config(font='Arial 35 bold')

        photo_image = tk.PhotoImage(file='mastermind.png')
        photo_label = tk.Label(frameBovenMainpage, image=photo_image, width=100, height=290)
        photo_label.image = photo_image

        startGameButton = tk.Button(frameOnderMainpage, text="start spel AI vs player", height=5, width=23, fg="white",
                                    bg="black",
                                    command=lambda: controller.showFrame("AIvsPlayer"))
        StartGameButton2 = tk.Button(frameOnderMainpage, text="start spel player vs AI", height=5, width=23, fg="white",
                                    bg="black",
                                    command=lambda: controller.showFrame("PlayervsAI"))
        uitlegSpelButton = tk.Button(frameOnderMainpage, text="Uitleg van het spel", height=5, width=23, fg='white',
                                     bg='black',
                                     command=lambda: controller.showFrame("SpelUitleg"))
        exitGameButton = tk.Button(frameOnderMainpage, text="Exit game", height=5, width=23, fg='white', bg='black',
                                   command=frameBovenMainpage.quit)
        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20, bg="light blue",
                             text="Copyright© Freek Gerrits Jans")

        titel.pack(side=tk.TOP, fill=tk.X)
        photo_label.pack(side=tk.TOP, fill=tk.X)
        startGameButton.pack(side=tk.LEFT, fill=tk.X, padx=5)
        StartGameButton2.pack(side=tk.LEFT, fill=tk.X, padx=5)
        uitlegSpelButton.pack(side=tk.LEFT, fill=tk.X, padx=5)
        exitGameButton.pack(side=tk.LEFT, fill=tk.X, padx=5)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        frameBovenMainpage.pack(pady=0, expand=tk.TRUE)
        frameOnderMainpage.pack(expand=tk.TRUE)


class AIvsPlayer(tk.Frame):
    firstTurn = True
    autoFeedback = False
    freezeFrame = False
    secretCode = ''
    opponent = 1
    row = 0
    black = 0
    white = 0
    changePinTimesClicked = {'timesClickedPin1': 0,
                             'timesClickedPin2': 0,
                             'timesClickedPin3': 0,
                             'timesClickedPin4': 0}

    def __init__(AIvsPlayer, parent, controller):
        """Bouwt de GUI op voor de pagina Mainpage."""

        tk.Frame.__init__(AIvsPlayer, parent, bg="grey")
        AIvsPlayer.controller = controller

        boveninMiddenFrame = tk.Frame(AIvsPlayer, bg="grey", height=200, width=200)
        middeninLinksFrame = tk.Frame(AIvsPlayer, bg="grey", height=200, width=100)
        middeninMiddenFrame = tk.Frame(AIvsPlayer, bg="grey", height=200, width=300)
        onderinMiddenFrame = tk.Frame(AIvsPlayer, bg="grey")

        # in frame 3 is alleen het antwoord van het langste algoritme te vinden."""
        uitkomstAlgorithm = tk.Label(boveninMiddenFrame, text="", bg='grey', font="Arial 18 bold")

        # In frame 4 is een tabel met 4 x 10 buttons te vinden waarin de speler kan aangegeven in hoeverre de pinnen
        # ingevuld door de AI goed zijn."""

        chooseAlgorithm1Button = tk.Button(onderinMiddenFrame, font='bold', text='BAD algorithm', height=2, width=16,
                                           command=lambda: algorithmConfig(1), bg='red')
        chooseAlgorithm2Button = tk.Button(onderinMiddenFrame, font='bold', text='REGULAR algorithm', height=2,
                                           width=16, command=lambda: algorithmConfig(2), bg='white')
        chooseAlgorithm3Button = tk.Button(onderinMiddenFrame, font='bold', text='GOOD algorithm', height=2, width=16,
                                           command=lambda: algorithmConfig(3), bg='white')

        FeedbackGrid = []
        for row in range(10):
            current_row = []
            for column in range(8):
                f4square = tk.Label(middeninMiddenFrame, text='    ', borderwidth=1, relief=tk.SUNKEN, bg='grey')
                f4square.grid(row=row, column=column)
                current_row.append(f4square)
            FeedbackGrid.append(current_row)

        ColorCodeGrid = []
        for row in range(11):
            current_row = []
            for column in range(4):
                f5square = tk.Label(middeninMiddenFrame, text='    ', borderwidth=5, relief=tk.SUNKEN, bg='grey')
                f5square.grid(row=row, column=column)
                current_row.append(f5square)
            ColorCodeGrid.append(current_row)

        autoFeedbackButtonOff = tk.Button(onderinMiddenFrame, text='off', height=2, width=5,
                                          command=lambda: configAutoFeedback(False), bg='red')
        autoFeedbackButtonOn = tk.Button(onderinMiddenFrame, text='on', height=2, width=5,
                                         command=lambda: configAutoFeedback(True), bg='white')

        # In frame 5 zijn de knoppen te vinden voor het bepalen van de geheime code en de enter button"""
        omschrijvingWerkingButtons = tk.Label(middeninLinksFrame,
                                     text="autofeedback OFF/ON                                  Algoritme BAD/GOOD                              pin1   pin2    pin3    pin4                                                                                ",
                                     font="Arial 14", bg='grey')

        # filmpje hoe command werkt zonder dat hij direct wat uitprint d.m.v. lambda.
        # --> https://www.youtube.com/watch?v=Y6cir7P3YUk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=3 <--"""

        returnToHomepageButton = tk.Button(onderinMiddenFrame, text="Return to mainpage", height=5, width=23,
                                           fg="white",
                                           bg="black",
                                           command=lambda: [controller.showFrame("MainPage"), masterReset()])
        codeSetPin1Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(1), bg='grey')
        codeSetPin2Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(2), bg='grey')
        codeSetPin3Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(3), bg='grey')
        codeSetPin4Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(4), bg='grey')
        enterButton = tk.Button(onderinMiddenFrame, text='ENTER', height=2, width=5, fg='black',
                                command=lambda: enter(), bg='grey')

        statusbar = tk.Label(AIvsPlayer, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        returnToHomepageButton.pack(side=tk.RIGHT, anchor='e')
        uitkomstAlgorithm.pack(side=tk.TOP)

        autoFeedbackButtonOff.pack(side=tk.LEFT, anchor='s', fill=tk.X, padx=10, pady=50)
        autoFeedbackButtonOn.pack(side=tk.LEFT, anchor='s', fill=tk.X, padx=10, pady=50)

        chooseAlgorithm1Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        chooseAlgorithm2Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        chooseAlgorithm3Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)

        omschrijvingWerkingButtons.pack(side=tk.BOTTOM, anchor="w")
        codeSetPin1Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        codeSetPin2Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        codeSetPin3Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        codeSetPin4Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        enterButton.pack(side=tk.LEFT, padx=100, pady=10)
        boveninMiddenFrame.pack(side=tk.TOP, expand=tk.TRUE)
        middeninMiddenFrame.pack(side=tk.TOP, anchor='center', expand=tk.TRUE)
        middeninLinksFrame.pack(side=tk.TOP, anchor='s', expand=tk.TRUE)
        statusbar.pack(side=tk.BOTTOM, anchor='s', fill=tk.BOTH)
        onderinMiddenFrame.pack(side=tk.TOP, anchor='s', expand=tk.TRUE)

        def enter():
            """Bij het drukken op enter wordt alle verzamelde data doorgegeven aan de class Game."""
            if AIvsPlayer.freezeFrame == False:
                if AIvsPlayer.firstTurn == False:
                    AIvsPlayer.row += 1

                if AIvsPlayer.firstTurn:
                    pin1 = AIvsPlayer.changePinTimesClicked['timesClickedPin1']
                    pin2 = AIvsPlayer.changePinTimesClicked['timesClickedPin2']
                    pin3 = AIvsPlayer.changePinTimesClicked['timesClickedPin3']
                    pin4 = AIvsPlayer.changePinTimesClicked['timesClickedPin4']
                    secretCode = '{}{}{}{}'.format(pin1, pin2, pin3, pin4)
                    if AIvsPlayer.opponent == 1:
                        AIvsPlayer.AIopponent = NaiefOpponent()
                    elif AIvsPlayer.opponent == 3:
                        AIvsPlayer.AIopponent = KnuthOpponent()
                    else:
                        AIvsPlayer.AIopponent = []
                    AIvsPlayer.game = Game(secretCode, AIvsPlayer.AIopponent,
                                           AIvsPlayer.opponent)  # self.code is hier de geheime code!
                    AIvsPlayer.firstTurn = False
                else:
                    for item in AIvsPlayer.changePinTimesClicked.values():
                        if item == 1:
                            AIvsPlayer.white += 1
                        if item == 2:
                            AIvsPlayer.black += 1

                inputFeedbackPins = (AIvsPlayer.black, AIvsPlayer.white)

                if str(AIvsPlayer.opponent) == '1':
                    AIvsPlayer.autoFeedback = True
                    autoFeedbackButtonOff.config(bg='white')
                    autoFeedbackButtonOn.config(bg='red')

                if AIvsPlayer.autoFeedback:
                    AIvsPlayer.freezeFrame = True
                    guess = ['empty', 'empty', 'empty', False]
                    if str(AIvsPlayer.opponent) == '1':
                        guess = AIvsPlayer.game.update(inputFeedbackPins,
                                                       AIvsPlayer.autoFeedback)  # self.code is hier het antwoord op de laatste gok
                        uitkomstAlgorithm.config(
                            text="Jouw geheime code is {}, {}, {}, {} geraden in {} beurten!".format(guess[0][0],
                                                                                                     guess[0][1],
                                                                                                     guess[0][2],
                                                                                                     guess[0][3],
                                                                                                     guess[2]))
                    else:
                        while guess[3] == False:
                            guess = AIvsPlayer.game.update(inputFeedbackPins,
                                                           AIvsPlayer.autoFeedback)  # self.code is hier het antwoord op de laatste gok
                            inputFeedbackPins = guess[1]

                            for pin in range(4):
                                ColorCodeGrid[guess[2]][pin].config(bg=guess[0][pin])
                            pinBlackOrWhite = 4
                            for blackPins in range(guess[1][0]):
                                FeedbackGrid[guess[2]][pinBlackOrWhite].config(bg='black')
                                pinBlackOrWhite += 1

                            for whitePins in range(guess[1][1]):
                                FeedbackGrid[guess[2]][pinBlackOrWhite].config(bg='white')
                                pinBlackOrWhite += 1

                            for greyPins in range(8 - pinBlackOrWhite):
                                FeedbackGrid[guess[2]][pinBlackOrWhite].config(bg='grey')
                                pinBlackOrWhite += 1

                        uitkomstAlgorithm.config(text="De AI heeft jouw geheime code geraden!")
                else:
                    guess = AIvsPlayer.game.update(inputFeedbackPins,
                                                   AIvsPlayer.autoFeedback)  # self.code is hier het antwoord op de laatste gok
                    if guess[2] == True:
                        uitkomstAlgorithm.config(text="De AI heeft jouw geheime code geraden!", font="Arial 25 bold")
                    elif guess[1] == True:
                        uitkomstAlgorithm.config(text="Oh oh, je speelt vals, niet weer doen!", font="Arial 25 bold")
                        AIvsPlayer.freezeFrame = True
                    else:
                        for pin in range(4):
                            ColorCodeGrid[AIvsPlayer.row][pin].config(bg=guess[0][pin])
                    setPinsClickedToZero()

        def configAutoFeedback(trueOrFalse):
            """Slaat op of de speler automatische feedback wil geven of handmatig."""
            if AIvsPlayer.firstTurn:
                autoFeedbackButtonOff.config(bg='white')
                autoFeedbackButtonOn.config(bg='white')
                AIvsPlayer.autoFeedback = trueOrFalse
                if trueOrFalse:
                    autoFeedbackButtonOn.config(bg='red')
                elif trueOrFalse == False:
                    autoFeedbackButtonOff.config(bg='red')

        def algorithmConfig(algorithmNumber):
            """Configureert welk algoritme de speler wil gebruiken."""
            if AIvsPlayer.firstTurn:
                chooseAlgorithm1Button.config(bg='white')
                chooseAlgorithm2Button.config(bg='white')
                chooseAlgorithm3Button.config(bg='white')
                AIvsPlayer.opponent = algorithmNumber

                if algorithmNumber == 1:
                    chooseAlgorithm1Button.config(bg='red')
                elif algorithmNumber == 2:
                    chooseAlgorithm2Button.config(bg='red')
                elif algorithmNumber == 3:
                    chooseAlgorithm3Button.config(bg='red')

        def configButton(pinNumber):
            """Configureerd de huidige stand van de knoppen visueel gezien. Bij de eerste beurt zal de secret code geconfigureerd
            en bij de overige beurten configureerd de functie de feedback pinnen (zwart of wit) welke dienen als goed/fout."""
            if AIvsPlayer.firstTurn:
                changeButtonToColor = changeSecretCodeColor(pinNumber)
                if pinNumber == 1:
                    ColorCodeGrid[10][0].config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 2:
                    ColorCodeGrid[10][1].config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 3:
                    ColorCodeGrid[10][2].config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 4:
                    ColorCodeGrid[10][3].config(bg="{}".format(changeButtonToColor))
            else:
                if AIvsPlayer.freezeFrame == False:
                    setFeedbackpins = changeFeedbackPins(pinNumber)
                    if pinNumber == 1:
                        FeedbackGrid[AIvsPlayer.row][4].config(bg="{}".format(setFeedbackpins))
                    elif pinNumber == 2:
                        FeedbackGrid[AIvsPlayer.row][5].config(bg="{}".format(setFeedbackpins))
                    elif pinNumber == 3:
                        FeedbackGrid[AIvsPlayer.row][6].config(bg="{}".format(setFeedbackpins))
                    elif pinNumber == 4:
                        FeedbackGrid[AIvsPlayer.row][7].config(bg="{}".format(setFeedbackpins))

        def changeSecretCodeColor(pinNumber):
            """Configureerd in de back end de secret code van de speler."""
            if AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)] == 6:
                AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)] = 1
            else:
                AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)] += 1
            clicked = AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)]
            colorOfPin = colorCode(clicked)
            return colorOfPin

        def changeFeedbackPins(pinNumber):
            """Configureerd in de back end de zwarte en witte pinnen die de speler teruggeeft aan de AI als feedback."""
            if AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)] == 2:
                AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)] = 0
            else:
                AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)] += 1
            clicked = AIvsPlayer.changePinTimesClicked['timesClickedPin{}'.format(pinNumber)]
            colorOfPin = colorCode(clicked)
            return colorOfPin

        def colorCode(clicked):
            """De algoritmes geven kleuren terug in getallen. Deze functie zet getallen om in kleuren.
            De GUI herkent deze kleuren."""
            if clicked == 0:
                color = 'grey'
            elif clicked == 1:
                color = 'white'
            elif clicked == 2:
                color = 'black'
            elif clicked == 3:
                color = 'yellow'
            elif clicked == 4:
                color = 'red'
            elif clicked == 5:
                color = 'green'
            elif clicked == 6:
                color = 'blue'
            else:
                color = None
                print("colorCode error")
            return color

        def setPinsClickedToZero():
            """Reset alle pinnen, nadat de GUI data heeft doorgespeeld naar een algoritme."""
            AIvsPlayer.changePinTimesClicked = {'timesClickedPin1': 0,
                                                'timesClickedPin2': 0,
                                                'timesClickedPin3': 0,
                                                'timesClickedPin4': 0}
            AIvsPlayer.black = 0
            AIvsPlayer.white = 0

        def masterReset():
            """Start de applicatie opnieuw op, wat ervoor zorgt dat alle data gereset wordt. NOTE: werkt nog niet."""
            python = sys.executable
            os.execl(python, python, *sys.argv)

class PlayervsAI(tk.Frame):
    firstTurn = True
    autoFeedback = False
    freezeFrame = False
    secretCode = ''
    opponent = 1
    row = 0
    black = 0
    white = 0
    changePinTimesClicked = {'timesClickedPin1': 0,
                             'timesClickedPin2': 0,
                             'timesClickedPin3': 0,
                             'timesClickedPin4': 0}

    def __init__(AIvsPlayer, parent, controller):
        """Game waarbij je de code van de AI moet gokken"""

        tk.Frame.__init__(AIvsPlayer, parent, bg="blue")
        AIvsPlayer.controller = controller

        boveninMiddenFrame = tk.Frame(AIvsPlayer, bg="grey", height=200, width=200)
        middeninLinksFrame = tk.Frame(AIvsPlayer, bg="grey", height=200, width=100)
        middeninMiddenFrame = tk.Frame(AIvsPlayer, bg="grey", height=200, width=300)
        onderinMiddenFrame = tk.Frame(AIvsPlayer, bg="grey")

        # in frame 3 is alleen het antwoord van het langste algoritme te vinden."""
        uitkomstAlgorithm = tk.Label(boveninMiddenFrame, text="", bg='grey', font="Arial 18 bold")

        # In frame 4 is een tabel met 4 x 10 buttons te vinden waarin de speler kan aangegeven in hoeverre de pinnen
        # ingevuld door de AI goed zijn."""

        chooseAlgorithm1Button = tk.Button(onderinMiddenFrame, font='bold', text='BAD algorithm', height=2, width=16,
                                           command=lambda: algorithmConfig(1), bg='red')
        chooseAlgorithm2Button = tk.Button(onderinMiddenFrame, font='bold', text='REGULAR algorithm', height=2,
                                           width=16, command=lambda: algorithmConfig(2), bg='white')
        chooseAlgorithm3Button = tk.Button(onderinMiddenFrame, font='bold', text='GOOD algorithm', height=2, width=16,
                                           command=lambda: algorithmConfig(3), bg='white')

        FeedbackGrid = []
        for row in range(10):
            current_row = []
            for column in range(8):
                f4square = tk.Label(middeninMiddenFrame, text='    ', borderwidth=1, relief=tk.SUNKEN, bg='grey')
                f4square.grid(row=row, column=column)
                current_row.append(f4square)
            FeedbackGrid.append(current_row)

        ColorCodeGrid = []
        for row in range(11):
            current_row = []
            for column in range(4):
                f5square = tk.Label(middeninMiddenFrame, text='    ', borderwidth=5, relief=tk.SUNKEN, bg='grey')
                f5square.grid(row=row, column=column)
                current_row.append(f5square)
            ColorCodeGrid.append(current_row)

        autoFeedbackButtonOff = tk.Button(onderinMiddenFrame, text='off', height=2, width=5,
                                          command=lambda: configAutoFeedback(False), bg='red')
        autoFeedbackButtonOn = tk.Button(onderinMiddenFrame, text='on', height=2, width=5,
                                         command=lambda: configAutoFeedback(True), bg='white')

        # In frame 5 zijn de knoppen te vinden voor het bepalen van de geheime code en de enter button"""
        omschrijvingWerkingButtons = tk.Label(middeninLinksFrame,
                                     text="autofeedback OFF/ON                                  Algoritme BAD/GOOD                              pin1   pin2    pin3    pin4                                                                                ",
                                     font="Arial 14", bg='grey')

        # filmpje hoe command werkt zonder dat hij direct wat uitprint d.m.v. lambda.
        # --> https://www.youtube.com/watch?v=Y6cir7P3YUk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=3 <--"""

        returnToHomepageButton = tk.Button(onderinMiddenFrame, text="Return to mainpage", height=5, width=23,
                                           fg="white",
                                           bg="black",
                                           command=lambda: [controller.showFrame("MainPage"), masterReset()])
        codeSetPin1Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(1), bg='grey')
        codeSetPin2Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(2), bg='grey')
        codeSetPin3Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(3), bg='grey')
        codeSetPin4Button = tk.Button(onderinMiddenFrame, height=2, width=5, command=lambda: configButton(4), bg='grey')
        enterButton = tk.Button(onderinMiddenFrame, text='ENTER', height=2, width=5, fg='black',
                                command=lambda: enter(), bg='grey')

        statusbar = tk.Label(AIvsPlayer, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        returnToHomepageButton.pack(side=tk.RIGHT, anchor='e')
        uitkomstAlgorithm.pack(side=tk.TOP)

        autoFeedbackButtonOff.pack(side=tk.LEFT, anchor='s', fill=tk.X, padx=10, pady=50)
        autoFeedbackButtonOn.pack(side=tk.LEFT, anchor='s', fill=tk.X, padx=10, pady=50)

        chooseAlgorithm1Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        chooseAlgorithm2Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        chooseAlgorithm3Button.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)

        omschrijvingWerkingButtons.pack(side=tk.BOTTOM, anchor="w")
        codeSetPin1Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        codeSetPin2Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        codeSetPin3Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        codeSetPin4Button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        enterButton.pack(side=tk.LEFT, padx=100, pady=10)
        boveninMiddenFrame.pack(side=tk.TOP, expand=tk.TRUE)
        middeninMiddenFrame.pack(side=tk.TOP, anchor='center', expand=tk.TRUE)
        middeninLinksFrame.pack(side=tk.TOP, anchor='s', expand=tk.TRUE)
        statusbar.pack(side=tk.BOTTOM, anchor='s', fill=tk.BOTH)
        onderinMiddenFrame.pack(side=tk.TOP, anchor='s', expand=tk.TRUE)

        def enter():
            """Bij het drukken op enter wordt alle verzamelde data doorgegeven aan de class Game."""
            if AIvsPlayer.freezeFrame == False:
                if AIvsPlayer.firstTurn == False:
                    AIvsPlayer.row += 1

                if AIvsPlayer.firstTurn:
                    pin1 = AIvsPlayer.changePinTimesClicked['timesClickedPin1']
                    pin2 = AIvsPlayer.changePinTimesClicked['timesClickedPin2']
                    pin3 = AIvsPlayer.changePinTimesClicked['timesClickedPin3']
                    pin4 = AIvsPlayer.changePinTimesClicked['timesClickedPin4']
    


class SpelUitleg(tk.Frame):
    def __init__(self, parent, controller):
        """Bouwt de GUI op voor de pagina SpelUitleg."""
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller

        wholeScreenFrame = tk.Frame(self, bg="white")
        titelUitlegPagina = tk.Label(wholeScreenFrame, font='Arial 18 bold', bg='white', text='Hoe werkt Mastermind?')
        uitlegSpel = tk.Label(wholeScreenFrame, font='Arial 14', bg='white',
                          text="""Het doel van het spel is om de kleurcode van jouw opponent te achterhalen.\nEen van de
                                  spelers is de codemaker, deze dient een code te maken met vier\ngekleurde pionnen. 
                                  Deze code is alleen zichtbaar voor de codemaker, er kan\ngekozen worden uit zes
                                  verschillende kleuren. De andere speler of spelers mag\nvervolgens proberen om de code
                                  te breken door vier pionnen op de eerste rij te\nplaatsen. De maker van de code moet
                                  vervolgens aangeven of pionnen op de juiste \n positie staan, geen enkele pion goed is
                                  geplaatst of dat de juiste kleuren aanwezig zijn. \n Dit doet hij door middel van
                                  zwarte en witte pinnen in het bord te plaatsen. Vervolgens\nmag de codebreker weer
                                  opnieuw een rij opvullen. De speler die de code binnen het\nminst aantal beurten weet
                                  te raden is de winnaar. """)


        terugNaarHoofdMenu = tk.Button(wholeScreenFrame, text="Terug naar mainpage", height=5, width=23, fg="white", bg="black",
                            command=lambda: controller.showFrame("MainPage"))

        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20, bg="light blue",
                             text="Copyright© Freek Gerrits Jans")

        terugNaarHoofdMenu.pack(side=tk.BOTTOM)
        titelUitlegPagina.pack(side=tk.TOP, fill=tk.X, padx=5)
        uitlegSpel.pack(side=tk.LEFT, anchor='n', fill=tk.X, padx=5)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        wholeScreenFrame.pack(pady=100, expand=tk.TRUE)

if __name__ == "__main__":
    game = GUI()
    game.mainloop()