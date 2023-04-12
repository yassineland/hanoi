# import pygame library
import pygame

''' DRAWING CONFIGURATION '''

# Titre
title = "AND/OR Graph"
# Image path
# img_path = "img.jpg"
# Font size
police_name = 20
police_cost = 15
# Node width & height
wnode = 100
hnode = 20
# Space between childs
pas = 50
# Initialise configs
width = 900
height = 600
# Set title
pygame.display.set_caption(title)
# Set window dimensions
screen = pygame.display.set_mode((width, height))
# initialise the pygame font
pygame.font.init()
# Load fonts for future use
font1 = pygame.font.SysFont("comicsans", police_name)
font2 = pygame.font.SysFont("comicsans", police_cost)

''' KEYBOARD/MOUSE INPUT '''

def detect_exit():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

''' PREPARE TREE '''

class Node:
	def __init__(self, text, cost = 0, is_and = False):
		self.text = text
		self.cost = cost
		self.is_and = is_and

		self.parent = None
		self.childs = []
		self.neighbors = []
		self.cost_parent = None
		self.status = 0
		self.is_optimum = False
		self.solutionGraph = {}

	def add_child(self, lnode):
		for node in lnode:
			node.parent = self
		self.childs.append(lnode)

	def computeMinimumCostChildNodes(self): # Computes the Minimum Cost of child nodes of a given node v
		minimumCost = 0
		costToChildNodeListDict = {}
		costToChildNodeListDict[minimumCost] = []
		flag = True
		for lchild in self.childs: # iterate over all the set of child node/s
			cost = 0
			nodeList = []
			for child in lchild:
				# cost += h + edge_weight
				cost = cost + child.cost + 1
				nodeList.append(child)

			if flag == True:
				# initialize Minimum Cost with the cost of first set of child node/s
				minimumCost = cost
				costToChildNodeListDict[minimumCost] = nodeList # set the Minimum Cost child node/s
				flag = False
			else:
				# checking the Minimum Cost nodes with the current Minimum Cost
				if minimumCost>cost:
					minimumCost = cost
					costToChildNodeListDict[minimumCost] = nodeList # set the Minimum Cost child node/s
		
		return minimumCost, costToChildNodeListDict[minimumCost] # return Minimum Cost and Minimum Cost child node/s

	def aoStar(self, backTracking=False): # AO* algorithm for a start node and backTracking status flag
		print("HEURISTIC VALUES :", self.cost)
		# print("SOLUTION GRAPH :", self.solutionGraph)
		print("PROCESSING NODE :", self.text)
		# print("-----------------------------------------------------------------------------------------")
		
		# if status node v >= 0, compute Minimum Cost nodes of v
		if self.status >= 0:
			minimumCost, childNodeList = self.computeMinimumCostChildNodes()
			# print(minimumCost, childNodeList)
			
			self.cost = minimumCost
			self.status = len(childNodeList)
			# check the Minimum Cost nodes of v are solved
			solved = True
			
			for childNode in childNodeList:
				childNode.cost_parent = self
				if childNode.status != -1:
					solved = False
			
			# if the Minimum Cost nodes of v are solved, set the current node status as solved(-1)
			if solved == True:
				self.status = -1
				# update the solution graph with the solved nodes which may be a part of solution
				solutionGraph[self.text] = [child.text for child in childNodeList]
			
			# check the current node is the start node for backtracking the current node value
			if self.parent:
				# backtracking the current node value with backtracking status set to true
				self.cost_parent.aoStar(True)
			
			# check the current call is not for backtracking
			if backTracking == False:
				# for each Minimum Cost child node
				for childNode in childNodeList:
					# set the status of child node to 0 (needs exploration)
					childNode.status = 0
					# Minimum Cost child node is further explored with backtracking status as false
					childNode.aoStar(False)
		
