import os
import csv
from lib.entities import entity_classes

def load_from_csv(filepath):
  """ Creates a csv-formatted list representing name and pallette info for a line"""
  rows_to_return = []
  with open(filepath, newline='') as csvfile:
     reader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in reader:
       rows_to_return.append(row)
  return rows_to_return

def build_lines():
  """Construct the production lines based on data csv data info"""
  production_lines = []
  production_line_information = load_from_csv('C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\lines\\lines.csv')
  print (os.getcwd())
  print (production_line_information)
  for row in production_line_information:
    pallettes = []
    line_name = row[0] # first element of this row
    #Create the line
    line = entity_classes.Line(line_name)
    production_lines.append(line) 
    # Add product info
    product_source_name = line_name + '.csv'
    product_info = load_from_csv('C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\products\\'+product_source_name)
    line.populate_product_list(product_info)
    #Add pallette info
    i = 1
    while i < len(row):
      line.add_new_pallette(row[i])
      i += 1

    print ("\nFinished building line "+line_name)
    print (line.to_pretty_string())
    
  return production_lines
