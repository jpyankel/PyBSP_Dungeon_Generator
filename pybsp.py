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

def generateDungeonTreeVisualize():
    pass

def _visualizeDungeonTree ():
    pass

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

generateDungeon()
