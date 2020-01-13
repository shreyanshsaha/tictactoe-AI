import sys
import time
import copy
from random import choice, randint

playerPeg = ['X', 'O']
board=[['.','.','.'], ['.','.','.'], ['.','.','.']]
positions = [(x, y) for x in [0, 1, 2] for y in [0, 1, 2]]

# Print board
def printBoard(board):
	print("\n\nBOARD")
	print("-"*10)
	for row in board:
		for cell in row:
			print(cell, end=' ')
		print()
	print("-"*10)

# Make the user or AI play
def playPlayer(playerID):
	if len(positions) < 1:
		return

	# if playerID==0:
	# 	position = tuple(map(int, input('Enter position: ').split(' ')))
	# 	print(position)
	# 	if position not in positions:
	# 		print("Invalid position")
	# 		playPlayer(playerID)
	# 		return
	# 	positions.remove(position)
	# 	board[position[0]][position[1]] = playerPeg[playerID]
	# 	return

	# Get winning position
	winPosition = getWinningPosition(board, playerID)
	if len(winPosition)>0:
		position = winPosition
	else:
		position = choice(positions)

	positions.remove(position)
	board[position[0]][position[1]] = playerPeg[playerID]

# Check if player won
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

# Count current pegs of playerID on board
def countPegs(pegBoard, playerID):
	# print('Peg Count')
	# printBoard(pegBoard)
	count=0
	for row in pegBoard:
		for cell in row:
			if cell == playerPeg[playerID]:
				count+=1
	# print(count)
	return count

# Calculate all positions
def positionWins(permBoard, playerID, positions):
	if didPlayerWin(permBoard, playerID):
		pegCount = countPegs(permBoard, playerID)
		return pegCount

	for position in positions:
		tempBoard = copy.deepcopy(permBoard)
		tempPositions = copy.deepcopy(positions)
		tempPositions.remove(position)
		tempBoard[position[0]][position[1]] = playerPeg[playerID]

		return min(positionWins(tempBoard, playerID, tempPositions), positionWins(permBoard, playerID, tempPositions))

	return 20000

def sortValue(x):
	return x[1]

# Get the best position
def getWinningPosition(board, playerID):
	# Check if we win in one step
	for position in positions:
		tempBoard = copy.deepcopy(board)
		# Place a peg on the board
		tempBoard[position[0]][position[1]] = playerPeg[playerID]
		if didPlayerWin(tempBoard, playerID):
			if board[position[0]][position[1]]!=playerPeg[playerID]:
				print('One Step Winning position:',position)
				return position

	# Check if opponent is winning
	for position in positions:
		tempBoard = copy.deepcopy(board)
		# Place a peg on the board
		tempBoard[position[0]][position[1]] = playerPeg[1-playerID]
		if didPlayerWin(tempBoard, 1-playerID):
			if board[position[0]][position[1]]!=playerPeg[1-playerID]:
				print('Opponent Winning position:',position)
				return position

	# Calculate next best position based on recursion
	winningPositions=[]
	for position in positions:
		tempBoard = copy.deepcopy(board)
		tempPositions = copy.deepcopy(positions)
		tempPositions.remove(position)
		# Place a peg on the board
		tempBoard[position[0]][position[1]] = playerPeg[playerID]
		if didPlayerWin(tempBoard, playerID):
			return position
		# Calculate how many steps it will take to win
		steps = positionWins(tempBoard, playerID, tempPositions)
		if steps:
			winningPositions.append((position, steps))

	
	winningPositions.sort(key=sortValue)

	smallestValue = winningPositions[0][1]
	possiblePositions = []
	for position in winningPositions:
		if position[1]>smallestValue:
			break
		possiblePositions.append(position[0])

	# Print all positions and their steps
	print('\nPositions:',winningPositions, '\n', possiblePositions)
	if len(winningPositions)>0:
		return choice(possiblePositions)
	
	# If no position wins
	return []


if __name__=='__main__':
	currentPlayer = 0
	printBoard(board)
	while len(positions) > 0:
		print("Current player: ", playerPeg[currentPlayer], end='')
		if currentPlayer==1 or currentPlayer==0:
			dots = 0
			while dots<3:
				dots+=1
				sys.stdout.write('.')
				sys.stdout.flush()
				time.sleep(randint(3, 5)/10)
		playPlayer(currentPlayer)
		printBoard(board)
		if didPlayerWin(board, currentPlayer):
			time.sleep(1)
			print("Player", playerPeg[currentPlayer],"wins!")
			exit(0)
		currentPlayer = 1 - currentPlayer

	time.sleep(1)
	if didPlayerWin(board, 0):
		print("Player", playerPeg[0],"wins!")
	elif didPlayerWin(board, 1):
		print("Player", playerPeg[1],"wins!")
	else:
		print("DRAW")


