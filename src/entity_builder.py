#!/usr/bin/python
import datetime
import sys
from lib.entities import schedule_classes
from lib.loaders import *
  
def new_schedule_menu():
    sched_date = input("Enter the date: ") # convert date input to individual chars
    sched_date = datetime.datetime.strptime(sched_date, '%d%m%y').strftime('%d/%m/%y')
    s = schedule_classes.Schedule(sched_date)
    current_schedule = s
    schedules.append(s)
    print

def new_run_menu():
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
              print ("["+i+"] ", s.to_pretty_string())
      else:
          print ("Invalid input. Returning...")
          return False
  

def new_batch_menu():
  if current_run:
      print ("\n1) Add to current run")
      print ("2) Select run from current schedule")
      print ("3) Select different schedule")
      print ("0) Main menu")
      print ("Current run: "+current_run.date +". Current schedule: " +current_schedule.date+".\n")
      choice = input(">: ")
      if choice == 'y' or choice == '1':
          # add the new batch to the current run
          print ("TODO")
      elif choice == 'n' or choice == '2':
          # select different run
            runs_by_date = current_schedule.runs_by_date()
            paired = zip(range(1, len(current_schedule.runs)+1), runs_by_date)
            for pair in paired:   
                print ("[{index}] {run_string}".format(index=pair[0], run_string=pair[1]))
            selection = int(input("Enter index: "))
            current_run = runs_by_date[selection]
      elif choice == '3':
          # select different schedule
          print ("TODO")
          return False
      else:
          invalid()

def init_data():
    print ('TODO')

def save_to_excel():
    print ('TODO')

def save_raw():
    print ('TODO')
    
def print_main_prompt_menu():
    print ("Entity Builder~")
    print ("\n1) New schedule")
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
production_lines = []
schedules =[]
current_schedule = None
current_line = None
current_run = None
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
    
        
