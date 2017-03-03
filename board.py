from copy import deepcopy as copy

class Board():

	def __init__(self,b,x,y):
		self.originalBoard = b
		self.board = copy(self.originalBoard)
		self.x = x
		self.y = y
		self.cur = None
		self.undoStack = []
		self.debug = False

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
		return len(surround())

	def reset(self):
		self.board = copy(self.originalBoard)
		self.cur = None

	def start(self,x,y):
		self.cur = [x,y]
		self.set(x,y,True)

	def move(self,dir):
		self.undoStack.append(self.cur)
		x = self.cur[0]
		y = self.cur[1]
		broken = False
		if(dir == "U"):
			while(not self.get(x,y-1)):
				self.set(x,y,True)
				y -= 1
		elif(dir == "D"):
			while(not self.get(x,y+1)):				
				self.set(x,y,True)
				y += 1
		elif(dir == "L"):
			while(not self.get(x-1,y)):
				self.set(x,y,True)
				x -= 1
		elif(dir == "R"):
			while(not self.get(x+1,y)):
				self.set(x,y,True)
				x += 1
		self.set(x,y,True)
		self.cur = [x,y]
		return broken

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

	def undo(self):
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

	return s[:-1]