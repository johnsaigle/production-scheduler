import csv

def load_csv_info(filepath):
  """ Loads data from a csv file and returns the results"""
  rows_to_return = []
  try:
    with open(filepath, newline='') as csvfile:
       reader = csv.reader(csvfile, delimiter=',', quotechar='|')
       for row in reader:
         if len(row) > 0:
           rows_to_return.append(row)
  except Exception as e:
    print ("File does not exist -- "+filepath)
    return None
  return rows_to_return

def save_csv_info(filepath, formatted_data):
  with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(formatted_data)
