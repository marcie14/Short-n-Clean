#M E 369P - Team 4 - Short n' Clean 
#Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava
#GUI File:
#    This file creates the GUI for the game of rock paper scissors
#    Much of this file was extrapolated from https://pythonistaplanet.com/rock-paper-scissors-game-using-python-tkinter/
#    Changes made for this project: 
#        -Winner/Loser Comments
#        -Easy (random) and Hard (cheat) mode
#        -Not-So-Random computer hand selection for Hard Mode
#        -Incorporating OpenCV and trained model 
#FLOW OF CODE:
#1. create a live window and gui
#2. player chooses easy or hard -> goes to that loop
#3. player presses 's' to screenshot hand
#4. computer detects and predicts players hand
#5. computer calls on player_hand, passing predicted players hand
#6. rock paper or scissors is called depending on hand
#7. computer hand is decided (either randomly or by cheating)
#8. results is called on to determine winner 


# import required libraries
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
from platformdirs import user_cache_dir
import tensorflow as tf
keras = tf.keras
import numpy as np
from random import choice
import time
import os 
import random

# We might not need this part 
# Create folder where we can capture player's move 
Data = 'Player Move'
mode = '' # variable to store difficulty chosen by user

# initializing global variables
user_score = 0      # keeps track of user's score for RPS game
user_hand = ''      # keeps track of user's hand for RPS game
comp_score = 0      # keeps track of computer's score for RPS game
comp_hand = ''      # keeps track of computer's hand for RPS game

if not os.path.exists(Data):
    print('Creating folder ', Data)
    os.makedirs(Data)

# Number of photos taken 
photo_of_move = 0

# converts choice (string) to number (int) - used by results(user, comp) function
def choice_to_number(choice):
    print('getting choice to number: ' + choice)
    rps = {'rock':0, 'paper':1, 'scissors':2}
    return rps[choice]

# function to decipher player move and call rock/paper/scissors functions
def player_hand(user):
    print('user hand: ' + user)
    if user == 'rock':
        user_hand = 'rock'
        rock()
    elif user == 'paper':
        user_hand = 'paper'
        paper()
    elif user == 'scissors':
        user_hand = 'scissors'
        scissors()
    elif user == 'none':
        user_hand = 'none'
        print("Error: computer couldn't read user's hand.")
        none()
    else:
        print("Error: user hand variable empty.")

# function to decide random computer choice for easy mode
def random_computer_choice():
    return random.choice(['rock','paper','scissors']) 

# function to decide computer hand if user plays rock
def rock():
    global comp_hand 
    global user_hand
    user_hand ='rock'
    comp_hand = ''
    if mode == 'Easy':     # Easy Mode
        comp_hand = random_computer_choice() 
    elif mode == 'Hard':   # Hard Mode
        comp_hand ='paper'
    print('comp hand: ' + comp_hand)
    return

# function to decide computer hand if user plays paper
def paper():
    global comp_hand 
    global user_hand
    user_hand ='paper'
    comp_hand = ''
    if mode == 'Easy':     # Easy Mode
        comp_hand = random_computer_choice() 
    elif mode == 'Hard':   # Hard Mode
        comp_hand ='scissors'
    print('comp hand: ' + comp_hand)
    return

# function to decide computer hand if user plays scissors
def scissors():
    global comp_hand 
    global user_hand
    user_hand ='scissors'
    comp_hand = ''
    if mode == 'Easy':     # Easy Mode
        comp_hand = random_computer_choice() 
    elif mode == 'Hard':   # Hard Mode
        comp_hand ='rock'
    print('comp hand: ' + comp_hand)
    return

# function if players hand couldnt be detected
def none():
    print('ERROR: UNABLE TO RETRIEVE PLAYERS HAND')
    return

# random win statement
def random_win_statement():
    r = random.randint(1,5)
    match r:
        case 1:
            statement = 'That was all luck...'
        case 2:
            statement = 'You got lucky'
        case 3:
            statement = 'I let you win that one...'
        case 4:
            statement = 'Your awkward hands were\ndistracting me...'
        case 5:
            statement = 'You cheated!'
    return statement

# random lose statement
def random_lose_statement():
    r = random.randint(1,5)
    match r:
        case 1:
            statement = 'Ha I dont even have hands\nand I won! XD'
        case 2:
            statement = 'Like playing against\na baby... XD'
        case 3:
            statement = 'You kinda suck... XD'
        case 4:
            statement = 'Do you even know how\nto play? XD'
        case 5:
            statement = 'How many times do I have to\ntell you? Paper beats Rock beats\nScissors beats Paper! XD'
    return statement

