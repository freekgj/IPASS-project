import tkinter as tk
from AIvsPlayerGame import changeColor, setCode, theCode, setRow, getRow, changeGoodOrBad, colorCode, setGoodOrBad, \
    goodBadClickedFinal, setGoodOrBadToZero, setPinsClicked0
from Algorithm1 import responseAlgorithm1
from Algorithm2 import responseAlgorithm2
from AlgoritmeSelfConstructed import theAlgorithm
from algorithm2TestFase import algorithmIn5Steps

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
        frame = self.frames[pageName]
        frame.tkraise()

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller

        frame1 = tk.Frame(self, bg="white")
        frame2 = tk.Frame(self, bg="white")
        label1 = tk.Label(frame1, text="Welkom bij Artificial Intelligence mastermind!", fg='black', bg="white")
        label1.config(font='Arial 35 bold')
        """wat doet SUNKEN????"""

        photo_image = tk.PhotoImage(file='mastermind.png')
        photo_label = tk.Label(frame1, image=photo_image, width=100, height=290)
        photo_label.image = photo_image

        button1 = tk.Button(frame2, text="start game AI vs player", height=5, width=23, fg="white", bg="black",
                            command=lambda: controller.showFrame("AIvsPlayer"))
        button2 = tk.Button(frame2, text="Uitleg van het spel", height=5, width=23, fg='white', bg='black',
                            command=lambda: controller.showFrame("SpelUitleg"))
        button3 = tk.Button(frame2, text="Exit game", height=5, width=23, fg='white', bg='black', command=frame1.quit)
        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        frame1.pack(pady=0, expand=tk.TRUE)
        frame2.pack(expand=tk.TRUE)
        label1.pack(side=tk.TOP, fill=tk.X)
        photo_label.pack(side=tk.TOP, fill=tk.X)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        button1.pack(side=tk.LEFT, fill=tk.X, padx=5)
        button2.pack(side=tk.LEFT, fill=tk.X, padx=5)
        button3.pack(side=tk.LEFT, fill=tk.X, padx=5)

