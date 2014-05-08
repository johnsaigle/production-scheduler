class Product:
  """Represents one type of product produced in a batch on some Line"""
    def __init__(self, brand, kind, sizebase_unit):
        self.brand = brand
        self.kind = kind # placeholder for what the product is -- can be oil visocosity, ATF (automatic transmission fluid, PSF (powersteering fluid etc 
        self.size = size # products per pallette
        self.base_unit = base_unit

    #returns a string for nice output and for csv writing
    def to_pretty_string(self):
        return ", ".join([self.brand, self.kind, self.brand, self.size]) 


class Line:
  """Represents one production line in the plant"""
    def __init__(self, name, products, pallettes):
        self.name = name
        self.products = products # a list of products packaged by this line
        self.pallettes = pallettes # an enum type represeting the pallette type for this line
        self.runs = {}

    
