#!/usr/bin/python
import sys
import datetime
import os
##sys.path.append('../')
from lib.entities import *
from lib.loaders import *

def convert_lazy_date(date_as_list):
    """Cleans up date format -- doesn't work for some dates of length 7"""
    if len(date) == 8:
        return "".join(date_as_list)

    date_as_list[-2:-2] = ['2','0'] #adds 20 to the place of the year
    if len(date_as_list) == 6:
        date_as_list.insert(1,'0')
        date_as_list.insert(0,'0')

    elif len(date_as_list) == 7:
      # either day or month is double digited
      i = date_as_list.index('0') # find first '0'
      if (i == 0):
          date_as_list.insert(2,'0')
      elif (i == 2):
        date_as_list.insert(0,'0')

    date = "".join(date_as_list)
    if len(date) == 8:
        return date
    else:
        print ("Error, date is not size 8")
        return False
  
def new_schedule_menu():
    date = list(input("Enter the date: ")) # convert date input to individual chars
    date = convert_lazy_date(date)
    if not date:
        print ("Conversion failed")
        return 1
      
    date = datetime.datetime.strptime(date, '%d%m%y').strftime('%d/%m/%y')
    s = Schedule(date)
    current_schedule = s
    schedules.add(s)

def new_run_menu():
  if current_schedule:
      print ("\n1) Add to current schedule")
      print ("2) Select schedule")
      choice = input(">: ")
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
          print ("Invalid input. Returning...")
          return False
    
def print_main_prompt_menu():
    print ("Entity Builder~")
    print ("\n1) New schedule")
    print ("2) New run")
    print ("3) New batch")
    print ("4) Load (import from csv)")
    print ("5) Save (export to csv)")
    print ("6) Save raw (not formatted for excel)")
    print ("0) Quit\n")

production_lines = []
schedules =[]
current_schedule = None
current_line = None
current_run = None
choice = 1
while not choice == '0':
    print_main_prompt_menu()
    choice = input('>: ')
    choice = int(choice.strip()) # remove white space and convert to int
    if choice == 1:
        print("TODO: Link functions to menu")
    else:
        print("Please make a valid selection")
    
        
