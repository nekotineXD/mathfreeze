# import necessary modules
# import time
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3
import random
# from time import strftime

# Database connection
conn = sqlite3.connect('myDb.db')  # connect to database
cursor = conn.cursor()  # create the cursor
# Create Table
# cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_easy(id integer primary key, user_name text, score integer)""")
# conn.commit()
# conn.close()

# root window creation
root = Tk()
root.title('Math Freeze!')
# disable/enable resize window
root.resizable(False, False)

root_window_width = 500
root_window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (root_window_width / 2)
y = (screen_height / 2) - (root_window_height / 2)

root.geometry(f'{root_window_width}x{root_window_height}+{int(x)}+{int(y)}')
# root.attributes('-fullscreen', True)

# mainGame window creation
mainGame = Tk()
mainGame.withdraw()  # hides mainGame

# gameOver window creation
gameOver = Tk()
gameOver.withdraw()  # hides gameOver


def root_onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        mainGame.destroy()
        gameOver.destroy()
        conn.close()


def mainGame_onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        mainGame.destroy()
        gameOver.destroy()
        conn.close()


def gameOver_onClosing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        mainGame.destroy()
        gameOver.destroy()
        conn.close()


num1 = random.randint(1, 10)
num2 = random.randint(1, 10)
score = 0
timerDifficulty = "easy"
timerEasy = 8


def numRand():
    global num1
    global num2
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)


