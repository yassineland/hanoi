# import pygame library
import pygame
import random

''' DRAWING CONFIGURATION '''

# Titre
title = "AND Graph (Hanoi)"
# Initialise configs
width = 900
height = 700
# Set title
pygame.display.set_caption(title)
# Set window dimensions
screen = pygame.display.set_mode((width, height))
# initialise the pygame font
pygame.font.init()
# Load fonts for future use
font1 = pygame.font.SysFont("comicsans", 20)
font2 = pygame.font.SysFont("comicsans", 12)

''' DRAWING TREE CONFIGURATION '''

# Node width & height
wnode = 25
hnode = 20
# Tree height
tree_height = 250

''' DRAWING HANOI CONFIGURATION '''

# peg names
peg_names = ["A", "B", "C"]
# margin
marge_hanoi = 50
# width & height stick
wstick = 5
hstick = 300
# height disk
hdisk = 20
# max width disk
max_wdisk = 230
# max number of disks initiate
nbdisks = 0
# width & color disks initiate
wdisk = []
color_disk = []
# (x, y) for Disks
cordDisk = []
cordDisk.append((200, height-hdisk-marge_hanoi-tree_height))
cordDisk.append(((width/2)-wstick, height-hdisk-marge_hanoi-tree_height))
cordDisk.append((width-200, height-hdisk-marge_hanoi-tree_height))

# (x, y) for sticks
cordStick = []
for i in range(len(cordDisk)):
    cordStick.append((cordDisk[i][0]-(wstick/2), height-hstick-marge_hanoi-tree_height))

# variable to map place name into index
place2i = {}
for i in range(len(peg_names)):
    place2i[peg_names[i]] = i

# list will be filled by disks' informations
disks_list = []

''' KEYBOARD/MOUSE INPUT '''

def detect_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# detect keyboard press
def detect_keyboard():

    # Loop through the events stored in event.get()
    for event in pygame.event.get():

        # Get if key pressed
        if event.type == pygame.KEYDOWN:
        
            # Arrow key (return the direction)
            if event.key == pygame.K_a:
                return "A"
            if event.key == pygame.K_b:
                return "B"
            if event.key == pygame.K_c:
                return "C"
        else:
            # If exit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    return ""

''' DRAW HANOI '''

# Fill disks' informations
def fill_disk_conf(disks_list, nb_disks):
    # fill width & colors
    for i in range(nb_disks):
        wdisk.append(max_wdisk * ((i+1) / nb_disks))
        color_disk.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))

# Draw Hannoi
def draw_hanoi(nb_disks, sel_from_place=None):

    # list of disks is not yet filled?
    if not disks_list:
        # fill disks information
        fill_disk_conf(disks_list, nb_disks)
        # fill list of disks
        disks_list.extend([list(sorted(range(nb_disks), reverse=True)), [], []])

    # base
    pygame.draw.rect(screen, (210, 200, 0), (0, cordDisk[0][1]+hdisk, width, 50))
    
    # draw pegs
    for i in range(len(peg_names)):
        # - Choose text color (selected or not)?
        color = (0, 0, 0)
        if sel_from_place and place2i[sel_from_place]==i:
            color = (250, 0, 0)
        # - Text
        text = font1.render(peg_names[i], 1, color)
        screen.blit(text, (cordStick[i][0], cordDisk[i][1]+hdisk+10))
        # - Stick
        pygame.draw.rect(screen, (210, 200, 0), (cordStick[i][0], cordStick[i][1], wstick, hstick))
        y = cordDisk[i][1]
        for disk in disks_list[i]:
            # - Disk
            pygame.draw.rect(screen, color_disk[disk], (cordDisk[i][0]-(wdisk[disk]/2), y, wdisk[disk], hdisk))
            y -= hdisk

# Change the list of disks according to action
def move_list(peg1, peg2):
    # convert places to indices (e.g.: A -> 0, B -> 1, ..)
    peg1 = place2i[peg1]
    peg2 = place2i[peg2]

    # do nothing if there is no disks in peg1
    if not disks_list[peg1]:
        return disks_list
    # don't put a disk above smaller one
    if disks_list[peg2] and disks_list[peg2][-1] < disks_list[peg1][-1]:
        return disks_list

    take = disks_list[peg1].pop()
    disks_list[peg2].append(take)

''' DRAW TREE '''

# recursively organize nodes according to their depth
def rec_tree_depth(root):

    # initially, we have one depth list (depth 0) contains only the root node
    deph2nodes = [[root]]

    while deph2nodes[-1]:
        # - get the last depth list
        nodes = deph2nodes[-1]
        # - add an empty list (new depth)
        deph2nodes.append([])
        # - add childs of the last depth list in the empty list
        for node in nodes:
            deph2nodes[-1].extend(node.childs)

    # delete the empty list
    deph2nodes.pop()
    return deph2nodes

# recursive draw tree
def rec_draw_tree(node, num_act=-1):
    global num_leaf
    
    # Rectangle
    if node.childs:
        # - have childrens? it's not a terminal node (need to be reduced)
        pygame.draw.rect(screen, (250, 220, 50), (node.x, node.y, wnode, hnode))
        
    else:
        # - don't have childrens? belong to the solution (sequence of actions)
        if num_act>=0 and num_leaf==num_act:
            # - it is the next action? (different color 1)
            pygame.draw.rect(screen, (250, 150, 150), (node.x, node.y, wnode, hnode))        
        else:
            # - not the next action (different color 2)
            pygame.draw.rect(screen, (50, 220, 250), (node.x, node.y, wnode, hnode))

        # number of terminal nodes +1
        num_leaf += 1

    # Childrens
    for child in node.childs:
        # Line
        pygame.draw.line(screen, (50, 50, 50), (node.x+(wnode/2), node.y+(hnode)), (child.x+(wnode/2), child.y), 1)
        # Draw children (recursively)
        rec_draw_tree(child, num_act)

    # Text name
    text = font2.render(node.text, 1, (0, 0, 0))
    screen.blit(text, (node.x, node.y))

# draw a tree by a root node
def draw_tree(root, num_act=-1):

    # organize the nodes according to their depth
    depth2nodes = rec_tree_depth(root)
    
    # compute (x, y) according to the node's depth
    wpas = 5
    ypas = 50
    y = height - tree_height + 10
    for i in range(len(depth2nodes)):
        x = (width/2) - ((len(depth2nodes[i]) * (wnode + wpas))/2)
        for node in depth2nodes[i]:
            node.x = x
            node.y = y
            x += wnode + wpas
        y += ypas

    # fix (x) position
    for i in range(len(depth2nodes)-1, -1, -1):
        for node in depth2nodes[i]:
            if node.childs:
                node.x = node.childs[0].x + ((node.childs[-1].x - node.childs[0].x)/2)
                node.childs[1].x = node.x

    ### DRAW TREE ###
    
    global num_leaf
    num_leaf = 0
    rec_draw_tree(node, num_act)
