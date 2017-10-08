# PyBSP-Dungeon-Generator
Python dungeon generator using the Binary Space Partitioning method.

## Prerequisites:
- Python 3+ (Made with python 3.6)

## How to test/run:
Make sure you have the prerequisites, then clone this repository. Open a command prompt/terminal and `cd` to the root of the PyBSP_Dungeon_Generator folder. Type `python pybsp.py` for a quick dungeon generation and visualization.

This project now supports Argparse when run as "\__main__". Here are a list of optional parameters you can add after `python pybsp.py`:
- --dungeonSize int int
- --minNodeSize int int
- --biasRatio floatbetween0&1
- --biasStrength floatbetween0&1
- --winSize int int
- --bridgeWidth positiveint

Please run `python pybsp.py -h` for more information.

## How to use in your project:
Clone this repository into your project folder. In your main script, add:
```
import PyBSP_Dungeon_Generator.pybsp
```
You can now generate a dungeon by calling:
```
pybsp.generateDungeon2DList()
```
This will return a 2D list. 0s represent empty space and 1s represent dungeon tiles.

Here is an example of using the other optional arguments:
```
generateDungeon2DList((100, 100), (20, 20),
                      biasRatio=.75, biasStrength=.9,
                      maxBridgeWidth=1)
```

## How it works:
This dungeon generator follows the Binary Space Partitioning algorithm shown here: http://www.roguebasin.com/index.php?title=Basic_BSP_Dungeon_generation

Here is a simple overview of the way this project generates dungeons:

A class, TreeNode, represents the dungeon in the style of a binary tree. Each TreeNode will have two child nodes.

Each TreeNode has a rectangular partition that limits the spawn position and size of a dungeon room. When the first TreeNode is initialized, it can be split into two sub-partitions or child nodes.

A method of TreeNode called "grow" will keep splitting and creating new TreeNode partitions until a minimum size has been reached.

At this stage, rooms are randomly generated inside these boundaries.

The final step is to connect each room with a bridge. In this code, a room attempts to connect itself to another room not already connected with a "z-bridge".

Now that all of the room and bridge sizes are known, we create a 2D list that is filled in with these known values. We have a 2D List randomly generated dungeon!

## License:
This is licensed under the MIT License. All you need to do is include the PyBSP_Dungeon_Generator folder with all of its contents in your project. You can also instead include just pybsp.py and the LICENSE file.
