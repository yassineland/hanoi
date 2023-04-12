from time import sleep
from draw import *

''' PARAMETERS '''

# Represent the main problem: number of disks to move, source and destination (using letters A, B, or C)
NB_DISKS = 3
SOURCE = 'A'
DESTINATION = 'C'

''' CLASSES '''

class Node:
    def __init__(self, text):
        # Node attributes

        self.text = text
        self.parent = None
        self.childs = []

        # + just for display
        self.x = 0
        self.y = 0

    def add_child(self, node):
        # Add a children to the node
        self.childs.append(node)
        node.parent = self

''' INIT '''

# Initialize the sequence of actions by declaring 'actions' as an empty list
actions = []

''' FUNCTIONS '''

# Find an auxiliary location
def find_aux(source, destination):
    # Function that finds an auxiliary location (A/B/C) different from the source and destination.

    # Method 1
    for place in ['A', 'B', 'C']:
        if place!=source and place!=destination:
                return place

    # Method 2
    """
    if 'A'!=source and 'A'!=destination:
        return 'A'
        
    if 'B'!=source and 'B'!=destination:
        return 'B'
        
    return 'C'
    """

# Recursive function to generate the AND tree of subproblems.
def move(disques, source, destination, parent=None):

    # Tree
    node = Node(f"{disques}{source}{destination}")
    if parent:
        parent.add_child(node)

    # Algorithm

    # Find an auxiliary location that is different from the source and destination
    auxiliaire = find_aux(source, destination)

    # Condition: if the number of disks to move is equal to 1.
    if disques==1:
        # - Is it a terminal node? Add the action to the sequence
        
        # Add the action [source, destination] to the sequence of actions (actions)
        actions.append([source, destination])

    else:
        # - Apply this function to 3 subproblems (taking the node as the parent):
    
        # Move 'number of disks'-1 from source to auxiliary
        move(disques-1, source, auxiliaire, node)

        # Move 1 disk from source to destination
        move(1, source, destination, node)

        # Move 'number of disks'-1 from auxiliary to destination
        move(disques-1, auxiliaire, destination, node)

    return node

''' MAIN '''

# Play manually!
"""
# init
from_place = ""
# run
while True:
    screen.fill((255, 255, 255))
    place = detect_keyboard()

    # Draw disks
    draw_hanoi(NB_DISKS, from_place)

    # Do action
    if place:
        if from_place:
            move_list(from_place, place)
            from_place = ""
        else:
            from_place = place

    # Update window
    pygame.display.update()
"""

# Call the 'move' function on the main problem (3 arguments: number of disks & source & destination). Result in 'node'.
node = move(NB_DISKS, SOURCE, DESTINATION)

''' DRAW '''

# Show tree & actions (animation)
for i, action in enumerate(actions):
    if detect_exit():
        break

    screen.fill((255, 255, 255))

    # Draw the tree
    draw_tree(node, i-1)
    # Draw the disks
    draw_hanoi(NB_DISKS)

    # Update window
    pygame.display.update()

    # Edit the list of disks
    move_list(action[0], action[1])
    sleep(1)

# Show tree & actions
while True:
    if detect_exit():
        break

    screen.fill((255, 255, 255))

    # Draw the tree
    draw_tree(node, len(actions)-1)
    # Draw the disks
    draw_hanoi(NB_DISKS)

    # Update window
    pygame.display.update()
