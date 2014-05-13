from lib.entities import schedule_classes
from lib.entities import entity_classes
from . import csv_loader
import copy
import csv

def save_schedule_to_csv(schedule):
    """Saves a schedule to a csv file"""
    rows_to_write = []
    sch = copy.deepcopy(schedule) # copy the passed schedule for encapsulation
    runs_to_save = sch.runs_by_line_then_date()
    for r in runs_to_save:   
        for b in r.batches:
            col_values = []
            col_values.append(r.line.name)
            col_values.append(r.date)
            col_values.extend(b.as_list())
            rows_to_write.append(col_values)
    filepath = 'C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\'+sch.date +'.csv'
    csv_loader.save_csv_info(filepath, rows_to_write)
    
def save_multiple_schedules(schedules):
    """Saves a batch of schedules.Each schedule is given an individual file"""
    for s in schedules:
        save_schedule_to_csv(s)

def load_schedule_from_csv(filename):
    """Loads a production schedule from a csv file"""
    rows_to_read = []
    runs_to_load = []
    with open 'C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\'+filename, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            rows_to_read.append(row)
    # Now we have a list of batches with the line and date as the first two elements of each row
    
