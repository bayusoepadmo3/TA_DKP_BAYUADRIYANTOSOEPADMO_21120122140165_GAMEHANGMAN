'''
Simple Python Hangman Game Using Tkinter
'''

import csv
from datetime import datetime
import os
import random
import tkinter
from tkinter import NSEW, messagebox
from tkinter import ttk
from tkinter import BOTH
from typing import Dict, List


class App:
    '''
    Class Application for Hangman Game
    '''

    def __init__(self, words: Dict[str, List[str]], column: int, images: List[str], icon: str, filename: str) -> None:
        '''
        Constructor for App class

        Parameters
        ----------
        data : dict
            dictionary of words for each difficulty

        column : int
            max number of column

        images : List[str]
            list of path to hangman images

        icon : str
            path to icon

        filename : str
            path to csv file
        '''

        # set attributes
        self.words = words
        self.column = column
        self.levels = list(words.keys())
        self.filename = filename

        # Create the main window
        self.window = tkinter.Tk()
        self.window.title('Hangman')
        self.window.minsize(width=400, height=200)
        self.window.resizable(False, False)

        # setting icon
        self.window.iconbitmap(icon)

        # list of hangman images
        self.images = [tkinter.PhotoImage(file=path) for path in images]

        # create main frame
        self.frame = ttk.Frame(self.window)
        self.frame.pack()

        # set variables for the game
        self.word = None
        self.guessed = None
        self.canvas = None

        self.player = None
        self.difficulty = None
        self.wrong = 0
        self.score = 0
        self.hint = 0

    def run(self) -> None:
        '''
        Function to run the app
        '''

        # change to default screen
        self.menu_screen()

        # run the main loop
        self.window.mainloop()

    def menu_screen(self) -> None:
        '''
        Menu screen, to choose difficulty
        '''

        # create frame
        self.frame.destroy()
        self.frame = ttk.Frame(self.window)

        # set padding for frame
        self.frame.propagate(False)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # create header label
        header = ttk.Label(self.frame, text='Welcome To Hangman!', font=('Open Sans', 13, 'bold'))
        header.grid(row=0, column=0, sticky=NSEW, columnspan=2, padx=10, pady=(0, 20))

        # crate label to choose difficulty
        ttk.Label(self.frame, text='Choose Difficulty').grid(row=1, column=0, sticky=NSEW, padx=10, pady=(0, 10))

        # create button for each difficulty
        for index, level in enumerate(self.levels):
            button = ttk.Button(self.frame, text=level, command=lambda key=level: self.player_screen(key), width=60)
            button.grid(row=2 + index, column=0, sticky=NSEW, padx=10, pady=(0, 5), ipadx=10, ipady=5)

        # create button for score
        score = ttk.Button(self.frame, text='score', command=self.score_screen, width=60)
        score.grid(row=2 + len(self.words), column=0, sticky=NSEW, padx=10, pady=(0, 5), ipadx=10, ipady=5)

        # exit button
        back = ttk.Button(self.frame, text='exit', command=self.window.destroy, width=60)
        back.grid(row=3 + len(self.words), column=0, sticky=NSEW, padx=10, pady=(0, 10), ipadx=5, ipady=5)

    def score_screen(self) -> None:
        '''
        Function to display score
        '''

        # create frame
        self.frame.destroy()
        self.frame = ttk.Frame(self.window)

        # set padding for frame
        self.frame.propagate(False)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # create header label
        header = ttk.Label(self.frame, text='Score', font=('Open Sans', 13, 'bold'))
        header.grid(row=0, column=0, sticky=NSEW, columnspan=2, padx=10, pady=(0, 20))

        # show data in a treeview
        tree = ttk.Treeview(self.frame, columns=('Player', 'Score', 'Difficulty', 'Date'), show='headings')
        tree.heading('Player', text='Player')
        tree.heading('Score', text='Score')
        tree.heading('Difficulty', text='Difficulty')
        tree.heading('Date', text='Date')

        # read data from csv file
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)

        # sort data by score
        data.sort(key=lambda line: int(line[1]), reverse=True)

        # insert data to treeview
        for row in data:
            tree.insert('', 'end', values=row)

        # place treeview on the frame
        tree.grid(row=1, column=0, sticky=NSEW, columnspan=2, padx=10, pady=(0, 20))

        # change column width
        tree.column('Player', width=100, anchor='center')
        tree.column('Score', width=80, anchor='center')
        tree.column('Difficulty', width=100, anchor='center')
        tree.column('Date', width=150, anchor='center')

        # set tree to be scrollable
        scroll = ttk.Scrollbar(self.frame, orient='vertical', command=tree.yview)
        scroll.grid(row=1, column=2, sticky=NSEW, pady=(0, 20))
        tree.configure(yscrollcommand=scroll.set)

        # back button on the left top of frame
        back = ttk.Button(self.frame, text='back', command=self.menu_screen, width=80)
        back.grid(row=2, column=0, sticky=NSEW, padx=10, pady=(0, 20), ipadx=5, ipady=5)

    def player_screen(self, difficulty: str) -> None:
        '''
        Function to display input for player name, if set and valid go to game screen
        '''

        # reset game variables
        self.word = None
        self.guessed = None
        self.canvas = None

        self.player = None
        self.difficulty = difficulty
        self.wrong = 0
        self.score = 0
        self.hint = 3

        # create frame
        self.frame.destroy()
        self.frame = ttk.Frame(self.window)

        # set padding for frame
        self.frame.propagate(False)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # create header label
        header = ttk.Label(self.frame, text='Input Player Name', font=('Open Sans', 13, 'bold'))
        header.grid(row=0, column=0, sticky=NSEW, columnspan=2, padx=10, pady=(0, 20))

        # crate label to choose difficulty
        ttk.Label(self.frame, text='Player Name').grid(row=1, column=0, sticky=NSEW, padx=10, pady=(0, 10))

        # create entry for player name
        player_entry = ttk.Entry(self.frame, width=60)
        player_entry.grid(row=2, column=0, sticky=NSEW, padx=10, pady=10, ipadx=10, ipady=5)

        # create button to start the game
        start = ttk.Button(self.frame, text='start', command=lambda: self.validate_name(player_entry.get()), width=60)
        start.grid(row=3, column=0, sticky=NSEW, padx=10, pady=(0, 5), ipadx=10, ipady=5)

        # add button to back to menu screen
        back = ttk.Button(self.frame, text='back', command=self.menu_screen, width=60)
        back.grid(row=4, column=0, sticky=NSEW, padx=10, pady=(0, 10), ipadx=5, ipady=5)

    def validate_name(self, player: str) -> None:
        '''
        Function to check if player name is valid, if valid go to game screen

        Parameters
        ----------
        player : str
            player name
        '''

        # check if player name is valid
        if player == '':
            messagebox.showinfo('Error', 'Player Name cannot be empty', parent=self.window)
            return

        # check if player name is more than 20 characters
        if len(player) <= 3:
            messagebox.showinfo('Error', 'Player Name cannot be more than 3 characters', parent=self.window)
            return

        # set player name
        self.player = player
        self.game_screen()

    def game_screen(self) -> None:
        '''
        Function to play the game
        '''
        # create frame
        self.frame.destroy()
        self.frame = ttk.Frame(self.window)

        # set padding for frame
        self.frame.propagate(False)
        self.frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # get random word from dictionary
        self.word = random.choice(self.words[self.difficulty]).lower()

        # create a set to store guessed letters
        self.guessed = set()

        # create header label in left top of frame
        header = ttk.Label(self.frame, text='Play Hangman!', font=('Open Sans', 13, 'bold'))
        header.grid(row=0, column=0, sticky=NSEW, padx=10, pady=(0, 20))

        # back button on the left top of frame
        back = ttk.Button(self.frame, text='back', command=self.menu_screen, width=3)
        back.grid(row=0, column=self.column - 1, sticky=NSEW, padx=10, pady=(0, 20), ipadx=5, ipady=5)

        # create a canvas to draw hangman
        self.canvas = tkinter.Canvas(self.frame, width=400, height=300, background='white')
        self.canvas.grid(row=1, column=0, sticky=NSEW, columnspan=self.column, padx=10, pady=(0, 10))

        # draw hangman image in canvass
        self.render_hangman()

        # create a empry button to show the word
        self.render_word(gridrow=2)

        # create keyboards button with qwerty layout
        self.render_keyboard(gridrow=3)

    def render_keyboard(self, gridrow: int) -> None:
        '''
        Function to render keyboard button, and place it on the frame

        Parameters
        ----------
        gridrow : int
            row position of the frame
        '''

        # initialize layout position for each line and keys
        keyboard = [ttk.Frame(self.frame) for _ in range(3)]
        keys = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

        # place keyboard on the frame
        for index, line in enumerate(keyboard):
            line.grid(row=index + gridrow, column=0, columnspan=self.column, padx=10)

        # place keys on the keyboard
        for index, line in enumerate(keyboard):
            for row, letter in enumerate(keys[index]):

                # check if the letter is in the word
                if letter in self.guessed:
                    button = ttk.Button(line, text=letter, state='disabled', width=2)
                else:
                    button = ttk.Button(line, text=letter, command=lambda letter=letter: self.handle_guess(letter), width=2)

                # set grid position for each button
                button.grid(row=0, column=row, padx=1, pady=2 if index < 2 else (2, 10), ipadx=8, ipady=5)

    def render_word(self, gridrow: int) -> None:
        '''
        Function to render the word to be guessed

        Parameters
        ----------
        gridrow : int
            row position of the frame
        '''

        # initialize layout position
        placeholder = ttk.Frame(self.frame)
        placeholder.grid(row=gridrow, column=0, columnspan=self.column, padx=10, pady=(0, 10))

        # place placeholder on the frame
        for index, letter in enumerate(self.word):

            # check if the letter is in the word
            if letter in self.guessed:
                button = ttk.Button(placeholder, text=letter, width=2)
            else:
                button = ttk.Button(placeholder, text='_', command=lambda letter=letter: self.handle_hint(letter), width=2)

            # set grid position for each button
            button.grid(row=0, column=index, padx=1, pady=2, ipadx=8, ipady=5)

    def render_hangman(self) -> None:
        '''
        Function to draw hangman image

        Parameters
        ----------
        canvas : tkinter.Canvas
            canvas to draw the image of hangman
        '''

        # draw image based on the number of wrong guesses
        self.canvas.create_image(200, 150, image=self.images[self.wrong])

    def count_score(self) -> int:
        '''
        Function to count the score

        - Each correct guess will add 100 points to the score
        - Each hint will reduce 50 points from the score
        - Each wrong guess will reduce 50 points from the score
        '''

        # count score
        return

    def check_status(self) -> bool:
        '''
        Function to check if the game is won
        '''

        # check if every letter in the word is guessed
        if all(letter in self.guessed for letter in self.word):

            # get current time
            now = datetime.now()
            now = now.strftime('%d/%m/%Y %H:%M:%S')

            # store data to csv file with csv module
            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    self.player,
                    self.count_score(),
                    self.difficulty.capitalize(),
                    now
                ])

            # return true
            return True

        # return false if the game is not won
        return False

    def check_gameover(self) -> bool:
        '''
        Function to check if the game is over
        '''

        # check if the number of wrong guesses is equal to the number of hangman images
        if self.wrong == len(self.images) - 1:

            # get current time
            now = datetime.now()
            now = now.strftime('%d/%m/%Y %H:%M:%S')

            # store data to csv file with csv module
            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([self.player, self.count_score(), now])

            # return true
            return True

        # return false if the game is not over
        return False

    def handle_guess(self, letter: str) -> None:
        '''
        Function to handle the guess

        Parameters
        ----------
        letter : str
            letter to be guessed
        '''

        # add letter to guessed set
        self.guessed.add(letter)
        self.render_keyboard(gridrow=3)

        # check if letter is in the word
        if letter not in self.word:
            self.wrong += 1
            self.render_hangman()
        else:
            # check how many times the letter is in the word, add it to score
            self.score += self.word.count(letter)
            self.render_word(gridrow=2)

        # check if the game is over
        if self.check_gameover():
            messagebox.showinfo('Game Over', 'Too bad, you lose', parent=self.window)
            self.menu_screen()

        # check if the game is won
        if self.check_status():
            messagebox.showinfo('Congratulation', 'Congratulation You Win!', parent=self.window)
            self.menu_screen()

    def handle_hint(self, letter: str) -> None:
        '''
        Function to handle the hint

        Parameters
        ----------
        letter : str
            letter to be guessed
        '''

        # if hint is 0, show message
        if self.hint == 0:
            messagebox.showinfo('Hint', 'You have no hint left', parent=self.window)
            return

        # add letter to guessed set
        self.hint -= 1
        self.guessed.add(letter)
        self.render_keyboard(gridrow=3)

        # render word
        self.render_word(gridrow=2)

        # show number of hint message
        messagebox.showinfo('Hint', 'You have %d hint(s) left' % self.hint, parent=self.window)

        # check if the game is won
        if self.check_status():
            messagebox.showinfo('Congratulation', 'Congratulation You Win!', parent=self.window)
            self.menu_screen()


# set difficulties
DIFFICULTIES = ['easy', 'medium', 'hard']


def main() -> None:
    '''
    Main function to run the app
    '''

    # set folder
    directory = os.getcwd()
    data = 'data'
    assets = 'assets'

    # read data from txt file
    words = {}
    for difficulty in DIFFICULTIES:
        with open(os.path.join(directory, data, '%s.txt' % difficulty), 'r', encoding='utf-8') as file:
            words[difficulty] = file.read().splitlines()

    # set max number of column
    column = max([len(word) for words in words.values() for word in words])

    # set images
    images = [os.path.join(directory, assets, 'hangman-%d.png' % index) for index in range(1, 12)]

    # set icon
    icon = os.path.join(directory, assets, 'icon.ico')

    # set csv filename
    filename = os.path.join(directory, data, 'score.csv')

    # create app
    app = App(words, column, images, icon, filename)

    # run app
    app.run()


if __name__ == '__main__':
    main()
