from lib.entities import schedule_classes
from lib.entities import entity_classes
import copy
import csv

def save_schedule(schedule):
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
    with open('C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\'+sch.date +'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_write)
    
def save_multiple_schedules(schedules):
    for s in schedules:
        save_schedule(s)

def load_schedules_from_csv(filename, filepath=None):
    print ("TODO")
