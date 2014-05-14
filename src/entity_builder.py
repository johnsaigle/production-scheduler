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
    global unused_fridays
    unused_fridays[datelist.index(date_as_isoformat)] = 1 # this is a bit vector
    
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
    if current_line == None:
        select_line()
    try:
        runs_for_line = current_schedule.runs[current_line.name]
        for i, r in zip(range(len(runs_for_line)), runs_for_line):
            print (str(i) +" -- " +r.to_pretty_string())
        while True:
            selection = int(input("Select run: "))
            if selection >= 0 and selection < len(runs_for_line):
                break
        current_run = runs_for_line[selection]
        print ("Current run: " +current_run.to_pretty_string())
    except KeyError:
        print("No runs initialized for "+current_line.name+".")
        while True:
            choice = input("Create new run? (y/n) ")
            if choice == 'y':
                new_run()
                break
            elif choice == 'n':
                break

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
    free_date = fridays[next_free_date_index(unused_fridays)]
    s = schedule_classes.Schedule(free_date)
    mark_date_as_used(free_date)
    current_schedule = s
    schedules.append(s)
    print ("Schedule created ({0})".format(s.date))

def new_run():
    global current_run
    global current_line
    global current_schedule
    global modified_schedules
    if current_schedule == None:
        print ("No schedule selected")
        select_schedule()
    if current_line == None:
        print("No line selected.")
        select_line()
    run_date = current_schedule.next_run_date(current_line)
    run_total = int(input("Enter expected total for run: "))
    current_run = schedule_classes.Run(run_date, run_total)
    # Add run to current schedule
    success = current_schedule.add_run(current_line.name, current_run)
    if success == False:
        print("Adding current run failed. Returning to main menu.")
    else:
        print("Run added.")
        if not current_schedule in modified_schedules:
            modified_schedules.append(current_schedule)
    print ("Current run: "+current_run.to_pretty_string())

def new_batch():
    global production_lines
    global current_schedule
    global current_run
    global current_line
    global modified_schedules
    if not current_schedule:
        select_schedule()
    if not current_line:
        select_line()
    if not current_run:
        print ("No current run.")
        print ("0 -- Select run from current schedule")
        print ("1 -- Create new run")
        while True:
            selection = int(input("Selection: "))
            if selection == 0:
                select_run()
                break
            elif selection == 1:
                new_run()
                break
    print("\nAll necessary data successfully initialized:")
    print("Schedule "+current_schedule.to_pretty_string())     
    print(current_line.name + " -- run date " + current_run.date)

    while True:
        print("\nCreating new batch...")
        # select product
        p_list = []
        while True:
            short_code = input("Enter short name (first two letters of brand): ")
            for p in current_line.products:
                #Find products that start with the short code (case insensitive)
                if p.brand.lower().startswith(short_code.lower()):
                    p_list.append(p)
            if len(p_list) > 0:
                break
            else:
                print("No match for " +short_code+" in line "+current_line.name)
                
        for i, pro in zip(range(len(p_list)), p_list):
            print (str(i) + " -- " + pro.to_pretty_string())
        selection = int(input("Select product: "))
        selected_product = p_list[selection]
        print (selected_product.to_pretty_string() + " selected.")

        # select pallette        
        for i, pal in zip(range(len(current_line.pallettes)), current_line.pallettes):
            print (str(i) + " -- " + pal)
        while True:
            selection = int(input("Select pallette: "))
            if selection >= 0 and selection < len(current_line.pallettes) -1:
                break
        selected_pallette = current_line.pallettes[selection]
        qty = int(input("Enter quantity: "))
        b = schedule_classes.Batch(selected_product, selected_pallette, qty)
        if current_run.add_batch(b) == False:
            print("Adding batch failed.")
        else:
            print ("Batch added. (" +b.to_pretty_string()+")")

        # mark this schedule to be written
        if not current_schedule in modified_schedules:
            modified_schedules.append(current_schedule)

        repeat = int(input("Enter 1 to add another batch or enter any key to return to main menu: "))
        if not repeat == 1: # return to main menu
            break
        
    current_run = None

def print_selected_data():
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

def print_all_data():
    global schedules
    for s in schedules:
        print("Schedule " +s.to_pretty_string())
        print("Runs:")
        s.print_all_runs_with_batches()

def save_data():
    global modified_schedules
    global schedule_directory
    if len(modified_schedules) > 0:
        print("Saving modified schedules...")
        schedule_loader.save_multiple_schedules(modified_schedules, schedule_directory)
    else:
        print("Nothing to save!")
        
def init_data():
    global current_schedule
    global current_line
    global current_run
    global fridays
    global unused_fridays
    global production_lines
    global schedules
    global schedule_directory
    current_schedule = None
    current_line = None
    current_run = None
    fridays = generate_fridays()
    unused_fridays = [0] * len(fridays) # this is a bit vector to keep track of the next avaialble friday
    production_lines = entity_loader.build_lines() # load production line data
    print ("\nLoading previous schedules...")
    schedules = schedule_loader.build_multiple_schedules(fridays, schedule_directory)
    # process loaded schedules
    if len(schedules) > 0:   
        print ("\n"+str(len(schedules))+" schedules loaded:")
        for s in schedules:
            print(s.to_pretty_string())
            mark_date_as_used(s.date) # mark availability
    
def print_main_prompt_menu():
    print ("\nEntity Builder~")
    print ("1) New schedule")
    print ("2) New run")
    print ("3) New batch")
    print ("4) Select line")
    print ("5) Select run")
    print ("6) Select schedule")
    print ("7) Print selected data (current schedule, line and run)")
    print ("8) Print all schedule data")
    print ("9) Save to csv")
    print ("q) Quit\n")

def error(error_message = None):
    if not error_message:
        print ("Something went wrong.")
    else:
        print ("Error: "+error_message)

schedule_directory = "C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\"
init_data()
modified_schedules = []
funcs = {   1: new_schedule,
            2: new_run,
            3: new_batch,
            4: select_line,
            5: select_run,
            6: select_schedule,
            7: print_selected_data,
            8: print_all_data,
            9: save_data
        }
choice = -1
while not choice == '0':
    print_main_prompt_menu()
    choice = input('>: ')
    if not len(choice) == 1: #not a valid size
        error("input size must be equal to 1")
        continue
    choice = choice.strip() # remove white space and convert to int
    if choice == 'q':
        print("Quitting...")
        sys.exit()
    else:
        choice = int(choice)
        try:
            funcs[choice]() # execute the chosen function based on funcs dictionary
        except KeyError:
            error("Function could not be found in dictionary")
    choice = -1
    
        
