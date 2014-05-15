#!/usr/bin/python
import datetime
import sys
import os
from lib.entities import schedule_classes
from lib.entities import entity_classes
from lib.loaders import schedule_loader
from lib.loaders import entity_loader
from itertools import repeat

def next_free_date_index(bit_vector):
    """Find the next unsued date according to bit vector parameter"""
    return bit_vector.index(0)

def mark_date_as_used(date_as_isoformat):
    """Mark a date (in isoformat) as being used within the global bit vector"""
    global fridays
    datelist = fridays
    global unused_fridays
    unused_fridays[datelist.index(date_as_isoformat)] = 1 # this is a bit vector
    
def generate_fridays():
    """"Generates a list of all fridays until ewnd of current year"""
    fridays = []
    start_date = datetime.date(2014,1,1)
    today = datetime.date.today()
    end_date = datetime.date(today.year, 12, 31)
    date_to_incr = start_date
    while not date_to_incr.isoweekday() == 5:
        date_to_incr += datetime.timedelta(days=1)
    #date is now equal to the first friday in 2014 when the program was written
    while not date_to_incr > end_date:
        fridays.append(date_to_incr.isoformat())
        date_to_incr += datetime.timedelta(days=7)
    return fridays

def select_schedule():
    """Select the global current schedule"""
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
    """Select the global current run"""
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
    """Set the current line globally"""
    global production_lines
    global current_line
    for i, l in zip(range(len(production_lines)), production_lines):
        print (str(i) +" -- " +l.name)
    current_line = production_lines[int(input("Select line: "))]
    print ("Current line: " +current_line.name)
    
def new_auto_schedule():
    """Automatically generate a new schedule by obtaining the next friday for which there is no schedule"""
    global schedules
    global fridays
    global unused_fridays
    global current_schedule
    free_date = fridays[next_free_date_index(unused_fridays)]
    s = schedule_classes.Schedule(free_date)
    mark_date_as_used(free_date)
    current_schedule = s
    schedules.append(current_schedule)
    print ("Schedule created for {0}".format(current_schedule.date))

def new_manual_schedule():
    """Initialize a schedule by typing in the date in the format YYY-MM-DD"""
    global schedules
    global current_schedule
    while True:
        try:
            date = input("Enter date for the new schedule formatted as YYYY-MM-DD): ")
            man_s  = schedule_classes.Schedule(date)
            man_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date.")
    
    if man_date.isoweekday() == 5:
        mark_date_as_used(datetime.datetime.strftime(man_date, "%Y-%m-%d"))
    current_schedule = man_s
    schedules.append(current_schedule)
    print ("Manual schedule created for {0}".format(current_schedule.date))

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
    # Add run to current schedule
    current_run = schedule_classes.Run(run_date)
    success = current_schedule.add_run(current_line.name, current_run)
    if success == False:
        print("Adding current run failed.")
        current_run = None
        while True: 
            switch_line = input("Select different line? (y/n) ")
            if switch_line == 'y':
                select_line()
                return new_run()
            elif switch_line == 'n':
                print ("Returning to main menu.")
                return False
                
    print("Run added to current schedule.")
    while True:
        try:
            run_total = int(input("Enter expected total for run: "))
            break
        except Exception as e:
            print("Expected total must be a number.")
    current_run.expected_total = run_total
    if not current_schedule in modified_schedules:
        modified_schedules.append(current_schedule)
    print ("Current run: "+current_run.to_pretty_string())
    return True

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
        if len(current_schedule.runs[current_line.name] < 1):
            new_run()
        else:
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
    print("Selected line is "+current_line.name + ". Run date " + current_run.date)
    print("Batch list for current run: ")
    current_run.print_all_batches()
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
        while True:
            selection = int(input("Select product: "))
            if selection >= 0 and selection < len(p_list):
                break
        selected_product = p_list[selection]
        print (selected_product.to_pretty_string() + " selected.")

        # select pallette        
        for i, pal in zip(range(len(current_line.pallettes)), current_line.pallettes):
            print (str(i) + " -- " + pal)
        while True:
            selection = input("Select pallette (u for unknown): ")
            if selection == 'u':
                selected_pallette = "Unknown"
                break
            else:
                selection = int(selection)
                if selection >= 0 and selection < len(current_line.pallettes):
                    selected_pallette = current_line.pallettes[selection]
                    break
        qty = int(input("Enter quantity: "))
        b = schedule_classes.Batch(selected_product, selected_pallette, qty)
        if current_run.add_batch(b) == False:
            print("Adding batch failed.")
        else:
            print ("Batch added. (" +b.to_pretty_string()+")")

        # mark this schedule to be written
        if not current_schedule in modified_schedules:
            modified_schedules.append(current_schedule)

        repeat = input("Enter 0 to add another batch. Press enter to return to main menu: ")

        if repeat != '0': # return to main menu
            break
        
    current_run = None

