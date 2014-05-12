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
        col_values = []
        for b in r.batches:
            col_values.append(r.line.name)
            col_values.append(r.date)
            col_values.extend(b.as_list())
            rows_to_write.append(col_values)
        print (col_values)
    with open('C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\'+sch.date +'.csv', 'w') as f:
        writer = csv.writer(f)
        print (len(rows_to_write)) # START HERE TOMORROW
        writer.writerows(rows_to_write)
        print (writer.dialect)
    
def save_multiple_schedules(schedules):
    for s in schedules:
        save_schedule(s)

def load_schedules_from_csv(filename, filepath=None):
    print ("TODO")

#create dummy object to test functionality
s = schedule_classes.Schedule("01012014")
print(s)
l = entity_classes.Line("BF713")
r = schedule_classes.Run(l,"01012014", 1000)
print (r)
p = entity_classes.Product("Du", "5W50", "1*5")
print (p)
b = schedule_classes.Batch(p, "mypallette", 1000)
print (b)
b2 = schedule_classes.Batch(p, "myotherpallette", 50)
print (b2)
s.add_run(r)
r.add_batch(b)
r.add_batch(b2)
save_schedule(s)
