from copy import deepcopy as copy
import logging

class Board():

	def __init__(self,b,x,y):
		self.originalBoard = b
		self.board = copy(self.originalBoard)
		self.x = x
		self.y = y
		self.cur = None
		self.undoStack = []
		self.debug = False
		self.originalStates, self.originalStateCounts = self.checkDeadEnds()
		self.states = copy(self.originalStates)
		self.stateCounts = copy(self.originalStateCounts)

	def get(self,x,y):
		if (-1 < x and x < self.x) and (-1 < y and y < self.y):
			return self.board[y][x]
		else:
			return True

	def exists(self,x,y):
		return (-1 < x and x < self.x) and (-1 < y and y < self.y)

	def set(self,x,y,val):
		if (-1 < x and x < self.x) and (-1 < y and y < self.y) and (val == True  or val == False):
			self.board[y][x] = val

	def surround(self,alt = False):
		if(not alt):
			x,y = self.cur
		else:
			x,y = alt
		s = ''
		if(not self.get(x,y-1)):
			s += 'U'
		if(not self.get(x,y+1)):
			s += 'D'
		if(not self.get(x-1,y)):
			s += 'L'
		if(not self.get(x+1,y)):
			s += 'R'
		return list(s)

	def getOrder(self,x,y):
		return len(self.surround([x,y]))

	def reset(self):
		self.board = copy(self.originalBoard)
		self.cur = None
		self.states = copy(self.originalStates)
		self.stateCounts = copy(self.originalStateCounts)
		#logging.debug("RESETTING")
		#printStates(self)

	def start(self,x,y):
		self.cur = [x,y]
		self.set(x,y,True)
		self.stateWall(x,y)
		toCheck = [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]
		self.updateDeadEnds(toCheck)

	def move(self,dir):
		self.undoStack.append(self.cur)
		x = self.cur[0]
		y = self.cur[1]
		toCheck = []
		self.set(x,y,True)
		if(dir == "U"):
			while(not self.get(x,y-1)):
				y -= 1
				self.set(x,y,True)
				self.stateWall(x,y)
				toCheck.extend([[x-1,y],[x+1,y]])	
		elif(dir == "D"):
			while(not self.get(x,y+1)):				
				y += 1
				self.set(x,y,True)
				self.stateWall(x,y)
				toCheck.extend([[x-1,y],[x+1,y]])
		elif(dir == "L"):
			while(not self.get(x-1,y)):
				x -= 1
				self.set(x,y,True)
				self.stateWall(x,y)
				toCheck.extend([[x,y-1],[x,y+1]])
		elif(dir == "R"):
			while(not self.get(x+1,y)):
				x += 1
				self.set(x,y,True)
				self.stateWall(x,y)
				toCheck.extend([[x,y-1],[x,y+1]])
		self.cur = [x,y]
		self.updateDeadEnds(toCheck)
		return self.stateCounts[0] + self.stateCounts[1] > 2

	def stateWall(self,x,y):
		currentState = self.states[x+y*self.x]
		self.stateCounts[currentState] -= 1
		self.stateCounts["X"] += 1
		self.states[x+y*self.x] = "X"

	def firstEmpty(self):
		for i in range(self.x):
			for j in range(self.y):
				if(not self.get(i,j)):
					return [i,j]
				else:
					return False

	def checkSplit(self):
		b = copy(self)
		cur = b.firstEmpty()
		if(not cur):
			return False
		b.set(*cur,True)
		stack = []
		stack.append(cur)
		while len(stack) > 0 and stack != [None]:
			i = len(stack) - 1
			x,y = stack[i]
			if(not b.get(x,y+1)):
				b.set(x,y+1,True)
				stack.append([x,y+1])
			if(not b.get(x,y-1)):
				b.set(x,y-1,True)
				stack.append([x,y-1])
			if(not b.get(x-1,y)):
				b.set(x-1,y,True)
				stack.append([x-1,y])
			if(not b.get(x+1,y)):
				b.set(x+1,y,True)
				stack.append([x+1,y])
			del stack[i]
		return not b.full()

	def checkDeadEnds(self):
		l = []
		for j in range(self.y):
			for i in range(self.x):
				if not self.get(i,j):
					l.append(self.getOrder(i,j))
				else:
					l.append("X")
		c = {0:0,1:0,2:0,3:0,4:0,"X":0}
		for key in c:
			c[key] = l.count(key)
		return l,c

	def updateDeadEnds(self,toCheck):
		if self.stateCounts[0] == 1 and self.stateCounts[1] == 0:
			return
		#logging.debug(self)
		#printStates(self)
		indexes = [x + self.x*y if not self.get(x,y) else None for x,y in toCheck]
		for i in indexes:
			if(i != None and self.states[i] != "X"):
				self.stateCounts[self.states[i]] -= 1
				self.states[i] -= 1
				self.stateCounts[self.states[i]] += 1
		#printStates(self)

	def undo(self):
		#logging.debug("================================================================")
		#logging.debug("Resetting states after backtrack:")
		#logging.debug(self)
		target = self.undoStack.pop()
		dx = self.cur[0] - target[0] 
		dy = self.cur[1] - target[1]
		x,y = self.cur
		while dx != 0:
			self.set(x,y,False)
			if dx > 0:
				x -= 1
				dx -= 1
			else:
				x += 1
				dx += 1
		while dy != 0:
			self.set(x,y,False)
			if dy > 0:
				y -= 1
				dy -= 1
			else:
				y += 1
				dy += 1
		self.cur = [x,y]
		
		self.states, self.stateCounts = self.checkDeadEnds()
		#logging.debug(self)
		#printStates(self)

	def __str__(self):
		return toString(self.board,self.cur)

	def full(self):
		return all([all(i) for i in self.board])

def toString(board,current,stack = []):
	s = ''
	for row in board:
		s += " ".join(["■" if i else "□" for i in row]) + "\n"
	if(current != None):
		index = 2*(current[0] + current[1]*len(board[0]))
		s = s[:index] + "●" + s[index+1:]
	if(len(stack) > 0):
		for i in stack:
			index = 2*(i[0] + i[1]*len(board[0]))
			s = s[:index] + "X" + s[index+1:]

	return "\n" + s[:-1]

def printStates(b):
	for i in range(0,b.x*b.y,b.x):
		logging.debug(" ".join(list(map(str,b.states[i:i+b.x]))))
	logging.debug(b.stateCounts)