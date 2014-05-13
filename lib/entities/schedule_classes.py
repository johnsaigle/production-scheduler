from operator import attrgetter
# Note: 'toprettystring' functions should be changed to __repr__

class Schedule:
    """Represents the production scheule for one day, projected three weeks in the future across various lines"""
    def __init__(self, date, line_names):
      self.runs = {}
      self.date = date # the date the schedule was created by the system
      
    def add_run(self, line_name, run):
        if line_name not in self.runs:
            self.runs[line_name] = []
            self.runs[line_name].append(run)
        else:
            self.runs[line_name].append(run)        
    # A string representation of all runs on the line
    def print_all_runs(self):
        for run in self.runs:
            print (run.date.isoformat()) # gives a string with YYYY-MM-DD
            print (run.to_pretty_string()) #
            print ("")

    def runs_by_date(self):
        runs_to_return = []
        # iterate over all runs and return them sorted by line, then date
        for key in d:
            runs_to_return.extend(sorted(self.runs[key], key=lambda run: run.date))
        return runs_to_return
    
    def to_pretty_string(self):
        return "Date: " + date +". "+len(runs) +" runs recorded."

class Run:
    """A series of batches to be produced in one day"""
    def __init__(self, date, expected_total):
        self.batches = []
        self.expected_total = expected_total # as calculated in the production schedule by SAP
        self.date = date # the day of manufacture
    
    def add_batch(self, batch):
     # if (batch.product in line.products) and (batch.pallette in line.pallettes):
        self.batches.append(batch)
     # else:
      #  print ("Error: {product} on {pallette} incompatible with {line}").format(product=batch.product.name, pallette=batch.pallette, line=line.name)

    def is_total_correct(self):
        summed_total = 0
        for batch in batches:
            summed_total = summed_total + batch.expected_quantity 
             
        if (summed_total != self.expected_total):
            print ("Summed total does not meet expected total")
            print ("Expected: {expected}, Summed: {total}".format(expected=self.expected_total, total=summed_total))
            return False
        else:
            return True

    def to_pretty_string(self):
        return self.date + " -- " +len(self.batches) + " batches recorded"

    def print_all_batches(self):
        for b in self.batches:
            print (b.to_pretty_string())

class Batch:
    """ The quantity and production of some product in the plant"""
    def __init__(self, product, pallette, expected_quantity):
        self.product = product
        self.pallette = pallette # the pallette type used for this batch
        self.expected_quantity = expected_quantity

    #returns a string for nice output and for csv writing
    def to_pretty_string(self):
        return ", ".join([product.to_pretty_string(), self.pallette, self.expected_quantity])

    def to_csv_string(self):
        return ",".join([product.to_pretty_string(), self.pallette, self.expected_quantity])

    def as_list(self):
        to_return = []
        to_return.extend(self.product.as_list())
        to_return.append(self.pallette)
        to_return.append(self.expected_quantity)
        return to_return
