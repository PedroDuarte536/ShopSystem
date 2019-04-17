# Only used for rating searches in Product.search_by_query
# It will be summed to the position of query in word
# in case it is not in the begginning so that result
# appears later - DOES NOT ENFORCE ANYTHING
NUM_WORDS_PRODUCT_NAME = 5

class Product:
    def __init__ (self, name, price, unit="uni"):
        self.name = str(name)
        self.unit = unit
        self.price = price

    def get_name (self):
        return self.name

    def get_unit (self):
        return self.unit

    def get_price (self):
        return self.price

    def set_price (self, price):
        self.price = price

    # Rates results according to relevance
    # If word starts with query, rating is position of
    # the word in the name
    # If query is in the middle rating is position in
    # the whole name plus a const, so it appears after
    # the other results
    def search_by_query (self, query):
        name_words = self.name.upper().split()              # Every word in the product name
        name_query_pos = self.name.upper().find(query)      # Position of query in product name
        
        for word in name_words:                             # Check if any of the words in 
            if word.startswith(query):                      # product name starts with query
                return name_words.index(word)
            
        if name_query_pos > 0:                              # Check if query is in the middle
            return name_query_pos + NUM_WORDS_PRODUCT_NAME  # of a word

        return -1

    def to_dict (self):
        return {"name":self.get_name(), "price":self.get_price(), "unit":self.get_unit()}


class ProductManager:
    def __init__ (self):
        self.products = dict()                              # {reference:Product()}

    def get_by_reference (self, reference):
        if reference in self.products:
            return self.products[reference]
        else:
            return False

    def get_all (self):
        return self.products

    def new_product (self, name, price, reference, unit="uni", groups=[0]):
        if reference:
            if reference not in self.products:
                self.products[reference] = Product(name, price)
                return True
            else:
                return False

        return False

    def search_by_query (self, query):
        query = query.upper()
        results = []                                        # [[match_rating, {reference:Product()}]]
        
        for reference, product in self.products.items():
            product_search = product.search_by_query(query)

            if reference.upper().startswith(query):         # Check if query is reference
                results.insert(0, [0, {reference:product}])

            elif product_search >= 0:                       # Check for Product().search_by_query()
                if len(results) > 0:                        # Order result by its rating
                    for r in results:
                        if product_search < r[0]:
                            results.insert(results.index(r), [product_search, {reference:product}])
                            break
                        
                        elif results.index(r) == len(results)-1:
                            results.append([product_search, {reference:product}])
                            break
                else:
                    results.append([product_search, {reference:product}])

        # [{reference:Product()}]
        results = [r[1] for r in results]                   
        # {reference:Product()}
        results = {ref:prod for r in results for ref, prod in r.items()}
        
        return results

    def to_dict (self):
        product_list = []
        for reference, product in self.products.items():
            product_dict = product.to_dict()
            product_dict["reference"] = reference
            product_list.append(product_dict)

        return {"products":product_list}

    def from_dict (self, product_list):
        for product in product_list:
            self.new_product(product["name"], product["price"], product["reference"],
                             product["unit"])

class ProductGroup:
    def __init__ (self, name, products=[]):
        self.name = name
        self.products = products

    def get_name (self):
        return self.name

    def add_product (self, reference):
        if reference not in self.products:
            self.products.append(reference)
            return True
        return False

    def remove_product (self, reference):
        if reference in self.products:
            self.products.remove(reference)
            return True
        return False

    def get_products (self):
        return self.products

    def is_in_group (self, reference):
        if reference in self.products:
            return True
        return False

    def to_dict (self):
        product_list = []
        for product in self.products:
            product_list.append(product)
            
        return {"name":self.name, "products":product_list}


class ProductGroupManager:
    def __init__ (self):
        self.groups = dict()

    def next_id (self):
        max_id = max(self.orders.keys())
        return max_id+1

    def new_group (self, name):
        self.groups[self.next_id()] = ProductGroup(name)

    def get_groups (self):
        return self.groups

    def get_by_id (self, ident):
        return self.groups[ident]

    def to_dict (self):
        group_list = []
        for ident, group in self.groups.items():
            group_dict = group.to_dict()
            group_dict["id"] = ident
            group_list.append(group_dict)

        return {"product_groups":group_list}

    def from_dict (self, group_list):
        for group in group_list:
            self.groups[group["id"]] = ProductGroup(group["name"], group["products"])           