def print_selected_data():
    global current_schedule
    global current_line
    global current_run
    if current_schedule:
        print(current_schedule.to_pretty_string())
    else:
        print("No schedule selected.")
    if current_line:
        print("Line: " + current_line.to_pretty_string())
    else:
        print("No line selected.")
    if current_run:
        print(current_run.to_pretty_string())
    else:
        print("No run selected.")

def print_all_data():
    global schedules
    for s in schedules:
        print(s.to_pretty_string())
        print("Runs:")
        s.print_all_runs_with_batches()

def save_data():
    global modified_schedules
    global schedule_directory
    if len(modified_schedules) > 0:
        print("Saving modified schedules...")
        schedule_loader.save_multiple_schedules(modified_schedules, schedule_directory)
        modified_schedules = []
    else:
        print("Nothing to save!")

def adj_run_date():
    """Permanently increments the date of the current run"""
    global current_run
    if current_run == None:
        print("No run selected. Returning to main menu.")
        return False
    old_date = current_run.date
    date = datetime.datetime.strptime(current_run.date, "%Y-%m-%d")
    date += datetime.timedelta(days=1)
    current_run.date = date.strftime("%Y-%m-%d")
    print("Date changed from "+old_date +" to "+current_run.date)
        
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
    # get existing schedules
    print ("\nLoading previous schedules...")
    prev_schedules = os.listdir(schedule_directory)
    for ps in prev_schedules:
        ps.rstrip('.csv')
    schedules = schedule_loader.build_multiple_schedules(prev_schedules, schedule_directory)
    # process loaded schedules
    if len(schedules) > 0:   
        print ("\n"+str(len(schedules))+" schedules loaded:")
        for s in schedules:
            print(s.to_pretty_string())
            mark_date_as_used(s.date) # mark availability
    
def print_main_prompt_menu():
    print ("\nEntity Builder~")
    print ("1) Create new schedule automatically (picks first friday without an existing schedule)")
    print ("2) New run")
    print ("3) New batch")
    print ("4) Select line")
    print ("5) Select run")
    print ("6) Select schedule")
    print ("7) Print selected data (current schedule, line and run)")
    print ("8) Print all schedule data")
    print ("9) Save to csv")
    print ("10) Increment run date (for days off)")
    print ("11) Create new schedule manually (if next Friday is a holiday, etc.)")
    print ("q) Quit\n")

def error(error_message = None):
    if not error_message:
        print ("Something went wrong.")
    else:
        print ("Error: "+error_message)

schedule_directory = "C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\schedules\\"
init_data()
modified_schedules = []
funcs = {   1: new_auto_schedule,
            2: new_run,
            3: new_batch,
            4: select_line,
            5: select_run,
            6: select_schedule,
            7: print_selected_data,
            8: print_all_data,
            9: save_data,
            10: adj_run_date,
            11: new_manual_schedule
        }
while True:
    print_main_prompt_menu()
    choice = input('>: ')
    if len(choice) > 2 or len (choice) < 1: #not a valid size
        error("Enter a one- or two-digit number to select an option.")
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
    
        
