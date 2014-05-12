A program that models production lines in the Shell plant. As an alternative to modelling data using excel, this project aims to do analysis and simulation using Python. 

The main components:
1) The Entity-Builder -- used to take some of the drudgery out of data entry work. Short forms are used for product names and products with their pallettes are tightly coupled with a Line data structure. This allows for assured integrity of the data: as an example, only certain products will be produced on certain lines, or on certain pallettes. This is a clear dvantagre to excel where it's much harder to enforce such measures.

2) Production-Scheduler -- largely a skeleton as of now, but essentially will act as a base-of-operations for the program so that many kinds of analytics can be run on the production schedules based on Line, product, expected quantity vs actual quantity of product produced, and so on.

The other files in the lib directories are mainly classes to represent objects as well as loader programs to support working with different csv formats (excel and raw data formats).