class AIvsPlayer(tk.Frame):

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

        algorithmButton1 = tk.Button(frame5, font='bold', text='BAD algorithm', height=2, width=16, command=lambda: algorithmConfig(1), bg='red')
        algorithmButton2 = tk.Button(frame5, font='bold', text='REGULAR algorithm', height=2, width=16, command=lambda: algorithmConfig(2), bg='white')
        algorithmButton3 = tk.Button(frame5, font='bold', text='GOOD algorithm', height=2, width=16, command=lambda: algorithmConfig(3), bg='white')

        f4grid = []
        for row in range(10):
            current_row = []
            for column in range(8):
                f4square = tk.Label(frame4, text='    ', borderwidth=1, relief=tk.SUNKEN, bg='grey')
                f4square.grid(row=row, column=column)
                current_row.append(f4square)
            f4grid.append(current_row)

        f4grid[0][1].config(bg="green")

        f5grid = []
        for row in range(10):
            current_row = []
            for column in range(4):
                f5square = tk.Label(frame4, text='    ', borderwidth=5, relief=tk.SUNKEN, bg='grey')
                f5square.grid(row=row, column=column)
                current_row.append(f5square)
            f5grid.append(current_row)

        #f5grid[0][1].config(bg="green")

        """In frame 5 zijn de knoppen te vinden voor het bepalen van de geheime code en de enter button"""
        label2 = tk.Label(frame5, text="Jouw geheime code:", font="Arial 18 bold", fg='black', bg="grey")
        label3 = tk.Label(frame5, text="pin1   pin2    pin3    pin4", padx=10, font="Arial 14", bg='grey')

        """filmpje hoe command werkt zonder dat hij direct wat uitprint d.m.v. lambda.
        --> https://www.youtube.com/watch?v=Y6cir7P3YUk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=3 <--"""

        f5button1 = tk.Button(frame5, height=2, width=5, command=lambda: configBut(1), bg='grey')
        f5button2 = tk.Button(frame5, height=2, width=5, command=lambda: configBut(2), bg='grey')
        f5button3 = tk.Button(frame5, height=2, width=5, command=lambda: configBut(3), bg='grey')
        f5button4 = tk.Button(frame5, height=2, width=5, command=lambda: configBut(4), bg='grey')
        f5button5 = tk.Button(frame5, text='ENTER', height=2, width=5, fg='black', command=lambda: configEnter(), bg='grey')

        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        uitkomstAlgorithm.pack(side=tk.TOP)
        frame3.pack(side=tk.TOP,  expand=tk.TRUE)

        algorithmButton1.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        algorithmButton2.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        algorithmButton3.pack(side=tk.LEFT, anchor='w', fill=tk.X, padx=5, pady=5)
        frame4.pack(side=tk.TOP, expand=tk.FALSE)

        label2.pack(side=tk.TOP, anchor="w", padx=0, pady=0)
        label3.pack(side=tk.TOP, anchor="w", padx=0, pady=0)
        f5button1.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        f5button2.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=0)
        f5button3.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        f5button4.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=10)
        f5button5.pack(side=tk.LEFT, padx=100, pady=10)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        frame5.pack(side=tk.TOP, anchor='s', expand=tk.TRUE)

        def algorithmConfig(algorithmNumber):
            if theCode['codeSet'] == False:
                algorithmButton1.config(bg='white')
                algorithmButton2.config(bg='white')
                algorithmButton3.config(bg='white')
                theCode['setAlgorithm'] = algorithmNumber

                if algorithmNumber == 1:
                    algorithmButton1.config(bg='red')
                elif algorithmNumber == 2:
                    algorithmButton2.config(bg='red')
                elif algorithmNumber == 3:
                    algorithmButton3.config(bg='red')

        def configBut(pinNumber):
            if theCode['codeSet'] == False:
                changeButtonToColor = changeColor(pinNumber)
                if pinNumber == 1:
                    f5button1.config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 2:
                    f5button2.config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 3:
                    f5button3.config(bg="{}".format(changeButtonToColor))
                elif pinNumber == 4:
                    f5button4.config(bg="{}".format(changeButtonToColor))

            else:
                blackWhiteBlanco = changeGoodOrBad(pinNumber)
                if pinNumber == 1:
                    print("getRow:", getRow())
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
            finalState = goodBadClickedFinal['black']
            setPinsClicked0()
            if finalState == 4:
                uitkomstAlgorithm.config(text="""The AI have guessed the game!""", font="Arial 25 bold")
                theCode['gameWon'] = True
                return

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
                print("goodbad:", goodBadClickedFinal)
                for item in responseAI2X[0]:
                    colorResponseAI2X.append(colorCode(item))
                for pin in range(4):
                    f5grid[getRow()][pin].config(bg='{}'.format(colorResponseAI2X[pin]))

                possibleCodesLeft = responseAI2X[1]

                lastGuessInt = [responseAI2X[0][0], responseAI2X[0][1], responseAI2X[0][2], responseAI2X[0][3]]
                lastGuess = ""
                for item in lastGuessInt:
                    lastGuess += str(item)

            setGoodOrBadToZero()
            theCode['firstRound'] = False

class SpelUitleg(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller

        frame6 = tk.Frame(self, bg="white")
        label3 = tk.Label(frame6, font='Arial 18 bold', bg='white', text='Hoe werkt Mastermind?')
        label4 = tk.Label(frame6, font='Arial 14', bg='white', text="""Het doel van het spel is om de kleurcode van jouw opponent te achterhalen.\nEen van de spelers is de codemaker, deze dient een code te maken met vier\ngekleurde pionnen. Deze code is alleen zichtbaar voor de codemaker, er kan\ngekozen worden uit zes verschillende kleuren. De andere speler of spelers mag\nvervolgens proberen om de code te breken door vier pionnen op de eerste rij te\nplaatsen. De maker van de code moet vervolgens aangeven of pionnen op de juiste \n positie staan, geen enkele pion goed is geplaatst of dat de juiste kleuren aanwezig zijn. \n Dit doet hij door middel van zwarte en witte pinnen in het bord te plaatsen. Vervolgens\nmag de codebreker weer opnieuw een rij opvullen. De speler die de code binnen het\nminst aantal beurten weet te raden is de winnaar. """)
        statusbar = tk.Label(self, bd=1, relief=tk.SUNKEN, padx=10, pady=20,
                             bg="light blue", text="Copyright© Freek Gerrits Jans")

        label3.pack(side=tk.TOP, fill=tk.X, padx=5)
        label4.pack(side=tk.LEFT, anchor='n', fill=tk.X, padx=5)
        frame6.pack(pady=100, expand=tk.TRUE)
        statusbar.pack(side=tk.BOTTOM, fill=tk.BOTH)

if __name__ == "__main__":
    game = Program()
    game.mainloop()