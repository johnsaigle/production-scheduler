#!/usr/bin/python
import sys
import os
import inspect
from lib.entities import schedule_classes 
from lib.loaders import schedule_loader as s_loader
from lib.loaders import entity_loader as e_loader

def print_usage():
    """A manual displaying the usage of functions for this program"""
    print ("USAGE:")
    print ("export filename [destination]")
    print ("\tExports a dataset to a csv file with filename. Saves to working directory by default")
    print ("import filename [destination]")
    print ("\tImports a dataset from a csv file with filename. Loads from working directory by default")
    print ("")

def run_entity_builder():
    import entity_builder
    entity_builder.start()

def plot():
   import matplotlib.pyplot as plt
   global schedules
   s = schedule[len(schedules) - 1] # just grab the last schedule for now
   runs = s.runs_by_date()
   batches = runs.batches
   totals = []
   for r in runs:
       totals.append(r.expected_total)

    #plotting
   plt.plot(totals)
   plt.xlabel('Run')
   plt.ylabel('Expected total')
   plt.show()
   
    
def load_schedules():
    global schedules
    working_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # this will return the filepath of the src directory
    if working_dir.endswith('/src'): # unix 
        script_root_directory = working_dir[:-4] # removes the final four characters
        schedule_directory = script_root_directory + '/data/schedules/' #this works for Mac, not sure yet about windows
    elif working_dir.endswith('\\src'): #windows
        script_root_directory = working_dir[:-4] # removes the final four characters
        schedule_directory = script_root_directory + '\\data\\schedules\\'
    else:
        print ("Loading error: script not launched from within src directory")
        sys.exit()

    prev_schedules = os.listdir(schedule_directory)
    schedules = s_loader.build_multiple_schedules(prev_schedules, schedule_directory)
    print ("Schedules loaded.")

def invalid():
    print ("Bad function name. Try %s" % (", ".join(funcs.keys())))

main_funcs = {  1: run_entity_builder,
                2: plot,
                3: load_schedules
             }
global schedules
choice = -1
while True:
      filename = None
      filepath = None
      print ("\n~*~*\tPRODUCTION SCHEDULER\t*~*~")
      print ("1) Launch entity builder")
      print ("2) Generate plot")
      print ("3) Load existing schedules")
      print ("Type ? for help ")

      choice = input(">: ");
      choice = choice.strip() # parse input
      if len(choice) > 2 or len (choice) < 1: #not a valid size
        error("Enter a one- or two-digit number to select an option.")
        continue
      if choice == 'q':
        print("Quitting...")
        sys.exit()
      else:
        choice = int(choice)
        try:
            main_funcs[choice]() # execute the chosen function based on funcs dictionary
        except KeyError:
            error("Function could not be found in dictionary")