def btnStart_click():  # start button function
    global conn
    global cursor
    global screen_width
    global screen_height
    global x
    global y
    global score
    global timerEasy

    root.withdraw()  # hide window
    # root.deiconify()

    # second = StringVar()
    # second.set("8")

    # mainGame window creation
    newWindow = Toplevel(mainGame)
    newWindow.title('Math Freeze!')
    newWindow.resizable(False, False)  # disable/enable resize window

    # set window size and centered to the screen
    mainGame_window_width = 600
    mainGame_window_height = 600
    screen_width = mainGame.winfo_screenwidth()
    screen_height = mainGame.winfo_screenheight()
    x = (screen_width / 2) - (mainGame_window_width / 2)
    y = (screen_height / 2) - (mainGame_window_height / 2)

    newWindow.geometry(f'{mainGame_window_width}x{mainGame_window_height}+{int(x)}+{int(y)}')

    # Database connection
    conn = sqlite3.connect('myDb.db')  # connect to database
    cursor = conn.cursor()
    username = txt_username.get()
    cursor.execute("""SELECT * FROM tbl_easy WHERE username = :username""",
                   {
                       'username': username
                   })
    conn.commit()
    data = cursor.fetchall()
    if not data:  # scans if list is empty
        cursor.execute("""INSERT INTO tbl_easy VALUES(:username, :score)""",
                       {
                           'username': username,
                           'score': 0
                       })
        conn.commit()
        # conn.close()
    else:
        print(username + " is logged in!")

    def updateScore():
        cursor.execute("""SELECT easy_score FROM tbl_easy WHERE username=:username""",
                       {
                           'username': username
                       })
        conn.commit()
        # display data from myDb.db
        # and put them in lbl_username
        print_data1 = 'High-score: '
        data2 = cursor.fetchall()
        for item1 in data2[0]:
            print_data1 += str(item1)

        lbl_highscore.config(text=print_data1)
        # conn.close()

    cursor.execute("""SELECT username FROM tbl_easy WHERE username=:username""",
                   {
                       'username': username
                   })
    conn.commit()

    print_data = 'Username: '
    data1 = cursor.fetchall()
    for item in data1[0]:
        print_data += str(item)

    # label for current user
    lbl_username = Label(newWindow, text=print_data, font=("Arial", 16))
    lbl_username.pack(anchor=CENTER, pady=5)

    cursor.execute("""SELECT easy_score FROM tbl_easy WHERE username=:username""",
                   {
                       'username': username
                   })
    conn.commit()

    print_data2 = 'High-score: '
    data3 = cursor.fetchall()
    for item in data3[0]:
        print_data2 += str(item)

    # label for high score
    lbl_highscore = Label(newWindow, text=print_data2, font=("Arial", 16))
    lbl_highscore.pack(anchor=CENTER, pady=5)

    # label for current score
    lbl_currentscore = Label(newWindow, text="Current score: " + str(score), font=("Arial", 16))
    lbl_currentscore.pack(anchor=CENTER, pady=5)

    # label for the question
    lbl_question = Label(newWindow, text=str(num1) + " + " + str(num2), font=("Arial", 16))
    lbl_question.pack(anchor=CENTER, pady=5)

    # textbox for the user's answer
    txt_answer = Entry(newWindow, width=40)
    txt_answer.pack(anchor=CENTER, pady=5)

    def updateTime():
        global timerEasy
        if timerDifficulty == "easy":
            timerEasy -= 1
            lbl_timer.config(text=timerEasy)
            if timerEasy == 0:
                print("Game Over!")
                # newWindow.withdraw()
                endGame()

    # label for timer
    lbl_timer = Label(newWindow, text=timerEasy, font=("Arial", 16))
    lbl_timer.pack(anchor=CENTER, pady=5)

    if timerDifficulty == "easy":
        lbl_timer.after(1000, updateTime)
        lbl_timer.after(2000, updateTime)
        lbl_timer.after(3000, updateTime)
        lbl_timer.after(4000, updateTime)
        lbl_timer.after(5000, updateTime)
        lbl_timer.after(6000, updateTime)
        lbl_timer.after(7000, updateTime)
        lbl_timer.after(8000, updateTime)

    def endGame():
        global screen_width
        global screen_height
        global x
        global y
        global score

        finalScore = score
        score = 0

        newWindow.withdraw()
        newWindow1 = Toplevel(gameOver)
        newWindow1.title('Math Freeze!')
        newWindow1.resizable(False, False)  # disable/enable resize window

        # set window size and centered to the screen
        gameOver_window_width = 400
        gameOver_window_height = 600
        screen_width = gameOver.winfo_screenwidth()
        screen_height = gameOver.winfo_screenheight()
        x = (screen_width / 2) - (gameOver_window_width / 2)
        y = (screen_height / 2) - (gameOver_window_height / 2)

        newWindow1.geometry(f'{gameOver_window_width}x{gameOver_window_height}+{int(x)}+{int(y)}')

        # label for username
        lbl_username1 = Label(newWindow1, text=print_data, font=("Arial", 16))
        lbl_username1.pack(anchor=CENTER, pady=5)

        cursor.execute("""SELECT easy_score FROM tbl_easy WHERE username=:username""",
                       {
                           'username': username
                       })
        print_data3 = 'High-score: '
        data4 = cursor.fetchall()
        for item2 in data4[0]:
            print_data3 += str(item2)

        # label for high-score
        lbl_highscore1 = Label(newWindow1, text=print_data3, font=("Arial", 16))
        lbl_highscore1.pack(anchor=CENTER, pady=5)

        # label for final score
        lbl_finalscore = Label(newWindow1, text="Final Score: " + str(finalScore), font=("Arial", 16))
        lbl_finalscore.pack(anchor=CENTER, pady=5)

        def retry():
            numRand()
            lbl_currentscore.config(text="Current score: " + str(score))
            lbl_question.config(text=str(num1) + " + " + str(num2))
            newWindow1.withdraw()
            newWindow.deiconify()

        # button for retry
        btn_retry = Button(newWindow1, text="Retry", command=retry)
        btn_retry.pack(anchor=CENTER, pady=5)

        def quitToMenu():
            newWindow1.withdraw()
            root.deiconify()

        # button for main menu
        btn_quit = Button(newWindow1, text="Main Menu", command=quitToMenu)
        btn_quit.pack(anchor=CENTER, pady=5)

        # loop newWindow1 and call mainGame_onClosing() protocol
        newWindow1.protocol("WM_DELETE_WINDOW", gameOver_onClosing)
        newWindow1.mainloop()

    def btnSubmit_click():
        global score
        global screen_width
        global screen_height
        global x
        global y
        global timerEasy

        timerEasy = 8
        lbl_timer.config(text=timerEasy)

        try:
            answer = int(txt_answer.get())
            if answer == (num1+num2):
                score += 1
                txt_answer.delete(0, END)
                numRand()
                lbl_question.config(text=str(num1)+"+"+str(num2))
                lbl_currentscore.config(text="Current score: " + str(score))
                print(score)
            else:
                print("Game Over!")

                cursor.execute("""SELECT easy_score FROM tbl_easy WHERE username=:username""",
                               {
                                   'username': username
                               })
                # print_data1 = ''
                data2 = cursor.fetchall()
                pastScore = 0
                for item1 in data2[0]:
                    # print_data1 += str(item1) + "\n"
                    pastScore = int(item1)
                if score > pastScore:
                    cursor.execute("""UPDATE tbl_easy SET easy_score=:score WHERE username=:username""",
                                   {
                                       'score': score,
                                       'username': username
                                   })
                    conn.commit()
                    updateScore()
                    # finalScore = score
                    # score = 0
                    txt_answer.delete(0, END)
                else:
                    print("Did not beat high score")
                    # finalScore = score
                    # score = 0
                    txt_answer.delete(0, END)
                endGame()
        except ValueError:
            print("Time's up!")

    # submit answer button
    btn_submit = Button(newWindow, text="Submit", command=btnSubmit_click)
    btn_submit.pack(anchor=CENTER, pady=5)

    # loop newWindow and call mainGame_onClosing() protocol
    newWindow.protocol("WM_DELETE_WINDOW", mainGame_onClosing)
    newWindow.mainloop()


# global variables for btnStart_click()
lbl_startText = "Math Freeze!"

# label for hello
lbl_start = Label(root, text=lbl_startText, font=("Impact", 32))
# lbl_start.grid(row=0, column=0, sticky="NESW")
# lbl_start.grid_columnconfigure(0, weight=1)
lbl_start.pack(anchor="center", pady=5)

# username textbox
txt_username = Entry(root, width=40)
txt_username.pack(anchor="center", pady=5)

# username password
# txt_password = Entry(root, width=40)
# txt_password.pack(anchor="center", pady=5)

# button for start game
btn_start = Button(root, text="Play", command=btnStart_click)
# btn_start.grid(row=1, column=0, sticky="NESW")
# btn_start.grid_columnconfigure(0, weight=1)
btn_start.pack(anchor="center", pady=5)

# loop the program and call on_closing() method
root.protocol("WM_DELETE_WINDOW", root_onClosing)
root.mainloop()