# function to process results of user and computer choices
def result(user, comp):
    global user_score
    global comp_score
    global comp_hand
    global user_hand
    print('getting the results')
    # convert user and comp hands to numbers
    user = choice_to_number(user)
    comp = choice_to_number(comp)

    if(user==comp):
        print('tie')
        results_statement = 'User: ' + user_hand + '\nComp: ' + comp_hand + '\n\nTie\n\nUser Score: ' + str(user_score) + '\nComp Score: ' + str(comp_score)
    elif((user-comp)%3==1):
        print('user wins')
        user_score += 1
        results_statement = 'User: ' + user_hand + '\nComp: ' + comp_hand + '\n\nUser Wins\n' + random_win_statement() + '\n\nUser Score: ' + str(user_score) + '\nComp Score: ' + str(comp_score)
    else:
        print('comp wins')
        comp_score += 1
        results_statement = 'User: ' + user_hand + '\nComp: ' + comp_hand + '\n\nComp Wins\n' + random_lose_statement() + '\n\nUser Score: ' + str(user_score) + '\nComp Score: ' + str(comp_score)
    return results_statement

# function to create easy mode game
def EasyMode():
    '''
    For this mode, the computer's outcome will be comepletly randomized

    '''
    print('now in ' + mode + ' mode')

    global cap 
    global user_hand
    global comp_hand
    global user_score
    global user_score

    model = keras.models.load_model("rpsedge2.h5")

    CLASS_MAP =  {
        0: "rock",
        1: "paper",
        2: "scissors",
        3: "none"
    }

    def mapper(val):
        return CLASS_MAP[val]

    # SET THE COUNTDOWN TIMER
    # for simplicity we set it to 3
    # We can also take this as input
    TIMER = int(3)

    # Open the camera
    cap = cv2.VideoCapture(0)
    x1, y1 = 25, 25
    x2, y2 = 300, 300 

    while True:

        # Read and display frame 
        ret, frame = cap.read()
        # cv2.imshow('a', img)  
        if not ret:
            continue
        
        imAux = frame.copy()
        # Check for the pressed key 
        # Waits 125 miliseconds to see if someone pressed any key 
        # k = cv2.waitKey(125)

        # rectangle for user to play
        cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)

        thing = imAux[y1:y2, x1:x2]
        # thing = imutils.resize (thing, width = 100)
        
        # extract the region of image within the user rectangle
        player_move = frame[25:300, 25:300]
        img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img_blur = cv2.GaussianBlur(img, (3,3), 0)
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
        # predict the move made
        pred = model.predict(np.array([sobelxy]))
        player_move_code = np.argmax(pred[0])
        player_move_name = mapper(player_move_code)
        # print(user_move_name)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
       
        # set the key for the countdown to begin, here we set it as s 
        k = cv2.waitKey(10)
        if k == ord('s'):
            prev = time.time()

            while TIMER >=0:
                ret, img = cap.read()

                # Display countdown on each frame 
                # Specify the font and draw the coundown 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(TIMER),
                            (200, 250), font,
                            7, (0, 255, 255),
                            4, cv2.LINE_AA)
                cv2.imshow('Rock Paper Scissors', img)
                cv2.waitKey(10)

                # Current Time 
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrease the counter
                if cur-prev >= 1:
                    prev = cur
                    TIMER = TIMER-1

            else: 
                ret, frame = cap.read()

                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                # cv2.imshow('a', img)
                cv2.imshow('Rock Paper Scissors', frame)
 
                # time for which image displayed
                cv2.waitKey(1000)
 
                # Save the frame
                # cv2.imwrite('camera.jpg', frame)
                # This will capture the image that was just in the box 
                cv2.imwrite(Data +'/thing_{}.jpg'.format(photo_of_move),thing)

                ##################################################
                ################ More New Code ###################
                # extract the region of image within the user rectangle
                player_move = frame[25:300, 25:300]
                img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (224, 224))
                img_blur = cv2.GaussianBlur(img, (3,3), 0)
                sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
                # predict the move made
                pred = model.predict(np.array([sobelxy]))
                player_move_code = np.argmax(pred[0])
                player_move_name = mapper(player_move_code)
                #print(player_move_name)
                user_hand = player_move_name

                # use player's hand to begin game
                player_hand(user_hand)
                if user_hand is not '' and user_hand is not 'none':
                    r = result(user_hand, comp_hand) # calls on result function (returns string) 
                else:
                    print('please retry. now exiting game')
                    break

                print(r)
                
                # HERE we can reset the Countdown timer
                # if we want more Capture without closing
                # the camera

                ######## New Code ###########
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2

                y0, dy = 50, 30
                for i, line in enumerate(r.split('\n')):
                    y = y0 + i*dy
                    image = cv2.putText(frame, line, (50, y ), font, 1, color, thickness)

                #image = cv2.putText(frame, r, org, font, 1, color, thickness, cv2.LINE_AA)

                # cv2.waitKey(4000)

                # Displaying the image
                cv2.imshow('Rock Paper Scissors', image) 
                cv2.waitKey(5000)

                #################################################
                TIMER = 3



        elif k == ord('q'):
            break
        cv2.imshow("Rock Paper Scissors", frame)

    cap.release()
    cv2.destroyAllWindows()

