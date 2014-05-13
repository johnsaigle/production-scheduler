from lib.entities import schedule_classes
from lib.entities import entity_classes
from lib.loaders import csv_loader
import copy
import csv

def save_schedule_to_csv(schedule):
    """Saves a schedule to a csv file"""
    rows_to_write = []
    sch = copy.deepcopy(schedule) # copy the passed schedule for encapsulation
    run_dict = sch.runs
    for line_name in run_dict: # line is the name of a line and the key of the dict
        for r in run_dict[line_name]:  # iterate over all runs for this lkine 
            for b in r.batches:
                col_values = []
                col_values.append(line_name)
                col_values.append(r.date)
                col_values.extend(b.as_list())
                rows_to_write.append(col_values)
    filepath = 'C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\'+sch.date +'.csv'
    csv_loader.save_csv_info(filepath, rows_to_write)
    
def save_multiple_schedules(schedules):
    """Saves a batch of schedules.Each schedule is given an individual file"""
    for s in schedules:
        save_schedule_to_csv(s)

def build_schedule_from_csv(filepath, date, production_lines):
    """Loads a production schedule from a csv file"""
    rows_to_read = []
    runs_to_load = []
    production_batch_info = csv_loader.load_csv_info(filepath)
    # Now we have a list of batches with the line and date as the first two elements of each row
    s_to_return = Schedule(date)
    for row in production_batch_info:
        line_name = row[0]
        run_date = row[1]
        if run_date in s.runs: # the run exists in the schedule's dictionary
            this_run = s.runs[run.date]
            if this_run.line.name == line_name:
                # Match: add batch info to this run
                print ("TODO")
            else:
                # There is an entry for this date, but not for this line. New entry
                print ("TODO")
