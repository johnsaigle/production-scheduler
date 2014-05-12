from lib.entities import entity_classes

def load_product_list_from_csv(filename, filepath=None):
  """ Returns a list of all Product objects stored in the csv file"""
  if not filename.endswith('.csv'):
    filename += '.csv'
  if filepath == None:
    # load from working directory
    with open(filename, newline='') as csvfile:
       datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
       product_list = next(datareader)
       return product_list
  else:
    # load from filepath
    print ("TODO")
