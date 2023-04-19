"""
File: Wordy.py
Authors: 
Kaelan Anderson - kaelananderson24@gmail.com
Date: 5/19/2022
"""

# Imports
import random
import tkinter as tk
import tkinter.font as font
from enum import Enum
import time

class Wordy:
    def __init__(self):
        """ Initialize the game """
        # Constants
        self.WORD_SIZE = 5  # number of letters in the hidden word
        self.NUM_GUESSES = 6 # number of guesses that the user gets 
        self.LONG_WORDLIST_FILENAME = "long_wordlist.txt"
        self.SHORT_WORDLIST_FILENAME = "short_wordlist.txt"

        # Size of the frame that holds all guesses.  This is the upper left
        # frame in the window.
        self.PARENT_GUESS_FRAME_WIDTH = 750
        self.PARENT_GUESS_FRAME_HEIGHT = 500

        # Parameters for an individual letter in the guess frame
        # A guess frame is an individual box that contains a guessed letter.
        self.GUESS_FRAME_SIZE = 50  # the width and height of the guess box.
        self.GUESS_FRAME_PADDING = 3 
        self.GUESS_FRAME_BG_BEGIN = 'white' # background color of a guess box 
                                            # after the user enters the letter,
                                            # but before the guess is entered.
        self.GUESS_FRAME_TEXT_BEGIN = 'black' # color of text in guess box after the
                                            # user enters the letter, but before
                                            # the guess is entered.
        self.GUESS_FRAME_BG_WRONG = 'grey'  # background color of guess box
                                            # after the guess is entered, and the
                                            # letter is not in the hidden word.
        self.GUESS_FRAME_BG_CORRECT_WRONG_LOC = 'orange' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # but in the wrong location.
        self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC = 'green' # background color
                                            # guess box after the guess is entered
                                            # and the letter is in the hidden word
                                            # and in the correct location.
        self.GUESS_FRAME_TEXT_AFTER = 'white' # color of text in guess box after
                                            # the guess is entered.
        self.FONT_FAMILY = 'ariel'          # Font to use for letters in the guess boxes.
        self.FONT_SIZE_GUESS = 33           # Font size for letters in the guess boxes.

        # Parameters for the keyboard frame
        self.KEYBOARD_FRAME_HEIGHT = 200
        self.KEYBOARD_BUTTON_HEIGHT = 2
        self.KEYBOARD_BUTTON_WIDTH = 3  # width of the letter buttons.  Remember,
                                        # width of buttons is measured in characters.
        self.KEYBOARD_BUTTON_WIDTH_LONG = 5 # width of the enter and back buttons.

        # The following colors for the keyboard buttons
        # follow the same specifications as the colors defined above for the guess
        # boxes.  The problem is that if one or both of you have a mac, you will
        # not be able to change the background color of a button.  In this case,
        # just change the color of the text in the button, instead of the background color.
        # So the text color starts as the default (black), and then changes to grey, orange, 
        # green depending on the result of the guess for that letter.
        self.KEYBOARD_BUTTON_BG_BEGIN = 'white' 
        self.KEYBOARD_BUTTON_TEXT_BEGIN = 'black' 
        self.KEYBOARD_BUTTON_BG_WRONG = 'grey'  
        self.KEYBOARD_BUTTON_BG_CORRECT_WRONG_LOC = 'orange' 
        self.KEYBOARD_BUTTON_BG_CORRECT_RIGHT_LOC = 'green' 
        self.KEYBOARD_BUTTON_TEXT_AFTER = 'white' 

        self.KEYBOARD_BUTTON_NAMES = [   
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "BACK"]]
        
        # Parameters for the control frame
        self.CONTROL_FRAME_HEIGHT = self.PARENT_GUESS_FRAME_HEIGHT + self.KEYBOARD_FRAME_HEIGHT
        self.CONTROL_FRAME_WIDTH = 300
        self.USER_SELECTION_PADDING = 10  # Horizontal padding on either side of the widgets in
                                            # the parameter frame.

        self.MESSAGE_DISPLAY_TIME_SECS = 5 # Length of time the message should be
                                            # displayed.
        self.PROCESS_GUESS_WAITTIME = 1  # When processing a guess (changing color
                                        # of the guess frames), time to wait between
                                        # updating successive frames.

        # Create window
        self.window = tk.Tk()
        self.window.title("Wordy")

        # Create guess fram
        self.guess_frame = tk.Frame(self.window, width=self.PARENT_GUESS_FRAME_WIDTH,
                        height=self.PARENT_GUESS_FRAME_HEIGHT, borderwidth=1, relief='solid')
        self.guess_frame.grid(row=1, column=1)
        self.guess_frame.grid_propagate(False)

        # Create keyboard frame
        self.keyboard_frame = tk.Frame(self.window, width=self.PARENT_GUESS_FRAME_WIDTH, 
                        height= self.KEYBOARD_FRAME_HEIGHT, borderwidth=1, relief='solid')
        self.keyboard_frame.grid(row=2, column=1 )
        self.keyboard_frame.grid_propagate(False)

        # Create control frame
        self.control_frame = tk.Frame(self.window, width= self.CONTROL_FRAME_WIDTH, 
                        height= self.CONTROL_FRAME_HEIGHT, borderwidth=1, relief = 'solid')
        self.control_frame.grid(row=1, column=2, rowspan=2)
        self.control_frame.grid_propagate(False)

        self.button_dict = {}
        self.FONT = font.Font(family=self.FONT_FAMILY, size= self.FONT_SIZE_GUESS)
        self.PADDING = 10 # Padding around widgets
        self.ENTRY_SIZE = 10 # Size of entry widget

        # Call methods to create the other frames within control frame
        self.message_frame()
        self.parameters()
        self.buttons()
        self.letter_frames()
        self.keyboard_first_row()
        self.keyboard_second_row()
        self.keyboard_third_row()

        # initialize the short and long word lists
        self.short_word_list = []
        self.long_word_list = []

        # initialize timer
        self.timer = None        

        # initialize hidden word as empty string
        self.hidden_word = ''
        
        # Start event loop
        self.window.mainloop()

    def message_frame(self):
        """ Creates the message frame and label and centers the message. """

        # Create message frame
        self.message_f = tk.Frame(self.control_frame, width= self.CONTROL_FRAME_WIDTH, 
                        height=self.CONTROL_FRAME_HEIGHT/3, borderwidth=1, relief='solid')
        self.message_f.grid(row=1, column=1)
        self.message_f.grid_propagate(False)

        # Create message label
        self.message_var = tk.StringVar()
        self.message = tk.Label(self.message_f, textvariable=self.message_var)
        self.message.grid(row=1, column=1)

        # Center column 1 in the frame.
        self.message_f.grid_columnconfigure(1, weight = 1)

        # Center (row wise) the message.
        self.message_f.grid_rowconfigure(0, weight = 1)
        self.message_f.grid_rowconfigure(1, weight = 0)
        self.message_f.grid_rowconfigure(2, weight = 1)

    def parameters(self):
        """ Creates the parameter frame and all its widgets and centers them. """

        # Create parameter frame
        self.parameter_frame = tk.Frame(self.control_frame, width=self.CONTROL_FRAME_WIDTH, 
                        height=self.CONTROL_FRAME_HEIGHT/3, borderwidth=1, relief='solid')
        self.parameter_frame.grid(row=2, column=1)
        self.parameter_frame.grid_propagate(False)

        # Create hard mode checkbox
        self.hard_mode_var = tk.BooleanVar()
        self.hard_mode_var.set(False)
        self.hard_mode = tk.Checkbutton(self.parameter_frame, text="Hard Mode", 
                            var = self.hard_mode_var)
        self.hard_mode.grid(row = 1, column = 1, sticky = tk.W, padx= self.USER_SELECTION_PADDING)

        # Create guesses must be words checkbox
        self.be_words_var = tk.BooleanVar()
        self.be_words_var.set(True)
        self.be_words = tk.Checkbutton(self.parameter_frame, text="Guesses must be words", 
                            var = self.be_words_var)
        self.be_words.grid(row = 2, column = 1, sticky = tk.W, padx= self.USER_SELECTION_PADDING)

        # Creates show word checkbox
        self.show_word_var = tk.BooleanVar()
        self.show_word_var.set(False)
        self.show_word = tk.Checkbutton(self.parameter_frame, text="Show word", 
                            var = self.show_word_var, command=self.show_word_handler)
        self.show_word.grid(row = 3, column = 1, sticky = tk.W, padx= self.USER_SELECTION_PADDING)

        # Creates the specify word checkbox
        self.specify_word_var = tk.BooleanVar()
        self.specify_word_var.set(False)
        self.specify_word = tk.Checkbutton(self.parameter_frame, text="Specify Word", 
                            var = self.specify_word_var)
        self.specify_word.grid(row = 4, column = 1, sticky = tk.W, padx= self.USER_SELECTION_PADDING)

        # Creates the specify word entry field
        self.specify_entry_var = tk.StringVar()
        self.specify_entry = tk.Entry(self.parameter_frame, textvariable=self.specify_entry_var, width = 5)
        self.specify_entry.grid(row = 4, column=2, padx = self.USER_SELECTION_PADDING)

        # Creates the show show word label
        self.show_word_label_var = tk.StringVar()
        self.show_word_label = tk.Label(self.parameter_frame, textvariable=self.show_word_label_var)
        self.show_word_label.grid(row=3, column=2, padx=self.USER_SELECTION_PADDING)

        # Center the widgets in the frame
        self.parameter_frame.grid_columnconfigure(1, weight = 1)
        self.parameter_frame.grid_rowconfigure(0, weight = 1)
        self.parameter_frame.grid_rowconfigure(5, weight = 1)

    def buttons(self):
        """ Creates the button frame and the start and and quit buttons. """

        # Create the button frame
        self.button_frame = tk.Frame(self.control_frame, width=self.CONTROL_FRAME_WIDTH, 
                        height=self.CONTROL_FRAME_HEIGHT/3, borderwidth=1, relief='solid')
        self.button_frame.grid(row=3, column=1)
        self.button_frame.grid_propagate(False)

        # Create the start button
        self.start_button  = tk.Button(self.button_frame, text = "Start Game", command = self.start_button_handler)
        self.start_button.grid(row = 1, column=1)
    
        # Creats the quit button
        self.quit_button = tk.Button(self.button_frame, text="Quit", command= self.quit_button_handler)
        self.quit_button.grid(row=1, column=2)

        # Centers the buttons in the frame
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)
        self.button_frame.grid_rowconfigure(1, weight=1)

    def start_button_handler(self):
        """ Handles the parameters when game is started. """

        # Get the short and long word lists
        self.word_lists()

        # Clear letter frames
        self.letter_frames()
        
        if self.specify_word_var.get() == False:
            # Selects random word from short list if word is not specified
            self.hidden_word = random.choice(self.short_word_list)
        
        else:
            # Sets word to specified word
            self.hidden_word = self.specify_entry_var.get()

            # Checks if the word is correct length
            if len(self.hidden_word) != self.WORD_SIZE:
                self.show_message("Incorrect specified word length")
                return

            # Checks if the word is in the long word list 
            if self.hidden_word not in self.long_word_list and self.be_words_var.get() == True:
                self.show_message("Specified word is not a valid word")
                return
            

            # Removes word from the entry field if all above correct
            self.specify_entry.delete(0, 'end')

        self.show_word_handler()

        if self.be_words_var.get() == True:
            # Guesses have to be words in long word list
            pass

        # Disable checkboxes when game is started
        self.hard_mode['state'] = 'disabled'
        self.be_words['state'] = 'disabled'
        self.specify_word['state'] = 'disabled'
        
        # Calls the method to print the parameter options selected
        self.parameter_options_display()

    def parameter_options_display(self):
        """ Prints out all of the options of the parameters and the hidden word. """

        print("Hard mode = " + str(self.hard_mode_var.get()))
        print("Guesses must be words = " + str(self.be_words_var.get()))
        print("Show word = " + str(self.show_word_var.get()))
        print("Specify word = " + str(self.specify_word_var.get()))
        print("Hidden word = " + self.hidden_word) 

    def quit_button_handler(self):
        """ Quits the window. """
        self.window.destroy()

    def word_lists(self):
        """ Implements the short and long word lists from the given files. """
    
        # Append all words from short word file to short word list
        short_file = open(self.SHORT_WORDLIST_FILENAME , 'r')
        for word in short_file:
            word = word.strip()
            if len(word) == self.WORD_SIZE:
                self.short_word_list.append(word)

        # Append all words from the long word file to long word file
        long_file = open(self.LONG_WORDLIST_FILENAME, 'r')
        for word in long_file:
            word = word.strip()
            if len(word) == self.WORD_SIZE:
                self.long_word_list.append(word)

    def show_message(self, message):
        """
        Displays the message for specified amount of time
        """
        self.message_var.set(message)
        # Set time to clear message after amount of time
        self.timer = self.window.after(self.MESSAGE_DISPLAY_TIME_SECS*1000, self.clear_message)

    def clear_message(self):
        """
        Clears the message frame
        """
        # Reset message to empty
        self.message_var.set('')

    def show_word_handler(self):
        """ Shows the word if show word is checked and dissappears if not. """
        if self.show_word_var.get() == True and self.hidden_word != '':
            # Display the hidden word if show word is checked
            self.show_word_label_var.set(self.hidden_word)
        else:
            self.show_word_label_var.set('')

    def letter_frames(self):
        """ 
        Creates a grid of frames for the letters to go in 
        """
        
        self.letter_box_list = []
        self.current_guess = {"row":0, "col":0}
        self.letter_frame_list = []
        self.guessed_letters_list = []

        # Create the grid of guess box frames
        for r in range(1,self.NUM_GUESSES+1):
            self.letter_box_list.append([])
            self.letter_frame_list.append([])

            for c in range(1,self.WORD_SIZE+1):
                self.letter_box = tk.Frame(self.guess_frame, width=self.GUESS_FRAME_SIZE, 
                                height= self.GUESS_FRAME_SIZE, borderwidth = 0.5, relief= 'solid')
                self.letter_box.grid(row=r, column=c, padx= self.GUESS_FRAME_PADDING, pady= self.GUESS_FRAME_PADDING)
                self.letter_box.grid_propagate(False)

                self.letter_label = tk.Label(self.letter_box, text="", font=(self.FONT_FAMILY, self.FONT_SIZE_GUESS))
                self.letter_label.grid(row=1, column=1)
                self.letter_box_list[r-1].append(self.letter_label)
                self.letter_frame_list[r-1].append(self.letter_box)

                # Center guess box
                self.letter_box.grid_rowconfigure(0, weight=1)
                self.letter_box.grid_rowconfigure(2, weight=1)
                self.letter_box.grid_columnconfigure(0, weight=1)
                self.letter_box.grid_columnconfigure(2, weight=1)

        # Center the guess box frames in the guess frame
        self.guess_frame.grid_rowconfigure(0, weight=1)
        self.guess_frame.grid_rowconfigure(self.NUM_GUESSES+2, weight=1)
        self.guess_frame.grid_columnconfigure(0, weight=1)
        self.guess_frame.grid_columnconfigure(self.WORD_SIZE+2, weight=1)

    def keyboard_first_row(self):
        """
        Creates first row of buttons for the keyboard
        """
    

        # Creates the frame for the first row
        self.top_row_letters = tk.Frame(self.keyboard_frame, width=self.PARENT_GUESS_FRAME_WIDTH,
                                        height=self.KEYBOARD_FRAME_HEIGHT // 3)
        self.top_row_letters.grid(row=1, column=1)
        self.top_row_letters.grid_propagate(False)

        # First line of letters of keyboard
        for c in range(len(self.KEYBOARD_BUTTON_NAMES[0])):

            # Defines a handler for the buttons
            def handler(key=self.KEYBOARD_BUTTON_NAMES[0][c]):
                self.keyboard_button_handler(key)

            # Create the button objects
            button = tk.Button(self.top_row_letters,
                            width=self.KEYBOARD_BUTTON_WIDTH,  
                            height=self.KEYBOARD_BUTTON_HEIGHT,  
                            text=self.KEYBOARD_BUTTON_NAMES[0][c],
                            fg=self.KEYBOARD_BUTTON_TEXT_BEGIN,
                            command=handler)
            button.grid(row=1, column=c + 1, padx=self.PADDING // 2)

            # Put the button in a dictionary of buttons
            # where the key is the button text, and the
            # value is the button object.
            self.button_dict[self.KEYBOARD_BUTTON_NAMES[0][c]] = button

            # Center the keys in the frame
            self.top_row_letters.grid_columnconfigure(c + 1, weight=1)  # Updated column configure to match the loop index
            self.top_row_letters.grid_rowconfigure(1, weight=1)  # Updated row configure to match the row number



    def keyboard_second_row(self):
        """
        Creates the second row of buttons for the keyboard
        """

        # Create the frame to put the second row of keys in
        self.mid_row_letters = tk.Frame(self.keyboard_frame, width=self.PARENT_GUESS_FRAME_WIDTH, 
                        height= self.KEYBOARD_FRAME_HEIGHT//3)
        self.mid_row_letters.grid(row=2, column=1)
        self.mid_row_letters.grid_propagate(False)

        # Second Line of letters in the keyboard
        for c in range(len(self.KEYBOARD_BUTTON_NAMES[1])):               
            
            # Defines a handler for the buttons
            def handler(key = self.KEYBOARD_BUTTON_NAMES[1][c]):
                self.keyboard_button_handler(key)
            
            # Create the button objects
            button = tk.Button(self.mid_row_letters,
                    width = self.KEYBOARD_BUTTON_WIDTH,                       
                    height = self.KEYBOARD_BUTTON_HEIGHT, 
                    text = self.KEYBOARD_BUTTON_NAMES[1][c],                        
                    fg=self.KEYBOARD_BUTTON_TEXT_BEGIN, 
                    command = handler)
            button.grid(row =  1, column = c + 1, padx = self.PADDING//2)

            # Put the button in a dictionary of buttons
            # where the key is the button text, and the
            # value is the button object.
            self.button_dict[self.KEYBOARD_BUTTON_NAMES[1][c]] = button 

            # Center the keys in te frame
            self.mid_row_letters.grid_columnconfigure(0, weight = 1)
            self.mid_row_letters.grid_columnconfigure(
                len(self.KEYBOARD_BUTTON_NAMES[1]) + 1 , weight = 1)
            self.mid_row_letters.grid_rowconfigure(0, weight = 1)
            self.mid_row_letters.grid_rowconfigure(2, weight = 1)


    def keyboard_third_row(self):
        """
        Creates the third row of buttons for the keyboard
        """

        # Create the frame to put the second row of keys in
        self.bot_row_letters = tk.Frame(self.keyboard_frame, width=self.PARENT_GUESS_FRAME_WIDTH, 
                        height= self.KEYBOARD_FRAME_HEIGHT//3)
        self.bot_row_letters.grid(row=3, column=1)
        self.bot_row_letters.grid_propagate(False)

        #Third line of letters in keyboard
        for c in range(len(self.KEYBOARD_BUTTON_NAMES[2])):               
            if len(self.KEYBOARD_BUTTON_NAMES[2][c]) >= 4:
                self.KEYBOARD_BUTTON_WIDTH_CHANGED = self.KEYBOARD_BUTTON_WIDTH_LONG

            if len(self.KEYBOARD_BUTTON_NAMES[2][c]) <= 3:
                self.KEYBOARD_BUTTON_WIDTH_CHANGED = self.KEYBOARD_BUTTON_WIDTH

            # Defines a handler for the buttons
            def handler(key = self.KEYBOARD_BUTTON_NAMES[2][c]):
                self.keyboard_button_handler(key)

            # Create the button objects
            button = tk.Button(self.bot_row_letters,
                    width = self.KEYBOARD_BUTTON_WIDTH_CHANGED,                       
                    height = self.KEYBOARD_BUTTON_HEIGHT, 
                    text = self.KEYBOARD_BUTTON_NAMES[2][c],                        
                    fg=self.KEYBOARD_BUTTON_TEXT_BEGIN, 
                    command = handler)
            button.grid(row =  1, column = c + 1, padx = self.PADDING//2)

            # Put the button in a dictionary of buttons
            # where the key is the button text, and the
            # value is the button object.
            self.button_dict[self.KEYBOARD_BUTTON_NAMES[2][c]] = button 

            # Center the keys in te frame
            self.bot_row_letters.grid_columnconfigure(0, weight = 1)
            self.bot_row_letters.grid_columnconfigure(
                len(self.KEYBOARD_BUTTON_NAMES[2]) + 1 , weight = 1)
            self.bot_row_letters.grid_rowconfigure(2, weight = 1)
        

    def keyboard_button_handler(self, text):
        """ Displays which key was hit by the user in the terminal. """

        print(text, "button was hit.")

        # Put letter in the correct box if letter clicked
        if self.current_guess['col'] < self.WORD_SIZE and text not in ["ENTER", "BACK"]:
            self.letter_box_list[self.current_guess['row']][self.current_guess['col']]['text'] = text
            self.guessed_letters_list.append(text)
            self.current_guess['col'] += 1

        # Remove the most recent letter guessed if back is clicked
        elif text == 'BACK' and self.current_guess['col'] > 0:
            self.current_guess['col'] -= 1
            self.guessed_letters_list.pop()
            self.letter_box_list[self.current_guess["row"]][self.current_guess["col"]]["text"] = ""

        # If enter is clicked
        elif text == 'ENTER':

            self.word_guessed = ''.join(self.guessed_letters_list).lower()

            # Check if a full 5 letter word was guessed
            if self.current_guess['col'] != self.WORD_SIZE:
                self.show_message('Word not finished')

            # If guess must be words is on check if word is in the long list
            elif self.be_words_var.get() and self.word_guessed not in self.long_word_list:
                self.show_message(f'{self.word_guessed} is not in the word list')

            # If user guessed word correctly, display message
            elif self.word_guessed == self.hidden_word:
                self.color_change(self.current_guess['row'])
                self.show_message('Correct. Nice job. Game over.')
                return

            # If user did not guess word in 6 tries, display message
            elif self.current_guess['row'] == self.NUM_GUESSES -1:
                self.color_change(self.current_guess['row'])
                self.show_message(f'Guesses used up. Word was {self.hidden_word}. Game over')
                return

            # reset the entry and move down to the next row
            else:
                self.color_change(self.current_guess['row'])
                self.current_guess['row'] += 1
                self.current_guess['col'] = 0
                self.guessed_letters_list = []
            

    def color_change(self, row):
        """
        Changes the color of keyboard and guess frames depending on accuracy of user guess. 
        """

        # Initialize a list for the letters guessed
        self.letters_guessed = []

        # Correct letters fill in first
        self.order_of_guesses = self.get_order_of_letters()

        # Loop through each letter
        for col in self.order_of_guesses:

            # Get current letter from box
            cur_letter = self.letter_box_list[row][col]["text"].lower()

            # Color changes to white
            self.letter_box_list[row][col]["fg"] = "white"

            # Change to green if letter is in correct place
            if cur_letter == self.hidden_word[col]:
                self.letter_frame_list[row][col]["bg"] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                self.letter_box_list[row][col]["bg"] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC
                self.button_dict[self.letter_box_list[row][col]["text"]]["fg"] = self.GUESS_FRAME_BG_CORRECT_RIGHT_LOC

            # Change to orange if letter is in the word but in the wrong place
            elif cur_letter in self.hidden_word:

                # Change to gray after max amount if the letter appears multiple times
                if cur_letter in self.letters_guessed:
                    if self.letters_guessed.count(cur_letter) >= self.hidden_word.count(cur_letter):
                        self.letter_frame_list[row][col]["bg"] = self.GUESS_FRAME_BG_WRONG
                        self.letter_box_list[row][col]["bg"] = self.GUESS_FRAME_BG_WRONG
                        self.button_dict[self.letter_box_list[row][col]["text"]]["fg"] = self.GUESS_FRAME_BG_WRONG
                        continue
                
                self.letter_frame_list[row][col]["bg"] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                self.letter_box_list[row][col]["bg"] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC
                self.button_dict[self.letter_box_list[row][col]["text"]]["fg"] = self.GUESS_FRAME_BG_CORRECT_WRONG_LOC

            # Change to grey if letter is not in the word
            else:
                self.letter_frame_list[row][col]["bg"] = self.GUESS_FRAME_BG_WRONG
                self.letter_box_list[row][col]["bg"] = self.GUESS_FRAME_BG_WRONG
                self.button_dict[self.letter_box_list[row][col]["text"]]["fg"] = self.GUESS_FRAME_BG_WRONG
                
            self.letters_guessed.append(cur_letter)

    def get_order_of_letters(self):
        """
        Returns a list with the correct letter indexes at the front
        """

        self.order_of_guesses = []
        self.guessed_word = ''.join(self.guessed_letters_list).lower()

        # To handle cases in which there are multiple of the same letter 
        # in a guesses, add the correct letters first 
        for i in range(len(self.hidden_word)):
            if self.hidden_word[i] == self.guessed_word[i]:
                # insert the correct letter to front of list
                self.order_of_guesses.insert(0, i) 
            else:
                # add to back of list if incorrect
                self.order_of_guesses.append(i) 

        return self.order_of_guesses




if __name__ == "__main__":
   Wordy()