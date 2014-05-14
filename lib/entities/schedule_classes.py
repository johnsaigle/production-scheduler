from operator import attrgetter
import datetime
# Note: 'toprettystring' functions should be changed to __repr__

class Schedule:
    """Represents the production scheule for one day, projected three weeks in the future across various lines"""
    def __init__(self, date):
      self.runs = {}
      self.date = date # the date the schedule was created by the system
                       # dates are strings (convenience with file reading/writing)
      self.dateobj = datetime.datetime.strptime(self.date, "%Y-%m-%d")
      
    def add_run(self, line_name, run):
        if run.dateobj < self.dateobj or (run.dateobj > self.dateobj+datetime.timedelta(days=7)):
            print("Bad run date (out of range)")
            print("Run date: {0}. Schedule date: {1}".format(run.date, schedule.date))
            return False
        if line_name not in self.runs:
            if len(self.runs) >= 3:
                print ("Error -- too many production lines. Rejecting addition.")
                return False
            else:
                self.runs[line_name] = []
                self.runs[line_name].append(run)
        else:
            if (len(self.runs[line_name]) >= 7):
                print("There are already seven entries for {0}".format(line_name))
                for r in self.runs[line_name]:
                    print (r.to_pretty_string())
                return False
            for r in self.runs[line_name]:
                if run.date == r.date:
                    print ("Run already exists.")
                    return False
            self.runs[line_name].append(run)        
    # A string representation of all runs on the line
    def print_all_runs(self):
        for run in self.runs:
            print (run.date.isoformat()) # gives a string with YYYY-MM-DD
            print (run.to_pretty_string()) #
            print ("")

    def runs_by_date(self, line = None):
        """Returns a list of the runs sorted by date. If line is none, sorts over all lines"""
        runs_to_return = []
        # iterate over all runs and return them sorted by line, then date
        if line == None:
            for key in self.runs:
                runs_to_return.extend(sorted(self.runs[key], key=lambda run: run.date))
        else:
            runs_to_return.extend(sorted(self.runs[line.name], key=lambda run: run.date))
        return runs_to_return

    def next_run_date(self, line):
        try:
            runs = self.runs_by_date(line)
            last_date_used = runs[len(runs)-1].dateobj #the last date is the most recent
            run_date = last_date_used + datetime.timedelta(days=1)
            # we don't want to create schedules for weekends
            while run_date.isoweekday() > 5:
                run_date += datetime.timedelta(days=1)
            date_to_return = run_date.isoformat() # return next available date as string
        except KeyError:
            print("No runs for "+line.name+". Using date for current schedule.")
            return self.date # already in iso format
            date_to_return = self.dateobj.isoformat()
        print ("From sched function"+date_to_return)
        return date_to_return
    
    def to_pretty_string(self):
        return "Date: " + self.date +". "+str(len(self.runs)) +" runs recorded."

class Run:
    """A series of batches to be produced in one day"""
    def __init__(self, date, expected_total=None):
        self.batches = []
        self.expected_total = expected_total # as calculated in the production schedule by SAP
        self.date = date # the day of manufacture
        self.dateobj = datetime.datetime.strptime(self.date, "%Y-%m-%d")
    
    def add_batch(self, batch):
        if batch in self.batches:
            print ("Run already contains batch.")  
        else:
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
        return self.date + " -- " +str(len(self.batches)) + " batches recorded"

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
        return ", ".join([self.product.to_pretty_string(), self.pallette, self.expected_quantity])

    def to_csv_string(self):
        return ",".join([self.product.to_pretty_string(), self.pallette, self.expected_quantity])

    def as_list(self):
        to_return = []
        to_return.extend(self.product.as_list())
        to_return.append(self.pallette)
        to_return.append(self.expected_quantity)
        return to_return
