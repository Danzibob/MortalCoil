from webInterface import *
from board import Board
from copy import deepcopy as copy
from random import random as random
import logging
from multiprocessing import Queue, Process, freeze_support
from time import sleep
logging.basicConfig(level=logging.DEBUG,format='[%(levelname)s] (%(processName)-10s) %(message)s',)

debug = False
def findPath(b,toCheck):
	for i in range(b.x):
		for j in range(b.y):
			if(not b.get(i,j)):
				toCheck.put([i,j])

def worker(board,q,out,end,ended):
	logging.debug("Starting Thread")
	b = copy(board)
	while end.empty() and not q.empty():
		start = q.get()
		logging.debug("working on ({},{})".format(*start))
		b.reset()
		b.start(*start)
		path = step(b,[])
		if path:
			out.put([start,path])
	ended.put("Finished")
	logging.debug("Ending Thread")

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

def cleanUp(threads,output,end,toCheck,ended):
	for i in range(4):
		threads[i].join()
	#print("Cleaning up")
	while not output.empty():
			try:
				toCheck.get(timeout=1)
			except:
				break
	#print("Cleared output")
	while not end.empty():
			try:
				end.get(timeout=1)
			except:
				break
	#print("Cleared end")
	while not toCheck.empty():
			try:
				toCheck.get(timeout=1)
			except:
				break
	#print("Cleared toCheck")
	for i in range(4):
		ended.get()
		#print("{} threads cleaned up".format(i))

def main():
	while 1:
		print("=======================")
		toCheck = Queue()
		output = Queue()
		end = Queue()
		ended = Queue()
		threads = []
		board = getPuzzle()
		for i in range(4):
			threads.append(Process(name="Thread "+str(i),target=worker,args = (board,toCheck,output,end,ended,)))
		findPath(board,toCheck)
		for i in range(4):
			threads[i].start()

		o = output.get()

		cleanUp(threads,output,end,toCheck,ended)
		del board
		del threads
		del toCheck
		del output
		del end
		del ended

		s,p = o
		print(*s,"".join(p))
		reply = sendSolution(*s,p)
		if b'sucked' in reply:
			print(reply)
			break
	

if __name__ == '__main__':
	freeze_support()
	main()

