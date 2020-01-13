import sys
import time
import copy
from random import choice, randint

playerPeg = ['X', 'O']
board=[['.','.','.'], ['.','.','.'], ['.','.','.']]
positions = [(x, y) for x in [0, 1, 2] for y in [0, 1, 2]]

def printBoard(board):
	print("\n\nBOARD")
	print("-"*10)
	for row in board:
		for cell in row:
			print(cell, end=' ')
		print()
	print("-"*10)

def playPlayer(playerID):
	if len(positions) < 1:
		return
	
	# Get winning position
	winPosition = getWinningState(board, playerID)
	if len(winPosition)>0:
		position = winPosition
	else:
		position = choice(positions)

	positions.remove(position)
	board[position[0]][position[1]] = playerPeg[playerID]

def didPlayerWin(board, playerID):
	# Check rows
	for row in board:
		count = 0
		for cell in row:
			if cell==playerPeg[playerID]:
				count+=1
		if count==3:
			# print("Row win")
			return True

	# Check cols
	for i in range(3):
		count = 0
		for j in range(3):
			if board[j][i]==playerPeg[playerID]:
				count+=1
		if count==3:
			# print("Col win")
			return True

	# Check left diag
	count=0
	for i in range(3):
		if board[i][i]==playerPeg[playerID]:
			count+=1
		if count==3:
			# print("LD win")
			return True

	# Check right diag
	count=0
	for i in range(3):
		if board[i][2-i]==playerPeg[playerID]:
			count+=1
		if count==3:
			# print("RD win")
			return True
	return False

def getWinningState(board, playerID):
	# Place playerPeg in every position and 
	# get return the winning state if found

	for position in positions:
		tempBoard = copy.deepcopy(board)
		# Place a peg on the board
		tempBoard[position[0]][position[1]] = playerPeg[playerID]
		if didPlayerWin(tempBoard, playerID):
			print('\nWinning position:',position)
			return position

	# No winning state
	return []

if __name__=='__main__':
	currentPlayer = 0
	printBoard(board)
	while len(positions) > 0:
		print("Current player: AI", playerPeg[currentPlayer], end='')
		dots = 0
		while dots<3:
			dots+=1
			sys.stdout.write('.')
			sys.stdout.flush()
			time.sleep(randint(3, 8)/10)
		playPlayer(currentPlayer)
		printBoard(board)
		if didPlayerWin(board, currentPlayer):
			time.sleep(1)
			print("Player", playerPeg[currentPlayer],"wins!")
			exit(0)
		currentPlayer = 1 - currentPlayer

	printBoard(board)
	time.sleep(1)
	if didPlayerWin(board, 0):
		print("Player", playerPeg[0],"wins!")
	elif didPlayerWin(board, 1):
		print("Player", playerPeg[1],"wins!")
	else:
		print("DRAW")


