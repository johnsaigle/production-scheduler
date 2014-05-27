#!/usr/bin/python
import sys
import os
import inspect
import datetime
from pylab import polyfit
from pylab import poly1d
import matplotlib.pyplot as plt
import numpy as np
# my classes
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
    weekdays = []
    date_strings = [r.date for r in schedule.runs[line]]
    if date_strings[0] == schedule.date:
        del date_strings[0]
        weekdays.append('Today')
    dates = [datetime.datetime.strptime(ds, "%Y-%m-%d") if not ds == schedule.date else 'Today' for ds in date_strings]
    weekdays.extend([d.strftime("%A") for d in dates])

    return weekdays

def plot(s, filepath):
    print("Plotting schedule.")
    print(s.to_pretty_string())

    for line in s.runs:
        plots = []
        runs = s.runs_by_date(line)
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # To make a stacked bar graph, we need to create an
        # array for each i batch
        num_batches_per_run = []
        for r in runs:
             num_batches_per_run.append(len(r.batches))
        max_batches = max(num_batches_per_run)
        batches_to_plot = []
        # init array with empty lists which will be filled with batch info
        for i in range(0,max_batches):
            batches_to_plot.append([])

        for i in range(0, max_batches):
            for r in runs:
                if i >= len(r.batches):
                    # pad with zeros if there is no entry
                    batches_to_plot[i].extend([0])
                    continue
                # add ith batch of r to ith row in batches_to_plot
                b = r.batches[i]
                qty = int(b.expected_quantity)
                batches_to_plot[i].extend([qty]) # qty must be a list because extend tries to iterate over elements, and ints are not iterable

        #set up formatting
        N = len(runs) # max days recorded per schedule
        x_pos = np.arange(N) # column placing
        width = 0.6 # how wide the bars will appear
        cols = ['r', 'b', 'g','y', '#D4D4D4', '#551A8B', '#EE82EE', '#FF6103', '#FFCC11', '#CDD704']
        col = 1 # represents the colour of the batches
        xticks = dates_to_weekday(s, line) # convert the dates to weekdays
        plt.xticks(x_pos+width/2., np.asarray(xticks))
        plt.ylabel('Run Total')
        plt.xlabel('Date of Production')
        plt.title("Production Schedule for "+ line + " -- "+s.date)
        bottom = np.zeros(N,)

        # build graph and print data
        print("Building graph ("+line+")")
        bars = []
        batch_labels = [value for sublist in batches_to_plot for value in sublist] # turns lsit of lists into a flat lsit of values
        for i, b in enumerate(batches_to_plot):
            bars.append(ax.bar(x_pos, np.asarray(b), width, bottom=bottom, color = cols[i % len(cols)]))
            # add the batch value to the offset of the bar positions
            bottom += b

        # add labels
        for j in range(len(bars)):
            for i, bar in enumerate(bars[j].get_children()):
                bl = bar.get_xy()
                x = 0.5*bar.get_width() + bl[0]
                y = 0.5*bar.get_height() + bl[1]
                if not batches_to_plot[j][i] == 0:
                    ax.text(x,y, "%d" % (batches_to_plot[j][i]), ha='center', va = 'center')

        # trend line
        x = x_pos
        y = np.array([r.expected_total for r in s.runs[line]])
        fit = polyfit(x,y,1)
        fit_fn = poly1d(fit)
        trendline = plt.plot(x,y, 'ro', x, fit_fn(x), '--k', linewidth=2)

        # save figures to appropriate directories
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = line + '.pdf'
        if os.path.exists(filepath + filename):
            choice = input(filename + " already exists. Overwrite? (y/n) ")
            if choice == 'y':
                os.remove(filepath+filename)
                print("Overwriting...")
            else:
               continue 
        plt.savefig(filepath + filename)
    print("Report complete ({0})".format(s.date))

def error(error_message = None):
    if not error_message:
        print ("Something went wrong.")
    else:
        print ("Error: "+error_message)
    
def load_schedules():
    global schedules
    global script_root_directory
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

#MAIN
main_funcs = {  1: run_entity_builder,
                2: plot,
                3: load_schedules
             }
global schedules
global script_root_directory
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
            while True:
               try:
                   selection= int(input("Select schedule: "))
                   if selection >= 0 and selection < len(schedules):
                       curr_schedule = schedules[selection]
                       break
               except ValueError:
                   continue
            plot(curr_schedule, script_root_directory+'\\reports\\'+curr_schedule.date+'\\')
            continue
        try:
            main_funcs[choice]() # execute the chosen function based on funcs dictionary
        except KeyError:
            error("Function could not be found in dictionary")
