encoding = {}
rep = {}
relation = {}

#automorphims(config) - returns the representative of the class
#when given config
#	checks if config or its automorphisms have already been added
#		if yes, 
#			returns the rep
#		if no,
#			applies all the automorphisms to the config and adds to the encoding table, also to the rep table
#			returns the rep

def automorphisms(config): 
	aulist = ["741852963", "987654321", "369258147", "147258369", "789456123", "963852741"]
	encodings = []
	global encoding
	test = encode(config)
	if test in rep:
		return decode(rep[test])
	for au in aulist: #each automorphism
		morphed = ""
		for a in au: #each number
			morphed += config[int(a)-1]
		encodings.insert(0, encode(morphed))
		encoding[morphed] = encode(morphed)
	encoding[config] = encode(config)
	encodings.sort()
	for e in encodings:
		rep[e] = encodings[0]
	return decode(encodings[0])


#encode(config) - returns unique number for each configuration
def encode(config):
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	i = 0
	code = 1
	for c in config:
		code *= pow(primes[i], int(c))
		i += 1
	return code

#decode(e) - returns unique configuration for each encoding
def decode(e):
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
	i = 0
	code = e
	config = ""
	while(i < 9):
		count = 0
		while(code%primes[i] == 0):
			code/=primes[i]
			count+=1
		i+=1
		config+=str(count)
	return config

#convert(n) - converts 0 to blankspace, 1 to X and 2 to O
#helper function while printing in grid
def convert(n):
	if(n == 0):
		return " "
	elif(n == 1):
		return "X"
	else:
		return "O"

#printInGrid(config)
#prints the configuration as it appears on paper
def printInGrid(config):
	for i in range(0, 3):
		line = ""
		for j in range(0, 3):
			line += convert(int(config[i*3+j]))+" | "
		print(line+"\n")
	print("\n")

#play(config, turn) - returns next set of possible configurations along with parent
#if player X's turn,
#	draws X in all possible configurations and stores it in possible
#	calls automorphisms(p) to get unique configs of each p in possible
#	stores it in next along with its parent node
#if player O's turn,
#	does the same thing as player X, with O
#updates the relations assoc array
#returns set of unique configurations, parent of each config
def play(config, turn):
	global rep
	global relation
	next = {}

	if turn%2 == 0:
		possible = drawx(config)
		for p in possible:
			unique = automorphisms(p)
			if unique not in next:
				next.update({unique: config})
	else:
		possible = drawo(config)
		for p in possible:
			unique = automorphisms(p)
			if unique not in next:
				next.update({unique: config})

	relation.update(next)
	return next

#drawx(config) - returns possible additions of X
def drawx(config):
	i = 0
	possible = []
	for c in config:
		if c == "0":
			possible.append(config[:i]+"1"+config[i+1:])
		i+=1
	return possible

#drawo(config) - returns possible additions of O
def drawo(config):
	i = 0
	possible = []
	for c in config:
		if c == "0":
			possible.append(config[:i]+"2"+config[i+1:])
		i+=1
	return possible

#checkwin(config) - checks whether given config is a winning config and returns the player who wins
def checkwin(config):
	winning = ["200020002", "000000111", "222000000", "100100100", "200200200", "001001001", "111000000", "001010100", "002020200", "000000222", "100010001", "002002002"];
	for w in winning:
		player, win = intersect(config, w)
		if win:
			return player
	return 0

#intersect(config, w) - helper function to check whether there are 3 X's or O's in a line
def intersect(config, w):
	count = 0
	for i in range(0, 9):
		if(int(w[i]) != 0):
			if(config[i] == w[i]):
				count+=1
		if count == 3:
			return w[i], True
	return 0, False

class Tree(object):
	def __init__(self):
		self.parent = None
		self.data = None
		self.child = []
		self.win = "0"
	def add(self, node, parent):
		global relation
		n = Tree()
		n.data = node
		p = self.search(automorphisms(parent))
		if p == None:
			p = self.add(parent, relation[parent])
		n.parent = p
		n.win = checkwin(node)
		p.child.append(n)
		return n
	def search(self, node):
		if self.data == node:
			return self
		elif self.child == None:
			return None
		else:
			for c in self.child:
				res = c.search(node)
				if res != None:
					return res

root = Tree()

def main():
	current = {"000000000": "000000000"}
	global root
	root.data = "000000000"
	turn = 0
	s = False
	while(turn < 8):
		next = {}
		for c in current:
			p = checkwin(c)
			if p:
				#print("\n\nWinning "+str(p))
				#printInGrid(c)
				#print(c)
				n = c
				for j in range(0, turn):
					n = relation[n]
					#print(n)
			next.update(play(c, turn))
		current = next
		for c in current:
			root.add(c, current[c])
		turn+=1

main()

def dfs(tree, level):
	if tree.child == []:
		if tree.win != 0:
			pass
			#print("P"+str(tree.win))
	for each in tree.child:
		#print(level, each.data, each.win)
		if (each.win == "1" and level%2 == 0) or (each.win == "2" and level%2 == 1):
			tree.win = each.win
			break
		dfs(each, level+1)

def propogate(tree, level):
	stack = []
	stack.push(tree)
	if tree.child != []: #non-leaf node
		while stack != []:
			t = stack.pop()
			for c in t.child:
				stack.push(c)
	

def bfs(tree):
	if tree.child != []:
		print("{\"name\": \""+tree.data+"\", \"children\": [")
		for each in tree.child:
			bfs(each)
		print("]},")
	else:
		print("{\"name\": \""+tree.data+"\", \"size\": "+str(int(tree.win)*2000+1000)+"},")

dfs(root, 0)
#propogate(root, 0)
bfs(root)
#dfs(root, 0)
#drawx("002000000")