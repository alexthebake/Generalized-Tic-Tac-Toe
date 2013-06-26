Generalized Tic-Tac-Toe
=======================

This program lets you play generalized tic-tac-toe with a computer player.
By "generalized" I mean that you can play more than just the typical formulation of tic-tac-toe.
That is, you could play 4x4, 5x5, or even some sort of 3D model of tic-tac-toe (with the proper game file).

The program takes a text file as input where the format of the text file is as follows:

The first line consists only of the total number of nodes, and every following line is a winning path, where the path is defined by a space delimited list of nodes, each labeled by the number representing the corresponding node (where the first node on the board starts with 1).


**Usage: python ttt.py [game_file]**

*Note: If no game_file is provided, the program will default to nine.txt, the usual 3x3 tic-tac-toe game.*
