import random

def generateDungeon2DList (dungeonSize = (100, 100), minNodeSize = (20, 20),
                           **kwargs):
    """
        Generates a 2D list dungeon of size dungeonSize.
        Uses the Binary Space Partitioning Method:
        http://www.roguebasin.com/index.php?title=Basic_BSP_Dungeon_generation
    """
    biasRatio = kwargs["biasRatio"] if "biasRatio" in kwargs else 0.75
    biasStrength = kwargs["biasStrength"] if "biasStrength" in kwargs else 0
    maxBridgeWidth = kwargs["maxBridgeWidth"] if "maxBridgeWidth" in kwargs else 1

    # Create dungeon tree with partitions:
    dungeonTree = TreeNode((0,0), dungeonSize, minNodeSize)
    partitions = dungeonTree.getPartitionsList()

    # Create rooms within the given partitions:
    # Convert from tree to slices list:
    dungeonTree.generateTreeRooms(biasRatio, biasStrength)
    roomsList = dungeonTree.getRoomsList()
    # Generate bridges between this tree's rooms:
    bridgesList = generateTreeBridges(roomsList, maxBridgeWidth)
    # In our 2D grid, rooms and bridges will count as floor:
    areaList = roomsList[:]
    areaList.extend(bridgesList)
    dungeon2D = [[0 for i in range(dungeonSize[0])] for j in range(dungeonSize[1])]
    # Go through each tile in the areaList and fill in dungeon2D's floor:
    for bounds in areaList:
        x0, y0, x1, y1 = bounds[0], bounds[1], bounds[2], bounds[3]
        for rowNum in range(y0, y1):
            for colNum in range(x0, x1):
                dungeon2D[rowNum][colNum] = 1
    return dungeon2D

def generateDungeonVisualize(dungeonSize = (100, 100),
    minNodeSize = (20, 20), **kwargs):
    """
        Generates a dungeon tree and uses TKinter to draw a visual of the
         partitions.
    """
    # Set up kwarg variables:
    winWidth = kwargs["winWidth"] if "winWidth" in kwargs else dungeonSize[0]
    winHeight = kwargs["winHeight"] if "winHeight" in kwargs else dungeonSize[1]
    biasRatio = kwargs["biasRatio"] if "biasRatio" in kwargs else 0.75
    biasStrength = kwargs["biasStrength"] if "biasStrength" in kwargs else 0
    maxBridgeWidth = kwargs["maxBridgeWidth"] if "maxBridgeWidth" in kwargs else 1

    import tkinter as tk
    root = tk.Tk()
    canvas = tk.Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()

    dungeonTree = TreeNode((0,0), dungeonSize, minNodeSize)
    partitions = dungeonTree.getPartitionsList()
    print("Displaying partitions:", partitions, '\n')
    _visualizeDungeonTreePartitions(canvas, dungeonSize, partitions, winWidth,
                                    winHeight)
    dungeonTree.generateTreeRooms(biasRatio, biasStrength)

    roomsList = dungeonTree.getRoomsList()
    print("Displaying rooms:", roomsList)
    _visualizeDungeonRooms(canvas, dungeonSize, roomsList, winWidth, winHeight)

    _visualizeDungeonDimensions(canvas, dungeonSize, partitions, roomsList,
                                winWidth, winWidth)
    bridgesList = generateTreeBridges(roomsList, maxBridgeWidth)
    print("Displaying Bridges: ", bridgesList)
    _visualizeRoomBridges(canvas, dungeonSize, bridgesList, winWidth, winHeight)
    root.mainloop() # Note, Will block until window is closed!

