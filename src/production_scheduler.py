#!/usr/bin/python
import csv
import sys
from lib.entities import schedule_classes 
from lib.loaders import scheduler_loader as s_loader
from lib.loaders import entity_loader as e_loader

def print_usage():
    """A manual displaying the usage of functions for this program"""
    print ("USAGE:")
    print ("export filename [destination]")
    print ("\tExports a dataset to a csv file with filename. Saves to working directory by default")
    print ("import filename [destination]")
    print ("\tImports a dataset from a csv file with filename. Loads from working directory by default")
    print ("")

def invalid():
    print ("Bad function name. Try %s" % (", ".join(funcs.keys())))

# MAIN PART
if __name__=='__main__':
  #init_data()
  products = [] # read in all products from file
  schedules = {}

  while True:
      filename = None
      filepath = None
      print ("~*~*\tPRODUCTION SCHEDULER\t*~*~")
      print ("Type ? for help ")
          
      action = input(">: ");
      action = (action.strip()).split(' ') # parse input
          
##      if func == 'save_to_csv' or 'load_from_csv':
##          if len(action) < 2:
##              print_usage()
##          else:
##              filename = action[1]
##              if len(action) == 3:
##                  filepath = action[2]
##              func(filename, filepath) # filename, filepath
else:
    print ("'Production-scheduler imported'")


    

    

    
