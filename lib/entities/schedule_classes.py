from operator import attrgetter
import datetime
# Note: 'toprettystring' functions should be changed to __repr__

class Schedule:
    """Represents the production scheule for one day, projected three weeks in the future across various lines"""
    def __init__(self, date):
      self.runs = {}
      self.date = date # the date the schedule was created by the system
                       # dates are strings (convenience with file reading/writing)
      
    def add_run(self, line_name, run_to_add):
        # check that the run date is within one week of the schedule date
        run_date = datetime.datetime.strptime(run_to_add.date, "%Y-%m-%d")
        self_date = datetime.datetime.strptime(self.date, "%Y-%m-%d")
        if run_date < self_date or (run_date > self_date+datetime.timedelta(days=7)):
            print("Bad run date (out of range)")
            print("Run date: {0}. Schedule date: {1}".format(run_to_add.date, self.date))
            return False
        # if there's no info for this line
        if line_name not in self.runs:
            if len(self.runs) >= 3:
                print ("Error -- too many production lines. Rejecting addition.")
                return False
            else:
                self.runs[line_name] = []
                self.runs[line_name].append(run_to_add)
        elif len(self.runs[line_name]) > 0:
                # we want only seven runs per schedule
                if (len(self.runs[line_name]) >= 7):
                    print("There are already seven entries for {0}".format(line_name))
                    self.print_all_runs()
                    return False
                else:
                    for extant_run in self.runs[line_name]:
                        if run_to_add.date == extant_run.date and run_to_add.expected_total == extant_run.expected_total:
                        
                            # same run. merge batches.
                            if len(run_to_add.batches) > 0:
                                extant_run.batches.extend(run_to_add.batches)
                            return True
                    self.runs[line_name].append(run_to_add)        

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

    def print_all_runs(self):
        for line in self.runs:
            print(line)
            for r in self.runs[line]:
                print("- "+r.to_pretty_string())
            
    def print_all_runs_with_batches(self):
        for line in self.runs:
            print(line)
            for r in self.runs[line]:
                print("- "+r.to_pretty_string())
                r.print_all_batches()

    def next_run_date(self, line):
        try:
            runs = self.runs_by_date(line)
            last_date_used_string = runs[len(runs)-1].date #the last date is the most recent        
            last_date_used = datetime.datetime.strptime(last_date_used_string, "%Y-%m-%d")
            run_date = last_date_used + datetime.timedelta(days=1)
            # we don't want to create schedules for weekends
            while run_date.isoweekday() > 5:
                run_date += datetime.timedelta(days=1)
            date_to_return = run_date.strftime("%Y-%m-%d") # return next available date as string
        except KeyError:
            print("No runs initialized for "+line.name+". Using date for current schedule.")
            date_to_return = self.date # already in correct format
        return date_to_return

    def get_total_runs(self):
        total = 0
        for line in self.runs:
            for run in self.runs[line]:
                total += 1
        return total

    def total_runs_by_line_string(self):
        to_return = ""
        for line_name in self.runs:
            total = 0
            for run in self.runs[line_name]:
                total +=1
            to_return += "{line}: {num_runs} runs recorded. ".format(line=line_name, num_runs=total)
        return to_return
    
    def to_pretty_string(self):
        return "Schedule date: " + self.date +". "+str(self.get_total_runs()) +" runs recorded.\n\t"+self.total_runs_by_line_string()

class Run:
    """A series of batches to be produced in one day"""
    def __init__(self, date, expected_total=None):
        self.batches = []
        self.expected_total = expected_total # as calculated in the production schedule by SAP
        self.date = date # the day of manufacture
    
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
        return "Run date: "+self.date + " - " +str(len(self.batches)) + " batches recorded"

    def print_all_batches(self):
        for b in self.batches:
            print ("--- "+b.to_pretty_string())

class Batch:
    """ The quantity and production of some product in the plant"""
    def __init__(self, product, pallette, expected_quantity):
        self.product = product
        self.pallette = pallette # the pallette type used for this batch
        self.expected_quantity = expected_quantity

    #returns a string for nice output and for csv writing
    def to_pretty_string(self):
        return ", ".join([self.product.to_pretty_string(), self.pallette, str(self.expected_quantity)])

    def to_csv_string(self):
        return ",".join([self.product.to_pretty_string(), self.pallette, str(self.expected_quantity)])

    def as_list(self):
        to_return = []
        to_return.extend(self.product.as_list())
        to_return.append(self.pallette)
        to_return.append(self.expected_quantity)
        return to_return