# --- Visualization Helper Functions ---
def _visualizeDungeonTreePartitions (canvas, originalSize, partitions, winWidth,
                                     winHeight):
    """
        Draws partitions in a Tkinter window given a list of partitions.
    """

    # Because our window size may not match our original size, we need scale:
    scaleX = winWidth/originalSize[0]
    scaleY = winHeight/originalSize[1]
    margin = 2
    # Draw blank rectangles with borders to represent partitions:
    for bounds in partitions:
        initialX = bounds[0]*scaleX + margin
        initialY = bounds[1]*scaleY + margin
        endX = bounds[2]*scaleX - margin
        endY = bounds[3]*scaleY - margin
        canvas.create_rectangle(initialX, initialY, endX, endY, width=margin)

def _visualizeDungeonDimensions (canvas, originalSize, partitions, roomList,
                                 winWidth, winHeight):
    """
        Draws the dimensions of each partition and room in text.
    """
    scaleX = winWidth/originalSize[0]
    scaleY = winHeight/originalSize[1]
    margin = 2
    textMargin = 10
    # Draw blank rectangles with borders to represent partitions:
    for bounds in partitions:
        initialX = bounds[0]*scaleX + margin
        initialY = bounds[1]*scaleY + margin
        endX = bounds[2]*scaleX - margin
        endY = bounds[3]*scaleY - margin
        canvas.create_text(initialX + textMargin , initialY + textMargin,
                           text=str(bounds), fill="blue", anchor="w")

    for room in roomList:
        initialX = room[0]*scaleX + margin
        initialY = room[1]*scaleY + margin
        endX = room[2]*scaleX - margin
        endY = room[3]*scaleY - margin
        canvas.create_text((initialX+endX)//2, (initialY+endY)//2,
                           text=str(room), fill="red")

def _visualizeDungeonRooms (canvas, originalSize, roomList, winWidth,
                            winHeight):
    """
        Draws rooms in a Tkinter window given a list of rooms.
    """
    # Because our window size may not match our original size, we need scale:
    scaleX = winWidth/originalSize[0]
    scaleY = winHeight/originalSize[1]
    margin = 2
    # Draw filled rectangles with the dimensions of our rooms:
    for room in roomList:
        initialX = room[0]*scaleX + margin
        initialY = room[1]*scaleY + margin
        endX = room[2]*scaleX - margin
        endY = room[3]*scaleY - margin
        canvas.create_rectangle(initialX, initialY, endX, endY, width=0,
                                fill="black")

def _visualizeRoomBridges (canvas, originalSize, bridgeList, winWidth,
                             winHeight):
    """
        Draws room bridges in a tkinter canvas.
    """
    scaleX = winWidth/originalSize[0]
    scaleY = winHeight/originalSize[1]
    margin = 2
    for bridge in bridgeList:
        initialX = bridge[0]*scaleX
        initialY = bridge[1]*scaleY
        endX = bridge[2]*scaleX
        endY = bridge[3]*scaleY
        canvas.create_rectangle(initialX, initialY, endX, endY, width=0,
                                fill="grey")

# --- ---

