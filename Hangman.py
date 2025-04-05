from tkinter import *
from tkinter import messagebox
import random


# Function to display instructions on how to play hangman
def instructions():
    # Create New Window
    instr_window = Toplevel(root)
    instr_window.title("How to Play Hangman")

    # Instructions
    heading = Label(instr_window, text="How to Play Hangman", font=("Ariel", 12))
    instruction1 = "1) The word to guess is shown as a row of dashes, one for each letter\n"
    instruction2 = "2) Guess a letter: If the guessed letter is in the word, it's position/s will be revealed\n"
    instruction3 = "3) If the guessed letter is not in the word, a body part will be added to the stick figure.\n"
    instruction4 = "4) Guess the word before the stickman is complete!"

    instruction = instruction1 + instruction2 + instruction3 + instruction4

    # Display Instructions
    msg = Message(instr_window, text=instruction, anchor=W)

    heading.pack()
    msg.pack()


# Create the gallows
def create_hangman():
    line_shaft = C.create_line(70, 10, 320, 10, width=3, fill="#964b00")  # Create shaft
    line_beam = C.create_line(70, 10, 70, 250, width=3, fill="#964b00")  # Create beam
    line_base = C.create_line(20, 250, 120, 250, width=3, fill="#964b00")  # Create base
    line_rope = C.create_line(195, 10, 195, 35, width=3, fill="#964b00")  # Create rope


# Create the body parts of Hangman
def update_hangman():
    global incorrect_guesses
    if incorrect_guesses > 0:
        head = C.create_oval(170, 35, 220, 80, width=3, fill='black')  # Make head
    if incorrect_guesses > 1:
        body = C.create_line(195, 80, 195, 175, width=3)  # Make body
    if incorrect_guesses > 2:
        l_hand = C.create_line(195, 100, 170, 140, width=3)  # Make left hand
    if incorrect_guesses > 3:
        r_hand = C.create_line(195, 100, 220, 140, width=3)  # Make right hand
    if incorrect_guesses > 4:
        l_leg = C.create_line(195, 175, 170, 215, width=3)  # Make left leg
    if incorrect_guesses > 5:
        r_leg = C.create_line(195, 175, 220, 215, width=3)  # Make right leg


def is_valid_guess(guess):
    guess_var.set("")  # delete the guess of the player

    # Check if the guess is valid (only a letter is guessed)
    if len(guess) == 1 and guess.isalpha():
        check_guess(guess)  # check if the guess is correct and display it
    else:
        messagebox.showerror("Error", "Invalid Guess! Try Again!")  # display error


# Function to check if guess is correct
def check_guess(guess):
    global incorrect_guesses

    guessed_letters.append(guess)  # add the letter to the list of guessed letters

    # if correct, display the guessed letter in chosen word
    if guess in word:
        display_guess(guess)
    # else increase incorrect guesses and add a body part to the hangman
    else:
        incorrect_guesses += 1
        update_hangman()
        check_win_lose()


# Function to provide a hint for the chosen word
def hint():
    for letter in word:  # check every letter in the chosen word
        if letter not in guessed_letters:  # if the letter has not been guessed by the player
            guessed_letters.append(letter)
            display_guess(letter)  # display that letter
            return


def display_guess(guess):
    global display_word
    display_word = display_word.replace(" ", "")  # remove the spaces in the display word
    display_list = list(display_word)  # make a list of the letters of the display word

    # loop through the list
    for i in range(len(word)):
        if word[i] == guess:  # if guess is in word
            display_list[i] = word[i]  # change the dash at index i to word[i]
    display_word = " ".join(display_list)  # convert list to string
    word_label.config(text=display_word)  # update label
    check_win_lose()  # check if player won


def check_win_lose():
    global display_word
    try_again = False

    # check win
    if display_word.replace(" ", "") == word:
        # display win message
        try_again = messagebox.askyesno("You Won!", "You Guessed The Word!\nTry Again?")

        guess_entry.config(state="disabled")  # disable entry
        guess_button.config(state="disabled")  # disable guess button

    # Check loss
    elif incorrect_guesses == 6:
        # display lose message
        try_again = messagebox.askyesno("You Lose", "You Lost :(\nThe word was: " + word + "\nTry Again?")

        guess_entry.config(state="disabled")  # disable entry
        guess_button.config(state="disabled")  # disable guess button

    # if player wants to try again, restart the game
    if try_again:
        reset_hangman()


def reset_hangman():
    global display_word, incorrect_guesses, words, word
    guessed_letters.clear()  # empty the list
    guess_entry.config(state="normal")  # enable the entry
    guess_button.config(state="normal")  # enable the guess button
    incorrect_guesses = 0  # initialize incorrect guesses
    C.delete('all')  # delete Canvas
    word = random.choice(words)  # choose a random word again
    display_word = "_ " * len(word)  # create the display word with dashes
    word_label.config(text=display_word)  # change label
    create_hangman()  # create the gallows


# Main Program
incorrect_guesses = 0  # Initialize incorrect guesses

guessed_letters = []  # Make a list to store guessed letters

# Words for Hangman
words = ["apple", "beach", "chair", "dance", "house",
         "puzzle", "rainbow", "dolphin", "forest", "lantern",
         "chandelier", "pharaoh", "glacier", "quarantine", "symphony"]

# choose a random word from the list
word = random.choice(words)

# Create Window
root = Tk()
root.title("Hangman")
root.geometry("500x500")

# Create Instruction Button
instr = Button(root, relief=RAISED, bitmap="info", command=instructions)
instr.pack(side=RIGHT, anchor=NE)

# Create Hint Button
hint = Button(root, relief=RAISED, bitmap="questhead", command=hint)
hint.pack(side=RIGHT, anchor=NE, padx=10)

# Display the chosen words as dashes
display_word = "_ " * len(word)
word_label = Label(text=display_word, font=("Ariel", 25))
word_label.pack(pady=15)

# Create Canvas
C = Canvas(root, height=275, width=400)
C.pack(pady=0)

create_hangman()

# Create Entry for user to guess letters
guess_var = StringVar()
guess_entry = Entry(root, textvariable=guess_var, font=("Ariel", 18))
guess_entry.pack(pady=5)

# Create button to enter the guessed letter
guess_button = Button(root, text="Guess", command=lambda: is_valid_guess(guess_var.get().lower()))
guess_button.pack()

mainloop()
