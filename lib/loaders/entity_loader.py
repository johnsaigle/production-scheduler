import os
import csv
from lib.entities import entity_classes
from . import csv_loader

def build_lines():
  """Construct the production lines based on data csv data info"""
  production_lines = []
  production_line_information = csv_loader.load_csv_info('C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\raw\\lines\\lines.csv')
  print (production_line_information)
  for row in production_line_information:
    pallettes = []
    line_name = row[0] # first element of this row
    print("Loading information for line "+line_name)
    #Create the line
    line = entity_classes.Line(line_name)
    production_lines.append(line) 
    # Add product info
    product_source_name = line_name + '.csv'
    product_info = csv_loader.load_csv_info('C:\\Users\\Brockville\\Documents\\John Summer File\\production-scheduler\\data\\raw\\products\\'+product_source_name)
    line.populate_product_list(product_info)
    #Add pallette info
    i = 1
    while i < len(row):
      line.add_new_pallette(row[i])
      i += 1
    print (line.to_pretty_string())
    print ("Finished building line "+line_name+"\n")
      
  return production_lines