class TreeNode ():
    """
        This class implements the tree behaviour of Binary Space Partitioning.
        Every TreeNode will have two sub-TreeNodes until we run out of space.
    """
    def __init__ (self, origin, bounds, minNodeSize, iteration=0):
        # Store our information:
        self.origin = origin
        self.bounds = bounds
        self.beforeSplitNode = None
        self.afterSplitNode = None
        self.iteration = iteration # Used for str representation and debug.
        self.roomBounds = None
        self._growTree(minNodeSize)

    def _growTree (self, minNodeSize):
        """
            Called every init, this splits the node randomly into two subnodes.
        """
        isHorizontalSplit = random.random() >= 0.5
        if isHorizontalSplit:
            sliceStart = self.origin[1]
            sliceEnd = self.bounds[1]
            minSpacing = minNodeSize[1]
            # If we have enough space to slice given our minimum spacing:
            if not sliceStart + minSpacing >= sliceEnd - minSpacing:
                splitPosition = random.randint(sliceStart + minSpacing,
                                               sliceEnd - minSpacing)
                self.beforeSplitNode = TreeNode((self.origin[0],
                                                self.origin[1]),
                                                (self.bounds[0], splitPosition),
                                                minNodeSize, self.iteration+1)
                self.afterSplitNode = TreeNode((self.origin[0], splitPosition),
                                               (self.bounds[0], self.bounds[1]),
                                               minNodeSize, self.iteration+1)
        else:
            # The idea is the same for a vertical split, but our constraints are
            #  now about the x-axis
            sliceStart = self.origin[0]
            sliceEnd = self.bounds[0]
            minSpacing = minNodeSize[0]
            if not sliceStart + minSpacing >= sliceEnd - minSpacing:
                splitPosition = random.randint(sliceStart + minSpacing,
                                               sliceEnd - minSpacing)
                self.beforeSplitNode = TreeNode((self.origin[0],
                                                self.origin[1]),
                                                (splitPosition, self.bounds[1]),
                                                minNodeSize, self.iteration+1)
                self.afterSplitNode = TreeNode((splitPosition, self.origin[1]),
                                               (self.bounds[0], self.bounds[1]),
                                               minNodeSize, self.iteration+1)

    def getPartitionsList (self, partitionList=[]):
        """
            Returns this tree's slices in list form.
            E.g. [(0,0,100,100)]
            Slices are found at the roots of this tree (the node which has no
             other nodes attached)
            Used for visualization.
        """
        # If we are a root node, we add our bounds to the list:
        if self.beforeSplitNode == None or self.afterSplitNode == None:
            partitionList.append((self.origin[0], self.origin[1],
                                  self.bounds[0], self.bounds[1]))
        else:
            # We need to go to a deeper node:
            # Destructively modify our partitionList through recursion:
            if self.beforeSplitNode != None:
                self.beforeSplitNode.getPartitionsList(partitionList)
            if self.afterSplitNode != None:
                self.afterSplitNode.getPartitionsList(partitionList)
        return partitionList # This will only matter at the top element!

    def getRoomBridges (self, bridgesList=[]):
        """
            Returns a list of rects representing bridges between rooms
             throughout the entire dungeon tree.
        """
        bridgesList.extend(self.bridges)
        if self.beforeSplitNode != None:
            self.beforeSplitNode.getRoomBridges(bridgesList)
        if self.afterSplitNode != None:
            self.afterSplitNode.getRoomBridges(bridgesList)
        return bridgesList

    def getRoomsList (self, roomsList=[]):
        """
            Returns this tree's slices in list form.
            E.g. [(75,50,97,90), (...)]
            Used for Visualization
        """
        # If we have a room in the current node, then we add it to the list:
        if self.roomBounds != None:
            roomsList.append(self.roomBounds)
        if self.beforeSplitNode != None:
            self.beforeSplitNode.getRoomsList(roomsList)
        if self.afterSplitNode != None:
            self.afterSplitNode.getRoomsList(roomsList)
        return roomsList

    def generateTreeRooms (self, biasRatio, biasStrength):
        """
            Generates rooms for this tree.
        """
        # If we are a root node, we generate our room:
        if self.beforeSplitNode == None and self.afterSplitNode == None:
            self.roomBounds = generateRoom((self.origin[0], self.origin[1],
                                           self.bounds[0], self.bounds[1]),
                                           biasRatio=biasRatio,
                                           biasStrength=biasStrength)
        if self.beforeSplitNode != None:
            self.beforeSplitNode.generateTreeRooms(biasRatio, biasStrength)
        if self.afterSplitNode != None:
            self.afterSplitNode.generateTreeRooms(biasRatio, biasStrength)

    def __str__ (self):
        """
            Called whenever this object needs to be converted to a string.
            For example, in a print statement.
            Used mainly for debugging.
        """
        intro = "Node %d:" % (self.iteration)
        data = "Origin: %s Bounds: %s" % (str(self.origin), str(self.bounds))
        beforeSplitData = "Before Split Branch: " + str(self.beforeSplitNode)
        afterSplitData = "After Split Branch: " + str(self.afterSplitNode)
        return ("%s\n%s\n%s\n%s") % (intro,data,beforeSplitData,afterSplitData)

