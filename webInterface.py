import urllib.request
from board import Board
def getPuzzle():
	getPuzzle = "http://www.hacker.org/coil/index.php?name=danzibob&password=Pass123"
	f = urllib.request.urlopen(getPuzzle)
	htmlStr = f.read()
	startIndex = htmlStr.index(b'FlashVars" value="') + 18
	htmlStr = htmlStr[startIndex:]
	endIndex = htmlStr.index(b'"')
	htmlStr = htmlStr[:endIndex]
	args = htmlStr.split(b'&')
	args = [i[i.index(b'=')+1:] for i in args]
	x = int(args[0])
	y = int(args[1])
	b = [[args[2][x*j + i] == 88 for i in range(x)] for j in range(y)]
	return Board(b,x,y)

def sendSolution(startX,startY,path):
	url = "http://www.hacker.org/coil/index.php?name=danzibob&password=Pass123&path={}&x={}&y={}"
	url = url.format("".join(path),startX,startY)
	f = urllib.request.urlopen(url)
	return f.read()
