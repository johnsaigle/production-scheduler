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

def select_schedule():
    global current_schedule
    global schedules
    if len(schedules) < 1:
        print ("No schedules initialized.")
        print("Creating new schedule.")
        new_schedule()
    else:
        for i, s in zip(range(len(schedules)), schedules):
            print (str(i) +" -- " +s.to_pretty_string())
        selection= int(input("Select schedule: "))
        current_schedule = schedules[selection]
    print ("Current schedule: " +current_schedule.to_pretty_string())

def select_run():
    global current_schedule
    global current_line
    global current_run
    if current_schedule == None:
        select_schedule()
    if len(current) < 1:
        print ("No runs initialized.")
        print("Creating new run.")
        new_run()
    else:
        runs_for_line = current_schedule.runs[current_line]
        for i, r in zip(range(len(runs_for_line)), runs_for_line):
            print (str(i) +" -- " +r.to_pretty_string())
        current_run = runs_for_line[int(input("Select run: "))]
    print ("Current run: " +current_run.to_pretty_string())

def select_line():
    global production_lines
    global current_line
    for i, l in zip(range(len(production_lines)), production_lines):
        print (str(i) +" -- " +l.name)
    current_line = production_lines[int(input("Select line: "))]
    print ("Current line: " +current_line.name)
    
def new_schedule():
    """Automatically generate a new schedule by obtaining the next friday for which there is no schedule"""
    global schedules
    global fridays
    global unused_fridays
    global current_schedule
    s = schedule_classes.Schedule(fridays[next_free_date_index(unused_fridays)])
    current_schedule = s
    schedules.append(s)
    print ("Schedule created ({0})".format(s.date))

def new_run():
    global current_run
    global current_line
    global current_schedule
    if current_schedule == None:
        print ("No schedule selected")
        select_schedule()
    if current_line == None:
        print("No line selected.")
        select_line()
    run_date = current_schedule.next_run_date(current_line)
    print("Automatic run date: "+run_date)
    run_total = int(input("Enter expected total for run: "))
    current_run = schedule_classes.Run(run_date, run_total)
    # Add run to current schedule
    success = current_schedule.add_run(current_line.name, current_run)
    if success == False:
        print("Adding current run failed. Returning to main menu.")
    else:
        print("Run added.")

def new_batch():
    global production_lines
    global current_schedule
    global current_run
    global current_line
    if not current_schedule:
        select_schedule()
    if not current_line:
        select_line()
    if not current_run:
        print ("No current run.")
        print ("0 -- Select run from current schedule")
        print ("1 -- Create new run")
        selection = -1
        while not selection == 0 or not selection == 1:
            selection = int(input("Selection: "))
            if selection == 0:
                select_run()
            elif selection == 1:
                new_run()
    print(current_schedule.to_pretty_string())     
    print(current_line.name + " -- run date " + current_run.date)
##    #check if any runs exist
##    if len(current_schedule.runs) > 0:
##        # check if the line exists in the dictionary
##        if current_schedule.runs[line_name] in current_schedule.runs:
##            runs = current_schedule.runs[line_name]
##            #check if any runs exist for this line
##            if len(runs) > 0:
##                print("Runs: ")
##                for r in zip(range(len(runs)), runs):
##                    print (r.to_pretty_string())
##                selection = int(input("Select run: "))
##                current_run = runs[selection]
##            else:
##                current_run = schedule_classes.Run(current_schedule.date)
##    else: #no runs or lines exist
##        current_run = schedule_classes.Run(current_schedule.date)

    # Now we create the batch
    another_batch = 0
    while another_batch == 0:
        print("Creating new batch...")
        # select product
        short_code = input("Enter short name (first two letters of brand): ")
        p_list = []
        for p in current_line.products:
            #Find products that start with the short code (case insensitive)
            if p.brand.lower().startswith(short_code.lower()):
                p_list.append(p)
        for i, pro in zip(range(len(p_list)), p_list):
            print (str(i) + " -- " + pro.to_pretty_string())
        selection = int(input("Select product: "))
        selected_product = p_list[selection]
        print (selected_product.to_pretty_string() + " selected.")
        
        # select pallette
        for i, pal in zip(range(len(current_line.pallettes)), current_line.pallettes):
            print (str(i) + " -- " + pal)
        selection = int(input("Select pallette: "))
        selected_pallette = current_line.pallettes[selection]
        qty = int(input("Enter quantity: "))
        b = schedule_classes.Batch(selected_product, selected_pallette, qty)
        if current_run.add_batch(b) == False:
            print("Adding batch failed.")
        else:
            print ("Batch added. (" +b.to_pretty_string()+")")
        print ("0 -- Add another batch")
        print ("1 -- Return to main menu")
        another_batch = input("Selection: ")
    current_run = None
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

def print_current_data():
    global current_schedule
    global current_line
    global current_run
    if current_schedule:
        print("Schedule: "+current_schedule.to_pretty_string())
    else:
        print("No schedule selected.")
    if current_line:
        print("Line: " + current_line.to_pretty_string())
    else:
        print("No line selected.")
    if current_run:
        print("Run: "+current_run.to_pretty_string())
    else:
        print("No run selected.")

def init_data():
    global current_schedule
    global current_line
    global current_run
    global fridays
    global unused_fridays
    global production_lines
    global schedules
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

def save_to_excel():
    print ('TODO')

def save_raw():
    print ('TODO')
    
def print_main_prompt_menu():
    print ("\nEntity Builder~")
    print ("1) New schedule")
    print ("2) New run")
    print ("3) New batch")
    print ("4) Select line")
    print ("5) Select run")
    print ("6) Select schedule")
    print ("7) Print current data")
    print ("0) Quit\n")

def error(error_message = None):
    if not error_message:
        print ("Something went wrong.")
    else:
        print ("Error: "+error_message)

init_data()
funcs = {   1: new_schedule,
            2: new_run,
            3: new_batch,
            4: select_line,
            5: select_run,
            6: select_schedule,
            7: print_current_data
        }
choice = -1
while not choice == '0':
    print_main_prompt_menu()
    choice = input('>: ')
    if not len(choice) == 1: #not a valid size
        error("input size must be equal to 1")
        continue
    choice = int(choice.strip()) # remove white space and convert to int
    if choice == 0:
        print("Quitting...")
        sys.exit()
    else:
        try:
            funcs[choice]() # execute the chosen function based on funcs dictionary
        except KeyError:
            error("Function could not be found in dictionary")
    choice = -1
    
        