# --- Generation Helper Functions ---
def generateRoom (partition, biasRatio=0.75, biasStrength=0):
    """
        Generates and returns a room (tuple with 2 coordinate sets)
         of random size limited by a the given partition/boundary (x0,y0,x1,y1).
        If given a bias, it will attempt to make the room match biasRatio of the
         partition with biasStrength.
    """
    # We will refer to the origin and bounds as follows (for readability):
    x0, y0, x1, y1 = partition[0], partition[1], partition[2], partition[3]

    xAvg = (x0 + x1) // 2
    # The random starting point:
    xOriginRand = random.randrange(x0, xAvg)
    # The point we are aiming towards:
    xOriginBiasPoint = x0 + (x1 - x0) * (1-biasRatio)
    # The final value:
    roomOriginX = int(xOriginRand + (xOriginBiasPoint - xOriginRand)\
                    * biasStrength)

    yAvg = (y0 + y1) // 2
    yOriginRand = random.randrange(y0, yAvg)
    yOriginBiasPoint = y0 + (y1 - y0) * (1-biasRatio)
    roomOriginY = int(yOriginRand + (yOriginBiasPoint - yOriginRand)\
                    * biasStrength)

    xEndRand = random.randrange(xAvg, x1)
    xEndBiasPoint = x1 - (x1 - x0) * (1-biasRatio)
    roomEndX = int(xEndRand + (xEndBiasPoint - xEndRand) * biasStrength)

    yEndRand = random.randrange(yAvg, y1)
    yEndBiasPoint = y1 - (y1 - y0) * (1-biasRatio)
    roomEndY = int(yEndRand + (yEndBiasPoint - yEndRand) * biasStrength)
    return (roomOriginX, roomOriginY, roomEndX, roomEndY)

