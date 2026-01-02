hangman_str = """

 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/           

"""

skull = """

                         _,.-------------.._
                      ,-'        j          `-.
                    ,'        .-'               `.
                   /          |                   '
                  /         ,-'                    `
                 .         j                         
                .          |                          
                : ._       |   _....._                 .
                |   -.     L-''       `.               :
                | `.  \  .'             `.             |
               /.\  `, Y'                 :           ,|
              /.  :  | \                  |         ,' |
             \.    " :  `\                |      ,--   |
              \    .'     '-..___,..      |    _/      :
               \  `.      ___   ...._     '-../        '
             .-'    \    /| \_/ | | |      ,'         /
             |       `--' |    '' |'|     /         .'
             |            |      /. |    /       _,'
             |-.-.....__..|     Y-dp`...:...--'''
             |_|_|_L.L.T._/     |
             \_|_|_L.T-''/      |
              |                /
             /             _.-'
             :         _..'
             \__...--''


"""

bulb = """

  ..---..
 /       \
|         |
:         ;
 \  \~/  /
  `, Y ,'
   |_|_|
   |===|
   |===|
    \_/   


"""

stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', '''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

import random
import sys

def clear():
    # Browser (Pyodide): clear the HTML console
    try:
        import js
        js.globalThis.__clear_console__()
        return
    except Exception:
        pass

async def ainput(prompt: str = "") -> str:
    if prompt:
        print(prompt, end="")
        sys.stdout.flush()  # <-- critical: forces prompt to appear immediately
    s = await __js_ainput__()
    return "" if s is None else str(s)

def random_w():
    """Get random word from lengthy text file"""
    filename = "WordsFile.txt"
    filepath = filename

    with open(filepath, "r") as file:
        lines = file.readlines()
        stripped_words = []
        for word in lines:
            stripped_words.append(word.strip("\n"))

    random_word = random.choice(stripped_words).lower()

    # return word
    return random_word


async def get_letter_entry():
    """function for asking user for text entry"""
    input1 = "0"
    is_valid_letter = False
    while not is_valid_letter:

        input1 = (await ainput("Tell me your guess!")).strip()
        if len(input1) > 1:
            print("\nOnly 1 character please! \n")
        elif input1.isnumeric():
            print("\nNo numbers please \n")
        elif any(not c.isalnum() for c in input1):
            print("\nNo special characters please \n")
        else:
            is_valid_letter = True
    return(input1.lower()) #returns guess

def check_word_return_guess(letter, word, letters_and_blanks):
    """takes guess and checks against the contents of the word"""
    is_letter_in_word = False
    for character in range(0, len(word)): 					#check if letter in word
        if letter == word[character]:
            letters_and_blanks[character] = " " + letter + " "
            is_letter_in_word = True

    if " _ " not in letters_and_blanks:	#check if word is fully guessed
        is_finished = True
    else:
        is_finished = False

    result = [letters_and_blanks, is_finished, is_letter_in_word]
    return result


if __name__== "__main__":

    # get random word
    random_word = random_w()

    print(hangman_str)

    # print random word in blank spaces
    blank_string = []
    for x in range(0, len(random_word)):
        blank_string.append(" _ ")
    blank = "".join(blank_string)
    print(f"{blank}")

    # assume game is ongoing
    game_is_finished = False

    # initialize list of guesses, and lives
    list_of_guesses = []
    Lives = 6

    # while neither win nor lose
    while not game_is_finished:

        # get guess
        guess = await get_letter_entry()
        clear()

        # assume not repeat guess
        # checks if repeat guess
        previous_guesses = False
        for character in list_of_guesses:
            if guess == character:
                previous_guesses = True

        # if new guess, add to list of guesses
        if previous_guesses == False:
            list_of_guesses.append(guess)
            string_of_guesses = ", ".join(list_of_guesses)

        # if repeat guess display guess and reset loop
        else:
            print("You already guessed that! \n")
            string_of_guesses = ", ".join(list_of_guesses)
            print(f"You already guessed that!\n This is your list of guesses: {string_of_guesses} \n"
                "Guess again! \n")
            continue

        # if new guess, compare guess, answer, and blank string
        result = check_word_return_guess(guess, random_word, blank_string)

        # get is game over value
        game_is_finished = result[1]

        # get is letter in word value
        is_letter_in_word = result[2]

        # get new display string
        string_to_display = "".join(result[0])


        # if game is still being played ...
        if not game_is_finished:

            # if bad guess, take away life, add body part, and display
            if not is_letter_in_word:
                Lives -= 1
                if Lives == 0:
                    print(f"{skull}\n\n{stages[Lives]}\n\nYou lose!\n\nYour final guess was: {string_to_display}\n\nYour list of guesses: {string_of_guesses}")
                    print(f"The word was: {random_word}")
                    game_is_finished = True
                else:
                    print(f" \n\nIncorrect!\n{stages[Lives]}\n\n{string_to_display}\n\n\nYour list of guesses: {string_of_guesses}")
            # if good guess add letter to display string
            else:
                print(f" \n\nCorrect\n\n{stages[Lives]}\n\n{string_to_display}\n\n\nYour list of guesses: {string_of_guesses}")

        # if game is over, display end
        else:
            print(f" \n\n{bulb}\n\nYou win!! {stages[Lives]}\n\n{string_to_display}\n\nYour list of guesses: {string_of_guesses}")
            game_is_finished = True












