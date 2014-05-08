#!/usr/bin/python
import csv

class Schedule:
  """Represents the production scheule for one day, projected three weeks in the future across various lines"""
  def __init__(self, date):
    self.runs = []
    self.date = date
  

"""
A series of batches to be produced in one day
"""
class Run:
    def __init__(self, date, expected_total):
        self.batches = []
        self.expected_total = expected_total # as calculated in the production schedule by SAP
        self.date = date
    
    def add_batch(self, batch):
        self.batches.add(batch)

    def is_total_correct(self):
        summed_total = 0
        for batch in self.batches:
            summed_total += batch.get_expected_quantity
             
        if (summed_total != self.expected_total):
            print ("Summed total does not meet expected total")
            print ("Expected: {expected}, Summed: {total}".format(expected=self.expected_total, total=summed_total))
            return False
        else:
            return True

    def pretty_print_batches(self):
        for b in self.batches:
            print (b.to_pretty_string())

"""
The quantity and production of some product in the plant
"""
class Batch:
    def __init__(self, product, expected_quantity):
        self.product = product
        self.expected_quantity = expected_quantity

    #returns a string for nice output and for csv writing
    def to_pretty_string(self):
        return ", ".join([product.to_pretty_string(), self.expected_quantity])
        

"""
Represents one type of product produced in a batch on some Line
"""
class Product:
    def __init__(self, brand, kind, size, pallette_type, base_unit):
        self.brand = brand
        self.kind = kind # placeholder for what the product is -- can be oil visocosity, ATF (automatic transmission fluid, PSF (powersteering fluid etc 
        self.size = size # products per pallette
        self.pallette_type = pallette_type
        self.base_unit = base_unit

    #returns a string for nice output and for csv writing
    def to_pretty_string(self):
        return ", ".join([self.brand, self.base_unit, self.viscosity, self.dimension]) 

"""
Represents one production line in the plant
"""
class Line:
    def __init__(self, name):
        self.name = name
        self.runs = {}

    def add_run(self, run):
        if (run.date not in runs):
            self.runs[run.date] = run
        else:
            print ("There is an existing run for date {date}. Delete existing run first or use modify.".format(date=run.date))

    def del_run(self, run):
        del self.runs[run.date]

    #Edits existing run or adds it to runs dictionary if it does not exist
    def modify_run(self, run):
        if(run.date not in self.runs):
            print ("Run added")

        self.runs[run.date] = run

    # A string representation of all runs on the line
    def print_all_runs(self):
        for run in self.runs:
            print (run.date.isoformat()) # gives a string with YYYY-MM-DD
            run.to_pretty_string #
            print ("")

def save_schedules_to_csv(filename, filepath=None):
    if not filename.endswith('.csv'):
        filename += '.csv'
    if filepath is None:
        # save to working directory
        print ("TODO")
    else:
        # save to filepath
        print ("TODO")

def load_schedules_from_csv(filename, filepath=None):
    if not filename.endswith('.csv'):
        filename += '.csv'
    if filepath is None:
        # save to working directory
        print ("TODO")
    else:
        # save to filepath
        print ("TODO")
    
def print_usage():
    print ("USAGE:")
    print ("export filename [destination]")
    print ("\tExports a dataset to a csv file with filename. Saves to working directory by default")
    print ("import filename [destination]")
    print ("\tImports a dataset from a csv file with filename. Loads from working directory by default")
    print ("")

def invalid():
    print ("Bad function name. Try %s" % (", ".join(funcs.keys())))

def init_data_from_csv():
    with open('data.csv', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
        production_lines = next(datareader) # first row in csv is the name of the product lines

        for row in datareader:
            products = (Product(",".join(row)))

        print (products.brand)
        # the rest of the csv file is the list of all avaialble products, one per row
# MAIN PART
init_data_from_csv()
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


    

    

    