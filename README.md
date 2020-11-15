# 667_project
The project for CIS667, Introduction to Artificial Intelligence

# Requirements
Python 3.x<br/>
Numpy

# Pattern
Player vs AI

# How ro run
Put main.py and treenew.py in the same directory and then open the terminal and type 'python main.py'<br/>
![alt text](Screenshots/initial.png)<br/>
It requires you to type a number to decide the board size (If size selected is smaller than 5, there will be a warning that there will be no winner).<br/>
And it also needs you to choose an AI type. Tree AI is what our team designed and baseline AI chooses actions uniformly at random.<br/>
Then a hint will be displayed that '-' marks in the board are valid actions.<br/>
Then player1 should put their stone. Simply type two number separated with space, such as:<br/>
![alt text](Screenshots/player1.png)<br/>
It input 5 5 and a stone 'x' has been put on (5,5) position on the board.<br/>
Then it is AI turn. AI will calculate the score and choose the position with the highest score so far.<br/>
Follow the same steps, after several rounds, we can see, for instance:<br/>
![alt text](Screenshots/winner.png)<br/>
When player1 put stone on (2,1), he will be the winner since he get 5 stones in a row<br/>
