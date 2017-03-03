from webInterface import *
from board import Board
from random import random as random
debug = False
def findPath(b):
	for i in range(b.x):
		for j in range(b.y):
			if(not b.get(i,j)):
				b.reset()
				b.start(i,j)
				path = step(b,[])
				if path:
					return [i,j,path]

def step(b,stack = []):
	dirs = b.surround()
	if len(dirs) == 0:
		if(b.full()):
			return stack
		else:
			return False
	for d in dirs:
		stack.append(d)
		b.move(d)
		dead = b.checkDeadEnds()
		if dead:
			stack.pop()
			b.undo()
		else:
			r = step(b,stack)
			if r :
				return stack
			else :
				stack.pop()
				b.undo()
	return False

while 1:
	print("=======================")
	board = getPuzzle()
	board.debug = debug
	x,y,p = findPath(board)
	print(x,y,"".join(p))
	reply = sendSolution(x,y,p)
	if b'sucked' in reply:
		print(reply)
		break
