from lib.entities import schedule_classes
from lib.entities import entity_classes
from lib.loaders import csv_loader
import copy
import csv

import os
import sys

def save_schedule_to_csv(schedule, filepath):
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
                col_values.append(r.expected_total)
                col_values.extend(b.as_list())
                rows_to_write.append(col_values)
    filepath = 'C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\'+sch.date +'.csv'
    csv_loader.save_csv_info(filepath, rows_to_write)
    
def save_multiple_schedules(schedules, directorypath):
    """Saves a batch of schedules. Each schedule is given an individual file"""
    for s in schedules:
        save_schedule_to_csv(s, directorypath + s.date +'.csv')

def build_schedule_from_csv(filepath):
    """Loads a production schedule from a csv file"""
    rows_to_read = []
    runs_to_load = []
    try: 
        production_batch_info = csv_loader.load_csv_info(filepath)
        if (production_batch_info == None):
            return
        # Now we have a list of batches with the line and date as the first two elements of each row
        date = os.path.basename(filepath).rstrip(".csv") #get date from file name
        s_to_return = schedule_classes.Schedule(date)
        for row in production_batch_info: # each line represents a batch
            if not len(row) == 8: # bad format
                continue
            # according to csv save format:
            line_name = row[0]
            run_date = row[1]
            run_total = row[2]
            product_name = row[3]
            product_kind = row[4]
            product_size = row[5]
            batch_pallette = row[6]
            batch_qty = row[7]

            # build and assemble constituent pieces of the schedule
            p = entity_classes.Product(product_name, product_kind, product_size)
            b = schedule_classes.Batch(p, batch_pallette, batch_qty)
            r = schedule_classes.Run(run_date, run_total)
            r.add_batch(b)
            s_to_return.add_run(line_name, r)

        return s_to_return
    except Exception:
        print ("An error occurred while building schedule from file " +os.path.basename(filepath))
        return None

def build_multiple_schedules(schedule_names, directory_path):
    to_return = []
    for s in schedule_names:
        s_filepath = directory_path + s + '.csv'
        s_to_add = build_schedule_from_csv(s_filepath)
        if not s_to_add == None:
            to_return.append(s_to_add)
    return to_return
