class Schedule:
    """Represents the production scheule for one day, projected three weeks in the future across various lines"""
    def __init__(self, date):
      self.runs = []
      self.date = date # the date the schedule was created by the system
      
    def add_run(self, line, run):
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
            print (run.to_pretty_string()) #
            print ("")

    def runs_by_line(self):
        return sorted(self.runs, key=lambda run: run.line)

    def runs_by_date(self):
        return sorted(self.runs, key=lambda run: run.date)

    def to_pretty_string(self):
        return "Date: " + date +". "+len(runs) +" runs recorded."

class Run:
    """A series of batches to be produced in one day"""
    def __init__(self, line, date, expected_total):
        self.batches = []
        self.expected_total = expected_total # as calculated in the production schedule by SAP
        self.date = date # the day of manufacture
    
    def add_batch(self, batch):
      if (batch.product in line.products) and (batch.pallette in line.pallettes):
        self.batches.add(batch)
      else:
        print ("Error: {product} on {pallette} incompatible with {line}").format(product=batch.product.name, pallette=batch.pallette, line=line.name)

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