# function to create hard mode game
def HardMode():
    '''
    For this mode, the computer will win every time. 
    '''
    global cap 
    global user_hand
    global comp_hand
    global user_score
    global user_score

    model = keras.models.load_model("rpsedge2.h5")

    print('now in ' + mode + ' mode')

    CLASS_MAP =  {
        0: "rock",
        1: "paper",
        2: "scissors",
        3: "none"
    }

    def mapper(val):
        return CLASS_MAP[val]

    # SET THE COUNTDOWN TIMER
    # for simplicity we set it to 5
    # We can also take this as input
    TIMER = int(3)

    # Open the camera
    cap = cv2.VideoCapture(0)
    x1, y1 = 25, 25
    x2, y2 = 300, 300 

    while True:

        # Read and display frame 
        ret, frame = cap.read()
        # cv2.imshow('a', img)  
        if not ret:
            continue
        
        imAux = frame.copy()
        # Check for the pressed key 
        # Waits 125 miliseconds to see if someone pressed any key 
        # k = cv2.waitKey(125)

        # rectangle for user to play
        cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)

        thing = imAux[y1:y2, x1:x2]
        # thing = imutils.resize (thing, width = 100)
        
        # extract the region of image within the user rectangle
        player_move = frame[25:300, 25:300]
        img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img_blur = cv2.GaussianBlur(img, (3,3), 0)
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
        # predict the move made
        pred = model.predict(np.array([sobelxy]))
        player_move_code = np.argmax(pred[0])
        player_move_name = mapper(player_move_code)
        # print(user_move_name)
        user_hand = player_move_name


        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
       
        # set the key for the countdown to begin, here we set it as s 
        k = cv2.waitKey(10)
        if k == ord('s'):
            prev = time.time()

            while TIMER >=0:
                ret, img = cap.read()

                # Display countdown on each frame 
                # Specify the font and draw the coundown 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(TIMER),
                            (200, 250), font,
                            7, (0, 255, 255),
                            4, cv2.LINE_AA)
                cv2.imshow('Rock Paper Scissors', img)
                cv2.waitKey(10)

                # Current Time 
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrease the counter
                if cur-prev >= 1:
                    prev = cur
                    TIMER = TIMER-1

            else: 
                ret, frame = cap.read()

                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                # cv2.imshow('a', img)
                cv2.imshow('Rock Paper Scissors', frame)
 
                # time for which image displayed
                cv2.waitKey(1000)
 
                # Save the frame
                # cv2.imwrite('camera.jpg', frame)
                # This will capture the image that was just in the box 
                cv2.imwrite(Data +'/thing_{}.jpg'.format(photo_of_move),thing)
                    
                ##################################################
                ################ More New Code ###################
                # extract the region of image within the user rectangle
                player_move = frame[25:300, 25:300]
                img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (224, 224))
                img_blur = cv2.GaussianBlur(img, (3,3), 0)
                sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
                # predict the move made
                pred = model.predict(np.array([sobelxy]))
                player_move_code = np.argmax(pred[0])
                player_move_name = mapper(player_move_code)
                #print(player_move_name)
                #################################################
                user_hand = player_move_name

                # use player's hand to begin game
                player_hand(user_hand)
                if user_hand is not '' and user_hand is not 'none':
                    r = result(user_hand, comp_hand) # calls on result function (returns string) 
                else:
                    print('please retry. now exiting game')
                    break
                print(r)

                # HERE we can reset the Countdown timer
                # if we want more Capture without closing
                # the camera

                ######## New Code ###########
                font = cv2.FONT_HERSHEY_SIMPLEX
                org = (50, 50)
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2

                y0, dy = 50, 30
                for i, line in enumerate(r.split('\n')):
                    y = y0 + i*dy
                    image = cv2.putText(frame, line, (50, y ), font, 1, color, thickness)

                #image = cv2.putText(frame, r, org, font, 1, color, thickness, cv2.LINE_AA)

                # cv2.waitKey(4000)

                # Displaying the image
                cv2.imshow('Rock Paper Scissors', image) 
                cv2.waitKey(5000)

                TIMER = 3



        elif k == ord('q'):
            break
        cv2.imshow("Rock Paper Scissors", frame)

    cap.release()
    cv2.destroyAllWindows()

# button to call on easy mode
def Easy():
    global cap 
    global mode
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    mode = 'Easy'
    print('Entering ' + mode + ' mode')
    EasyMode()

# button to call on hard mode
def Hard():
    global cap
    global mode
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    mode = 'Hard'
    print('Entering ' + mode + ' mode')
    HardMode()

cap = None 
root = Tk()

btnEasy = Button(root, text="Easy", width=45, command=Easy)
btnEasy.grid(column=0, row=0, padx=5, pady=5)

btnHard = Button(root, text="Hard", width=45, command=Hard)
btnHard.grid(column=1, row=0, padx=5, pady=5)

lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=2)

root.mainloop()