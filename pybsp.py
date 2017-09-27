import random

def generateDungeon2DList (dungeonSize = (100, 100), minNodeSize = (20, 20)):
    """
        Generates a 2D list dungeon of size dungeonSize.
        Uses the Binary Space Partitioning Method:
        http://www.roguebasin.com/index.php?title=Basic_BSP_Dungeon_generation
    """
    # Create partitions for the rooms.
    newTree = TreeNode((0,0), dungeonSize, minNodeSize)

    # Create rooms within the given partitions:
    # Convert from tree to slices list:
    partitionList = newTree.getPartitionsList()

def generateDungeonPartitionsVisualize(dungeonSize = (100, 100),
    minNodeSize = (20, 20), winWidth=500, winHeight=500):
    """
        Generates a dungeon tree and uses TKinter to draw a visual of the
         partitions.
    """
    dungeonTree = TreeNode((0,0), dungeonSize, minNodeSize)
    partitions = dungeonTree.getPartitionsList()
    print("Displaying partitions:", partitions)
    _visualizeDungeonTreePartitions(dungeonSize, partitions, winWidth,
                                    winHeight)

def _visualizeDungeonTreePartitions (originalSize, partitions, winWidth,
                                     winHeight):
    """
        Draws partitions in a Tkinter window given a list of partitions.
    """
    import tkinter as tk
    root = tk.Tk()
    canvas = tk.Canvas(root, width=winWidth, height=winHeight)
    canvas.pack()
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
    root.mainloop() # Note, Will block until window is closed!

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
