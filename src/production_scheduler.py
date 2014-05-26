#!/usr/bin/python
import sys
import os
import inspect
import datetime
import matplotlib.pyplot as plt
import numpy as np
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

def dates_to_weekday(schedule, line):
    date_strings = [r.date for r in schedule.runs[line]]
    dates = [datetime.datetime.strptime(ds, "%Y-%m-%d") for ds in date_strings]
    weekdays = [d.strftime("%A") for d in dates]
    return weekdays

def plot(s):
   print("Plotting schedule.")
   print(s.to_pretty_string())
   plots = []

   # To make a stacked bar graph, we need to create an
   # array for each i batch
   num_batches = []
   for key in s.runs:
       num_batches.append(len(s.runs[key]))
   max_batches = max(num_batches) # the max to iterate over
   batches_to_plot = []
   # init array with empty lists
   for i in range(0,max_batches):
       batches_to_plot.append([])

   # get info for the graph
   line = 'BF713'
   for i in range(0, max_batches):
       for r in s.runs[line]:
           if i >= len(r.batches):
               batches_to_plot[i].extend([0])
               continue
           # add ith batch of r to ith row in batches_to_plot
           b = r.batches[i]
           qty = int(b.expected_quantity)
           batches_to_plot[i].extend([qty]) # qty must be a list because extend tries to iterate over elements, and ints are not iterable

   #set up formatting
   N = max_batches # max days recorded per schedule
   ind = np.arange(N) # column spacing
   width = 0.6
   cols = ['r', 'b', 'g','y', 'k', '#551A8B', '#EE82EE']
   col = 1 # represents the colour of the batches
   xticks = dates_to_weekday(s, line)
   plt.xticks(ind+width/2., np.asarray(xticks) )
   plt.ylabel('Run Total')

   # build graph and print data
   print(batches_to_plot[0])
   plt.bar(ind, np.asarray(batches_to_plot[0]), width, color = 'r')
   bottom = np.cumsum(batches_to_plot,axis = 0)
   for i in range(1, len(batches_to_plot)):
       print(batches_to_plot[i])
       plt.bar(ind, np.asarray(batches_to_plot[i]), width, color = cols[col], bottom=bottom[i-1])
       col += 1
   plt.show()
   plt.savefig('test.pdf')
    
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
schedules = []
while True:
      choice = -1
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
        if choice == 2:
            if len(schedules) < 1:
                   print ("No loaded schedules.")
                   continue
            for i, s in zip(range(len(schedules)), schedules):
                print (str(i) +" -- " +s.to_pretty_string())
            selection= int(input("Select schedule: "))
            curr_schedule = schedules[selection]
            plot(curr_schedule)
            continue
        try:
            main_funcs[choice]() # execute the chosen function based on funcs dictionary
        except KeyError:
            error("Function could not be found in dictionary")