def generateBridge (room1, room2, maxBridgeWidth=1):
    """
        Generates a bridge between two rooms. Returns this bridge in rect. form.
         (x0, y0, x1, y1)
        We assume due to earlier methods that rooms may meet but never
         intersect.
        Basic Algorithm:
         - Get horizontal or vertical direction of bridge by finding the closest
          edges.
         - Pick a random point on the first room's edge.
         - Pick a random point on the second room's edge.
         - Pick a midpoint between the two edges on the predetermined axis.
         - Create three rectangles connecting these points.
    """
    # Determine direction of the bridge:
    horizontalBridge = False
    direction = (room2[0] - room1[2], room2[1] - room1[3])
    if direction[0] == 0 or direction[1] == 0:
        # Rooms are already connected, return emptyList:
        return []
    elif min(abs(direction[0]), abs(direction[1])) == abs(direction[0]):
        # Horizontal takes ties.
        horizontalBridge = True
    bridge = [] # List of 3 rectangles
    bridgeWidth = random.randint(0, maxBridgeWidth)
    # Find point on edge of first room (will be a range of values):
    if horizontalBridge:
        # Pick point range on right or left edge:
        if direction[0] > 0: # Going right
            bridgeStartX = room1[2]
            bridgeStartY = random.randint(min(room1[1], room1[3]), max(room1[1], room1[3]))
            bridgeEndX = room2[0]
            bridgeEndY = random.randint(min(room2[1], room2[3]), max(room2[1], room2[3]))
            bridgeMidpoint = random.randint(min(room1[2], room2[0]), max(room1[2], room2[0]))
        elif direction[0] < 0: # Going left, we instead bridge 2 to 1:
            bridgeStartX = room2[2]
            bridgeStartY = random.randint(min(room2[1], room2[3]), max(room2[1], room2[3]))
            bridgeEndX = room1[0]
            bridgeEndY = random.randint(min(room1[1], room1[3]), max(room1[1], room1[3]))
            bridgeMidpoint = random.randint(min(room1[0], room2[2]), max(room1[0], room2[2]))
        bridge.append((bridgeStartX, bridgeStartY - bridgeWidth,
                      bridgeMidpoint, bridgeStartY + bridgeWidth))
        bridge.append((bridgeMidpoint - bridgeWidth, bridgeStartY - bridgeWidth,
                      bridgeMidpoint + bridgeWidth, bridgeEndY + bridgeWidth))
        bridge.append((bridgeMidpoint, bridgeEndY - bridgeWidth,
                      bridgeEndX, bridgeEndY + bridgeWidth))
    else:
        if direction[1] < 0: # Going down
            bridgeStartY = room1[3]
            bridgeStartX = random.randint(min(room1[0], room1[2]), max(room1[0], room1[2]))
            bridgeEndY = room2[1]
            bridgeEndX = random.randint(min(room2[0], room2[2]), max(room2[0], room2[2]))
            bridgeMidpoint = random.randint(min(room1[3], room2[1]), max(room1[3], room2[1])) # Midpoint in y
        elif direction[1] > 0: # Going up
            bridgeStartY = room2[3]
            bridgeStartX = random.randint(min(room2[0], room2[2]), max(room2[0], room2[2]))
            bridgeEndY = room1[1]
            bridgeEndX = random.randint(min(room1[0], room1[2]), max(room1[0], room1[2]))
            bridgeMidpoint = random.randint(min(room2[3], room1[1]), max(room2[3], room1[1]))
        bridge.append((bridgeStartX - bridgeWidth, bridgeStartY,
                      bridgeStartX + bridgeWidth, bridgeMidpoint))
        bridge.append((bridgeStartX - bridgeWidth, bridgeMidpoint - bridgeWidth,
                      bridgeEndX + bridgeWidth, bridgeMidpoint + bridgeWidth))
        bridge.append((bridgeEndX - bridgeWidth, bridgeMidpoint,
                      bridgeEndX + bridgeWidth, bridgeEndY))
    return bridge

def generateTreeBridges (roomList, maxBridgeWidth=1):
    """
        Given a list of rooms, returns a list of rect. representing bridges.
        Attempts to connect each room to the closest room not already connected.
    """
    bridges = []
    roomsLeft = roomList[:]

    # Keep bridging the closest room until we run out of rooms:
    currentRoom = roomsLeft[0]
    while True:
        # Find closest room to the current room:
        listWithoutCurrent = roomsLeft[:]
        roomsLeft.remove(currentRoom)
        closestRoom = findClosestRoom(currentRoom, roomsLeft)
        if (closestRoom):
            bridges.extend(generateBridge(currentRoom, closestRoom, maxBridgeWidth))
            currentRoom = closestRoom
        else:
            # No more rooms left
            break
    return bridges

def findClosestRoom (room, roomList):
    """
        Finds the closest room to 'room' in the roomList.
        Distance is calculated by rectangle centers.
    """
    currentClosest = None
    closestDistance = None
    roomCenter = (room[0] + (room[0] + room[2]) // 2,
                  room[1] + (room[1] + room[3]) // 2)
    for compareRoom in roomList:
        compareCenter = (compareRoom[0] + (compareRoom[0] + compareRoom[2]) // 2,
                         compareRoom[1] + (compareRoom[1] + compareRoom[3]) // 2)
        dist = ((compareCenter[0] - roomCenter[0]) ** 2 + (compareCenter[1] - roomCenter[1]) ** 2) ** 0.5
        if currentClosest != None and dist < closestDistance:
            currentClosest = compareRoom
            closestDistance = dist
        elif currentClosest == None:
            currentClosest = compareRoom
            closestDistance = dist
    return currentClosest
# --- ---

if __name__ == "__main__": # If we aren't used as a module, do the visualization
    generateDungeonVisualize(biasRatio=0.9, biasStrength=1, winWidth=500, winHeight=500)
