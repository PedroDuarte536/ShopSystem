class Warehouse:
    def __init__ (self, name, products=dict()):
        self.name = name
        self.products = products

    def get_stock (self):
        return self.products

    def get_stock_by_reference (self, reference):
        if reference in self.products:
            return self.products[reference]
        return 0

    def add_to_stock (self, reference, amount):
        if reference in self.products:
            self.products[reference] += amount
        else:
            self.products[reference] = amount

    def take_from_stock (self, reference, amount):
        if reference in self.products:
            self.products[reference] -= amount
        else:
            self.products[reference] = 0

    def to_dict (self):
        product_list = []
        for reference, amount in self.products.items():
            product_dict = {"reference": reference, "amount":amount}
            product_list.append(product_dict)

        return {"name":self.name, "products":product_list}
        

class WarehouseManager:
    def __init__ (self):
        self.warehouses = dict()

    def new_warehouse (self, name, products=dict()):
        self.warehouses[len(self.warehouses)] = Warehouse(name)

    def get_all (self):
        return self.warehouses

    def get_by_id (self, ident):
        return self.warehouses[ident]

    def get_products_by_id (self, warehouse=0):
        return self.warehouses[warehouse].products

    def get_warehouses_num (self):
        return len(self.warehouses)

    def to_dict (self):
        warehouse_list = [warehouse.to_dict() for warehouse in self.warehouses.values()]
        return {"warehouses":warehouse_list}

    def from_dict (self, warehouse_list):
        for warehouse in warehouse_list:
            product_dict = dict()
            for product in warehouse["products"]:
                product_dict[product["reference"]] = product["amount"]
                
            self.new_warehouse(warehouse["name"], product_dict)

            
        
