# Sean Melone
# CPE 551

from tkinter import *   # tkinter is used to make our ui. * imports everything from the package
from tkinter.simpledialog import askstring  # needed for us to take input to change names


def change_name():
    global players
    name1 = askstring('P1', 'Enter string as name for player 1 (names > 6 characters will be tossed)')
    if len(name1) <= 6:  # only set new name in array if <=6
        players[0] = name1

    name2 = askstring('P2', 'Enter string as name for player 2 (names > 6 characters will be tossed)')
    if len(name2) <= 6:
        players[1] = name2

    new_game()  # must start new game to avoid bugs


def dark_mode():  # bonus function to run program in dark mode
    global color
    if color == "#F0F0F0":  # if color is default change to dark
        color = "#756E6D"
    else:
        color = "#F0F0F0"  # otherwise set color to default white

    for r in range(0, 3):  # loop through and change color of all tiles
        for c in range(0, 3):
            board[r][c].config(bg=color)



def next_turn(row, col):  # row and col are required arguments here
    global player  # player is a global variable so that it can be used outside this function after it is reinitialized
    global ai_bool  # ai features are experimental as this program was not designed with AI in mind
    check_break = False
    if board[row][col]['text'] == "" and check_win() is False:  # pycharm taught me is False is better than == False
        if ai_bool is True:
            board[row][col]['text'] = player
            if check_win() is True:
                label.config(text=(player + " won!"))
                return
            for r in range(0, 3):  # this ai simply loops through all the squares and takes the first available one
                if check_break is True:  # crude way to break out of nested loop
                    break
                for c in range(0, 3):
                    if board[r][c]['text'] == "":  # check empty square
                        board[r][c]['text'] = players[1]  # set square to player 2 controlled by ai
                        check_break = True
                        break
            if check_win() is True:
                label.config(text=(players[1] + " won!"))
            if check_win() == -1:
                label.config(text="you tied the AI :(")
            return




        if player == players[0]:
            board[row][col]['text'] = player  # sets the text in the button equal to the name of the player. ie. x or o
            if check_win() is False:
                player = players[1]  # this swaps player 1 to player 2
                label.config(text=(players[1] + "'s turn"))
            if check_win() is True:
                label.config(text=(players[0] + " won!"))
            if check_win() == -1:
                label.config(text=("Game ended in a tie :("))

        else:
            board[row][col]['text'] = player
            if check_win() is False:
                player = players[0]  # this swaps player 2 to player 1
                label.config(text=(players[0] + "'s turn"))
            if check_win() is True:
                label.config(text=(players[1] + " won!"))
            if check_win() == -1:
                label.config(text="Game ended in a tie :(")


def check_win():  # this function manually checks all possible win conditions
    # could create a scalable algorithm to do this but that is unnecessary. the board will always be 3x3
    if check_available() is False:
        for r in range(0, 3):
            for c in range(0, 3):
                board[r][c].config(bg="gray")  # makes squares grayed out if tie
        return -1
    if board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] != "":  # check backwards diagonal
        board[0][0].config(bg="cyan")
        board[1][1].config(bg="cyan")
        board[2][2].config(bg="cyan")
        return True
    if board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] != "":  # check forwards diagonal
        board[0][2].config(bg="cyan")
        board[1][1].config(bg="cyan")
        board[2][0].config(bg="cyan")
        return True

    for row in range(0, 3):  # loop through all rows and check win
        if board[row][0]['text'] == board[row][1]['text'] == board[row][2]['text'] != "":
            board[row][0].config(bg="cyan")
            board[row][1].config(bg="cyan")
            board[row][2].config(bg="cyan")
            return True
    for column in range(0, 3):  # loop through all cols and check win
        if board[0][column]['text'] == board[1][column]['text'] == board[2][column]['text'] != "":
            board[0][column].config(bg="cyan")
            board[1][column].config(bg="cyan")
            board[2][column].config(bg="cyan")
            return True

    else:
        return False


def check_available():  # this checks if any spaces are available. if none are, a draw results
    moves = 0
    for r in range(0, 3):  # works by looping through and counting the total moves made
        for c in range(0, 3):  # loops through the entire grid to check each square
            if board[r][c]['text'] != "":  # adds to move counter if space is not empty
                moves += 1
    if moves == 9:
        return False
    else:
        return True


def new_game():
    global player  # reference global var player
    global color
    global ai_bool
    if ai_bool is True:
        player = players[0]
    elif player == players[0]:
        player = players[1]
    else:
        player = players[0]
    label.config(text=player + "'s turn")  # clears board and returns board to default color used in tkinter

    for r in range(0, 3):
        for c in range(0, 3):
            board[r][c].config(text="", bg=color)


def ai():  # function to toggle play vs ai value on or off
    global ai_bool
    if ai_bool is True:
        ai_bool = False
        players[1] = "O"  # reset player 2 name
        main_window.title("Tic-Tac-Toe!")
    else:
        ai_bool = True
        players[1] = "AI"  # set player 2 name to AI
        main_window.title("Tic-Tac-Toe! (vs ai)")
    new_game()
# driver code below


main_window = Tk()  # instance of Tkinter class to create our window
main_window.title("Tic-Tac-Toe!")

ai_bool = False  # initialize ai to false
color = "#F0F0F0"
players = ['X', 'O']  # list of players. using an array allows us to easily swap players and even change names
player = players[0]  # initialize the first player in the list to go first
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]   # this 2d list serves as the game board


label = Label(text=player + "'s turn", font=('terminal', 24))  # use keywords here for non default arguments
label.pack(side='top')  # aligns label with top of screen

change_name_button = Button(text="Change Names", font=('terminal', 10), command=change_name)
change_name_button.pack(side='bottom') # pack button to bottom of window

toggle_ai_button = Button(text="Toggle AI (easy)", font=('terminal', 10), command=ai)
toggle_ai_button.pack(side='bottom')

new_game_button = Button(text="New game", font=('terminal', 10), command=new_game)
new_game_button.pack(side='bottom')

dark_mode_button = Button(text="Toggle Dark Mode", font=('terminal', 7), command=dark_mode)
dark_mode_button.pack(side='bottom')

frame = Frame(main_window)
frame.pack()

for row in range(0, 3):  # loops by row first, then column in a 2d array
    for col in range(0, 3):  # nested for loop lets us create this as a grid
        board[row][col] = Button(frame, text="", font=('terminal', 48), width=6, height=3, command=lambda row=row, col=col: next_turn(row, col))
        # the above line initializes all the buttons on the board we made earlier and assigns them the next turn method
        board[row][col].grid(row=row,column=col)  # adds the buttons in a grid arrangement each time the loop increments


main_window.mainloop()








