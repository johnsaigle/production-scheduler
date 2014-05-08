#!/usr/bin/python
import csv

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

def init_data():
    with open('data.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        production_lines = next(datareader) # first row in csv is the name of the product lines

# MAIN PART
if __name__=='__main__':
  init_data()
  products = [] # read in all products from file
  schedules = {}
  funcs = {"save": save_schedules_to_csv, "load": load_schedules_from_csv, "usage": print_usage, "?": print_usage}

  while True:
      filename = None
      filepath = None
      print ("~*~*\tPRODUCTION SCHEDULER\t*~*~")
      print ("Type ? for help ")
          
      action = input(">: ");
      action = (action.strip()).split(' ') # parse input
          
      func = funcs.get(action[0], invalid) # calls action[0]() if found and invalid if not
      if func == 'save_to_csv' or 'load_from_csv':
          if len(action) < 2:
              print_usage()
          else:
              filename = action[1]
              if len(action) == 3:
                  filepath = action[2]
              func(filename, filepath) # filename, filepath
else:
    print ("'Production-scheduler imported'")


    

    

    
