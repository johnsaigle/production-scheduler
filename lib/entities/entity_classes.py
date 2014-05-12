class Product:
  """Represents one type of product produced in a batch on some Line"""
  def __init__(self, brand, kind, size, base_unit):
      self.brand = brand
      self.kind = kind # placeholder for what the product is -- can be oil visocosity, ATF (automatic transmission fluid, PSF (powersteering fluid etc 
      self.size = size # products per pallette
      self.base_unit = base_unit

    #returns a string for nice output
  def to_pretty_string(self):
      return ", ".join([self.brand, self.kind, self.brand, self.size])

  def to_csv_string(self):
      return ",".join([self.brand, self.kind, self.size, self.base_unit])

class Line:
  """Represents one production line in the plant"""
  def __init__(self, name, products, pallettes):
      self.name = name
      self.products = products # a list of products packaged by this line
      self.pallettes = pallettes # an enum type represeting the pallette type for this line

  def populate_product_list(valid_products):
      for product in products:
          add_new_product_to_list(product)

  def add_new_product_to_list(product_as_csv_formatted_string):
      params = product_as_csv_formatted_string.split(',')
      products.add(Product(params[0], params[1], params[2]))

  def populate_pallette_list(valid_pallettes_as_csv_formatted_string):
      pallettes = valid_pallettes_as_csv_formatted_string.split(',')

    
