#!/usr/bin/python
import datetime
import sys
from lib.entities import schedule_classes
from lib.entities import entity_classes
from lib.loaders import schedule_loader
from lib.loaders import entity_loader
from itertools import repeat

def next_free_date_index(bit_vector):
    return bit_vector.index(0)

def mark_date_as_used(date_as_isoformat):
    global fridays
    datelist = fridays
    global bit_vector
    bit_vector[datelist.index(date_as_isoformat)] = 1
    
def generate_fridays():
    """"We are only concerned with friday production schedules. Generates a list of all fridays up to today"""
    fridays = []
    date = datetime.date(2014,1,1)
    # get the first friday from the 
    while not date.isoweekday() == 5:
        date += datetime.timedelta(days=1)
    #date is now equal to the first friday in 2014
    while not date > date.today():
        fridays.append(date.isoformat())
        date += datetime.timedelta(days=7)
    return fridays
    
    
def new_schedule_menu():
    """Automatically generate a new schedule by obtaining the next friday for which there is no schedule"""
    global schedules
    global fridays
    global unused_fridays
    global current_schedule
    s = schedule_classes.Schedule(fridays[next_free_date_index(unused_fridays)])
    current_schedule = s
    schedules.append(s)
    print ("Schedule created ({0})".format(s.date))

def new_run_menu():
    print ("New run")
    if current_schedule:
      print ("\n1) Add to current schedule")
      print ("2) Select schedule")
      print ("0) Main menu")
      choice = input(">(S-{schedule_date}): ".format(schedule_date=current_schedule.date))
      if choice == 'y' or choice == '1':
          if not current_line:
              print ("Select line: ")
      elif choice == 'n' or choice == '2':
          for i, s in zip(range(1, len(schedules)+1), schedules):
              print ("["+str(i)+"] ", s.to_pretty_string())
      else:
          print ("Invalid input. Returning...")
          return False
    else:
        print ("No current schedule")
        for i, s in zip(range(1, len(schedules)+1), schedules):
              print ("["+i+"] ", s.to_pretty_string())

def new_batch_menu():
    global production_lines
    global current_schedule
    global current_run
    if not current_schedule:
        print ("No schedule set.")
        return False
    for i, l in zip(range(len(production_lines)), production_lines):
        print (str(i)+" - "+ l.name)
    selection = int(input("Select line: "))
    current_line = production_lines[selection]
    print(current_line.to_pretty_string())
    #check if any runs exist
    if len(current_schedule.runs) > 0:
        # check if the line exists in the dictionary
        if current_schedule.runs[line_name] in current_schedule.runs:
            runs = current_schedule.runs[line_name]
            #check if any runs exist for this line
            if len(runs) > 0:
                print("Runs: ")
                for r in zip(range(len(runs)), runs):
                    print (r.to_pretty_string())
                selection = int(input("Select run: "))
                current_run = runs[selection]
            else:
                current_run = schedule_classes.Run(current_schedule.date)
    else: #no runs or lines exist
        current_run = schedule_classes.Run(current_schedule.date)

    if current_run.expected_total == None:
        current_run.expected_total = input("Enter expected total for run: ")

    if current_schedule.add_run(current_line.name, current_run) == False:
        print("Adding current run failed. Returning to main menu.")
        return False
    else:
        print("Run added.")

    
    
##  global current_run
##  global current_schedule
##  if current_run and current_schedule:
##      print ("\n1) Add to current run")
##      print ("2) Select run from current schedule")
##      print ("3) Select different schedule")
##      print ("0) Main menu")
##      print ("Current run: "+current_run.date +". Current schedule: " +current_schedule.date+".\n")
##      choice = input(">: ")
##      if choice == 'y' or choice == '1':
##          # add the new batch to the current run
##          print ("TODO")
##      elif choice == 'n' or choice == '2':
##          # select different run
##            runs_by_date = current_schedule.runs_by_date()
##            paired = zip(range(1, len(current_schedule.runs)+1), runs_by_date)
##            for pair in paired:   
##                print ("[{index}] {run_string}".format(index=pair[0], run_string=pair[1]))
##            selection = int(input("Enter index: "))
##            current_run = runs_by_date[selection]
##      elif choice == '3':
##          # select different schedule
##          print ("TODO")
##          return False
##      else:
##          invalid()

def init_data():
    print ('TODO')

def save_to_excel():
    print ('TODO')

def save_raw():
    print ('TODO')
    
def print_main_prompt_menu():
    print ("\nEntity Builder~")
    print ("1) New schedule")
    print ("2) New run")
    print ("3) New batch")
    print ("4) Load (import from csv)")
    print ("5) Save (export to csv)")
    print ("6) Save raw (not formatted for excel)")
    print ("0) Quit\n")

def invalid():
    print ("Input invalid.")
    
funcs = {   1: new_schedule_menu,
            2: new_run_menu,
            3: new_batch_menu,
            4: init_data,
            5: save_to_excel,
            6: save_raw
        }
current_schedule = None
current_line = None
current_run = None
fridays = generate_fridays()
unused_fridays = [0] * len(fridays) # this is a bit vector to keep track of the next avaialble friday
production_lines = entity_loader.build_lines() # load production line data
print ("\nLoading previous schedules...")
schedules = schedule_loader.build_multiple_schedules(fridays, 'C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\')
# process loaded schedules
if len(schedules) > 0:   
    print (str(len(schedules))+" schedules loaded:")
    for s in schedules:
        print(s.to_pretty_string())
        mark_date_as_used(s.date, fridays, unused_fridays) # mark availability
    current_schedule = schedules(len(schedules)-1)

choice = 1
while not choice == '0':
    print_main_prompt_menu()
    choice = input('>: ')
    if not len(choice) == 1: #not a valid size
        invalid()
        continue
    choice = int(choice.strip()) # remove white space and convert to int
    if choice == 0:
        sys.exit()
    else:
        try:
            funcs[choice]() # execute the chosen function based on funcs dictionary
        except KeyError:
            invalid()
    
        
