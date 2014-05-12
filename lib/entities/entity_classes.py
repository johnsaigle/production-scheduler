#Note: change all to_pretty_string to __repr__
class Product:
  """Represents one type of product produced in a batch on some Line"""
  def __init__(self, brand, kind, size, base_unit=None):
      self.brand = brand
      self.kind = kind # placeholder for what the product is -- can be oil visocosity, ATF (automatic transmission fluid, PSF (powersteering fluid etc 
      self.size = size # products per pallette
      self.base_unit = base_unit

    #returns a string for nice output
  def to_pretty_string(self):
      return ", ".join([self.brand, self.kind, self.size])

  def as_list(self):
      to_return = []
      to_return.append(self.brand)
      to_return.append(self.kind)
      to_return.append(self.size)
      return to_return                            

class Line:
  """Represents one production line in the plant"""
  def __init__(self, name):
      self.name = name
      self.products = [] # a list of products packaged by this line
      self.pallettes = [] # an enum type represeting the pallette type for this line

  def add_new_product_to_list(self, product_as_csv_list):
      if len(product_as_csv_list) > 2:
        new_product = Product(product_as_csv_list[0], product_as_csv_list[1], product_as_csv_list[2])
        self.products.append(new_product)
        print (new_product.to_pretty_string() + " added.")
      else:
        print ("Error with product creation. Passed list is too small")

  def populate_product_list(self, valid_products):
      for product in valid_products:
          self.add_new_product_to_list(product)

  def add_new_pallette(self, pallette):
      self.pallettes.append(pallette)

  def print_products(self):
    for p in self.products:
      print (p.to_pretty_string())

  def to_pretty_string(self):
      return self.name + ". "+str(len(self.products)) +" products produced."

    
