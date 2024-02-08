# Rock Paper Scissor Game

This is a simple rock paper scissor game implemented in Python using OpenCV and MediaPipe libraries. The game captures webcam input to detect hand gestures, allowing players to make their moves. The game includes a simple musical chime note using the pygame library.

## Prerequisites
Python version 3.7 to 3.10

## Note: Make sure to use the specified Python version, as mediapipe may not work with other versions.
How to Play

Run the script using a Python interpreter:
```bash
python main.py
```
The webcam feed will start, and the game will begin after a countdown.
Show your hand gestures to make a move:
Fist: Rock
Five Fingers: Paper
Two Fingers Up: Scissors

The game will display the computer's move, and the winner of each round will be determined.
The scores for the player and computer will be shown on the screen.
The game ends when one of the players reaches the maximum score (change maxScore variable in the script).
Additional Information

The pygame library is used to play a musical chime note during the game.
Modify the maxScore variable in the script to set the score at which the game should end.
Ensure your webcam is properly connected and accessible by the script.
Thank you for checking out this project! We hope you enjoy playing the Rock Paper Scissor game. If you have any issues or suggestions, feel free to reach out. Have fun!