'''
Yassine :- ali, saleh, amine
4
8
6
7
ali :- ahmed; taha
3
4
taha :- youssef, adem
6
4
'''
nodeA = Node("Yassine", 4)
nodeB = Node("ali", 6)
nodeC = Node("saleh", 5)
nodeD = Node("amine", 3)
nodeE = Node("ahmed", 7)
nodeF = Node("taha", 5)
nodeG = Node("youssef", 7)
nodeH = Node("adem", 8)
nodeX = Node("hamza", 1)
nodeY = Node("amir", 3)
nodeA.add_child([nodeB])
nodeA.add_child([nodeC, nodeD])
nodeB.add_child([nodeE, nodeF])
nodeF.add_child([nodeG])
nodeF.add_child([nodeH])
nodeH.add_child([nodeX, nodeY])
# nodeA.is_optimum = True
# nodeB.is_optimum = True
# nodeE.is_optimum = True
# nodeF.is_optimum = True
# nodeH.is_optimum = True

solutionGraph = {}
nodeA.aoStar()
print(solutionGraph)
'''
dnodes = {}
while True:
	in_rule = input("Rule : \n")
	if not in_rule:
		break

	sp = in_rule.split(":")
	
	# Get goal
	goal = sp[0].strip()
	
	# - already saved goal?
	if goal not in dnodes:
		# - make goal node
		node_goal = Node(goal)
		# - save the goal node
		dnodes[goal] = node_goal
	else:
		node_goal = dnodes[goal]

	# Get sub-goals
	subgoals = sp[1].strip().split(",")
	for i, subgoal in enumerate(subgoals):
		subgoal = subgoal.strip()
		# - make sub-goal node
		node_subgoal = Node(subgoal)
		# - add as (AND) with last sub-goal children
		if i:
			node_goal.childs[-1].set_and_neighbor(node_subgoal)
		# - add sub-goal as goal's children
		node_goal.add_child(node_subgoal)
		# - save the sub-goal node
		dnodes[subgoal] = node_subgoal

# Get costs
for node_name, node in dnodes.items():
	# - get input cost
	in_cost = input(f"Cost of {subgoal} = ")
	cost = int(in_cost or 0)
	# - set node cost
	node.cost = cost

# Get root node
nodeA = node_goal
while nodeA.parent:
	nodeA = nodeA.parent
'''

''' DRAW TREE '''

def draw_tree(node, x = width/2, y = pas+hnode):
	
	# Compute (x, y) of first children
	c_y = y + hnode + 50
	c_x = x-((len(node.childs)*wnode)/2)

	# Childrens
	for lchild in node.childs:
		for i, child in enumerate(lchild):
			if len(lchild)>1:
				# Arc (AND)
				pygame.draw.line(screen, (50, 200, 50), (x+(wnode/2), y), (c_x+(wnode/2), c_y), 2)
				if i+1<len(lchild):
					pygame.draw.line(screen, (50, 200, 50), (c_x+(wnode/2), c_y), (c_x+wnode+(wnode/2)+pas, c_y), 1)
			else:
				# Line (OR)
				pygame.draw.line(screen, (50, 50, 50), (x+(wnode/2), y), (c_x+(wnode/2), c_y), 1)

			# Draw children (recursively)
			draw_tree(child, c_x, c_y)
			# Increment x
			c_x += wnode+pas

	# Rectangle
	if node.is_optimum:
		# - Belong to optimum path?
		pygame.draw.rect(screen, (50, 150, 250), (x, y-(hnode/2)-5, wnode, hnode+10))
	else:
		# - Not in optimum path?
		pygame.draw.rect(screen, (210, 200, 0), (x, y-(hnode/2)-5, wnode, hnode+10))
	
	# Text name
	text = font1.render(node.text, 1, (0, 0, 0))
	screen.blit(text, (x+5, y-15))
	
	# Text cost
	text = font1.render(str(node.cost), 1, (250, 0, 0))
	screen.blit(text, (x+(wnode/2)+5, y-hnode-20))

''' MAIN '''
while True:
	detect_exit()
	screen.fill((255, 255, 255))

	# screen.blit(img_parts[m[i][j]-1], (j*stile, i*stile))

	draw_tree(nodeA)

	# Update window
	pygame.display.update()
