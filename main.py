import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import mediapipe as mp
import time
import pygame  # Import the pygame library

cap = cv2.VideoCapture(0)  # webcam capture
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [ai, player]
playerMove = None
imgAI = None  # Initialize imgAI
maxScore = 3

# Initialize pygame
pygame.init()
pygame.mixer.init()

def play_mp3(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Flag to track whether foul.mp3 has been played
foul_sound_played = False

while True:
    imgBg = cv2.imread('Resources/bg.png')  # background image
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.935, 0.935)
    imgScaled = imgScaled[:, 99:500]

    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:  # count till 3 before starting the game
            timer = time.time() - initialTime
            cv2.putText(imgBg, str(int(timer)), (600, 520), cv2.FONT_HERSHEY_PLAIN, 6, (157, 117, 203), 8)

            if timer > 3:  # start the game at the count of 3
                stateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:  # stone
                        playerMove = 1
                    elif fingers == [1, 1, 1, 1, 1]:  # paper
                        playerMove = 2
                    elif fingers == [0, 1, 1, 0, 0]:  # scissor
                        playerMove = 3
                    else:
                        if not foul_sound_played:
                            play_mp3('Resources/foul.mp3')
                            foul_sound_played = True
                        playerMove = 0
                        print("Please Show the right sign")

                    if playerMove != 0:
                        randomNumber = random.randint(1, 3)
                        imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                        play_mp3('Resources/move.mp3')
                        foul_sound_played = False  # Reset the flag
                        # player wins
                        if (playerMove == 1 and randomNumber == 3) or \
                                (playerMove == 2 and randomNumber == 1) or \
                                (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1

                        # ai wins
                        if (playerMove == 3 and randomNumber == 1) or \
                                (playerMove == 1 and randomNumber == 2) or \
                                (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1

                        # Play the MP3 when imgAI is displayed

                    print(fingers)
                    print(playerMove)

    imgBg[320:769, 790:1191] = imgScaled

    if playerMove is None:
        imgError = None
    elif playerMove == 0:
        if not foul_sound_played:
            play_mp3('Resources/foul.mp3')
            foul_sound_played = True
        imgError = cv2.imread('Resources/error.png', cv2.IMREAD_UNCHANGED)
        imgBg = cvzone.overlayPNG(imgBg, imgError, (300, 250))
    else:
        imgError = None

    if stateResult and imgAI is not None and imgError is None and scores != [0, 0]:
        imgBg = cvzone.overlayPNG(imgBg, imgAI, (150, 360))  # AI hand will stay

    # ai score
    cv2.putText(imgBg, str(scores[0]), (400, 275), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 6)

    # player score
    cv2.putText(imgBg, str(scores[1]), (1120, 275), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 255), 6)

    # Check if either player has reached a score of 2
    if scores[0] >= maxScore:
        win_img = cv2.imread('Resources/lose.png', cv2.IMREAD_UNCHANGED)
        imgBg = cvzone.overlayPNG(imgBg, win_img, (300, 250))
        cv2.imshow("Rock Paper Scissor", imgBg)
        key = cv2.waitKey(0)
        if key == ord(' '):  # space to reset scores
            scores = [0, 0]

    elif scores[1] >= maxScore:
        lose_img = cv2.imread('Resources/win.png', cv2.IMREAD_UNCHANGED)
        imgBg = cvzone.overlayPNG(imgBg, lose_img, (300, 250))
        cv2.imshow("Rock Paper Scissor", imgBg)
        key = cv2.waitKey(0)
        if key == ord(' '):  # space to reset scores
            scores = [0, 0]
            foul_sound_played = False

    cv2.imshow("Rock Paper Scissor", imgBg)

    key = cv2.waitKey(1)
    if key == ord(' '):  # space to start the game
        playerMove = None
        startGame = True
        foul_sound_played = False
        initialTime = time.time()
        stateResult = False

# Quit pygame and release resources when the program exits
pygame.mixer.quit()
pygame.quit()
