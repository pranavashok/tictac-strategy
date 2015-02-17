relation = {1: 0, 2: 1, 3: 1, 4: 1, 5: 0, 6: 4}
class Tree(object):
	def __init__(self):
		self.parent = None
		self.data = None
		self.child = []
		self.win = None
	def add(self, node, parent):
		n = Tree()
		n.data = node
		p = self.search(parent)
		if p == None:
			p = self.add(parent, relation[parent])
		n.parent = p
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
	def update(self, node, winner):
		p = self.search(node)
		p.win = winner
	def _print(self):
		print(self.data)

root = Tree()
root.data = 0
t = root.add(1, 0)
t = root.add(3, 1)
t = root.add(4, 1)
t = root.add(9, 2)
print(root.data, root.child[0].data, root.child[0].child[1].data)