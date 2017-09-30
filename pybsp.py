import random

def generateDungeon2DList (dungeonSize = (100, 100), minRoomSize = (20, 20)):
    """
        Generates a 2D list dungeon of size dungeonSize.
        Uses the Binary Space Partitioning Method:
        http://www.roguebasin.com/index.php?title=Basic_BSP_Dungeon_generation
    """
    # Create partitions for the rooms.
    newTree = TreeNode((0,0), dungeonSize, minRoomSize)

    # Create rooms within the given partitions:
    # Convert from tree to slices list:
    partitionList = newTree.getPartitionsList()
    roomList = generateRooms(partitionList)

def generateRooms (partitions, biasRatio=0.75, biasStrength=0):
    """
        Generates and returns a list of rooms (tuples with 2 coordinate sets)
         of random size limited by a list of partitions/boundaries.
        If given a bias, it will attempt to make the room match biasRatio of the
         partition with biasStrength.
    """
    roomList = []
    for bounds in partitions:
        xAvg = (bounds[2] + bounds[0]) // 2
        # The random starting point:
        xOriginRand = random.randrange(bounds[0], xAvg)
        # The point we are aiming towards:
        xOriginBiasPoint = bounds[0] + (bounds[2] - bounds[0]) * (1-biasRatio)
        # The final value:
        roomOriginX = int(xOriginRand + (xOriginBiasPoint - xOriginRand)\
                        * biasStrength)

        yAvg = (bounds[3] + bounds[1]) // 2
        yOriginRand = random.randrange(bounds[1], yAvg)
        yOriginBiasPoint = bounds[1] + (bounds[3] - bounds[1]) * (1-biasRatio)
        roomOriginY = int(yOriginRand + (yOriginBiasPoint - yOriginRand)\
                        * biasStrength)

        xEndRand = random.randrange(xAvg, bounds[2])
        xEndBiasPoint = bounds[2] - (bounds[2] - bounds[0]) * (1-biasRatio)
        roomEndX = int(xEndRand + (xEndBiasPoint - xEndRand) * biasStrength)

        yEndRand = random.randrange(yAvg, bounds[3])
        yEndBiasPoint = bounds[3] - (bounds[3] - bounds[1]) * (1-biasRatio)
        roomEndY = int(yEndRand + (yEndBiasPoint - yEndRand) * biasStrength)

        roomList.append( (roomOriginX, roomOriginY, roomEndX, roomEndY) )
    return roomList

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

    import tkinter as tk
    root = tk.Tk()
    canvas = tk.Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()

    dungeonTree = TreeNode((0,0), dungeonSize, minNodeSize)
    partitions = dungeonTree.getPartitionsList()
    print("Displaying partitions:", partitions, '\n')
    _visualizeDungeonTreePartitions(canvas, dungeonSize, partitions, winWidth,
                                    winHeight)
    roomList = generateRooms(partitions, biasRatio, biasStrength)
    print("Displaying rooms:", roomList)
    _visualizeDungeonRooms(canvas, dungeonSize, roomList, winWidth, winHeight)

    _visualizeDungeonDimensions(canvas, dungeonSize, partitions, roomList,
                                winWidth, winWidth)

    root.mainloop() # Note, Will block until window is closed!


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

        isHorizontalSplit = random.random() >= 0.5
        if isHorizontalSplit:
            sliceStart = origin[1]
            sliceEnd = bounds[1]
            minSpacing = minNodeSize[1]
            # If we have enough space to slice given our minimum spacing:
            if not sliceStart + minSpacing >= sliceEnd - minSpacing:
                splitPosition = random.randint(sliceStart + minSpacing,
                                               sliceEnd - minSpacing)
                self.beforeSplitNode = TreeNode((origin[0], origin[1]),
                                                (bounds[0], splitPosition),
                                                minNodeSize, iteration+1)
                self.afterSplitNode = TreeNode((origin[0], splitPosition),
                                               (bounds[0], bounds[1]),
                                               minNodeSize, iteration+1)
        else:
            # The idea is the same for a vertical split, but our constraints are
            #  now about the x-axis
            sliceStart = origin[0]
            sliceEnd = bounds[0]
            minSpacing = minNodeSize[0]
            if not sliceStart + minSpacing >= sliceEnd - minSpacing:
                splitPosition = random.randint(sliceStart + minSpacing,
                                               sliceEnd - minSpacing)
                self.beforeSplitNode = TreeNode((origin[0], origin[1]),
                                                (splitPosition, bounds[1]),
                                                minNodeSize, iteration+1)
                self.afterSplitNode = TreeNode((splitPosition, origin[1]),
                                               (bounds[0], bounds[1]),
                                               minNodeSize, iteration+1)

    def getPartitionsList (self, partitionList=[]):
        """
            Returns this tree's slices in list form.
            E.g. [(0,0,100,100)]
            Slices are found at the roots of this tree (the node which has no
             other nodes attached)
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

generateDungeonVisualize(biasRatio=.9, biasStrength=1, winWidth=500, winHeight=500)
