import csv
import os.path
def load_csv_info(filepath):
  """ Loads data from a csv file and returns the results"""
  rows_to_return = []
  base = os.path.basename(filepath)
  try:
    with open(filepath, newline='') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='|')
      print("Opening file "+base)
      for row in reader:
        if len(row) > 0:
          rows_to_return.append(row)
  except Exception as e:
    print ("File does not exist -- "+base)
    return None
  return rows_to_return

def save_csv_info(filepath, formatted_data):
  if os.path.isfile(filepath):
    # if file already exists, verify that the user wishes to overwrite
    base = os.path.basename(filepath)
    ovr = input("File '"+base+"' already exists. Overwrite? (y/n)")
    if ovr == 'y':
        ovr2 = input("Are you sure? (y/n)")
        if ovr2 == 'y':
          # Overwrite file
            with open(filepath, 'w') as f:
              writer = csv.writer(f)
              writer.writerows(formatted_data)
        else:
            print("File not overwritten.")
            return False
    else:
      print("File not overwritten.")
      return False
      print("")
  else:
    with open(filepath, 'w') as f:
      writer = csv.writer(f)
      writer.writerows(formatted_data)
  
