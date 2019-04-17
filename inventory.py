from products import Product, ProductManager, ProductGroup, ProductGroupManager
from warehouses import Warehouse, WarehouseManager
from shop import Order, OrderManager
from clients import Client, ClientManager

from interface import Interface

import json

class CreateOrder(Interface):
    def __init__ (self, products, clients, order=False):
        self.products = products
        self.clients = clients

        if order == False:
            self.order = Order()
        else:
            self.order= order
        
    def add_product (self, command=False):
        if command:
            return "Add Product"

        product_reference = ""
        while product_reference not in self.products:
            product_reference = input("Product Reference: ")

        product_amount = 0
        while product_amount <= 0:
            product_amount = int(input("Amount: "))
            
        self.order.add_product(product_reference, self.products[product_reference], product_amount)

    def remove_product (self, command=False):
        if command:
            return "Remove Product"

        if not self.order.remove_product(input("Reference: ")):
            print("No such reference!")

    def show_order (self, command=False):
        if command:
            return "Show Order"

        for reference, product in self.order.get_products().items():
            print("\t"+str(product.get_amount())+" "+product.get_product().get_name()+" ("+reference+")"+"\t\t"+str(product.get_product().get_price())+"$\t"+str(product.get_product().get_price()*product.get_amount())+"$")

        print("\n\tTOTAL: "+str(self.order.total_price())+"$")

    def set_client (self, command=False):
        if command:
            return "Set Client"

        a.list_clients()
        
        client = 0
        while client not in self.clients.keys():
            client = int(input("Which Client? "))
            
        self.order.set_client(client)
            
    def behaviour (self):
        return [self.add_product, self.remove_product, self.show_order, self.set_client]

    def run (self):
        return super().run(self.behaviour())

        
class Inventory(Interface):
    def __init__ (self):
        self.product_manager = ProductManager()
        self.warehouse_manager = WarehouseManager()
        self.order_manager = OrderManager()
        self.client_manager = ClientManager()
        self.product_group_manager = ProductGroupManager()

        prods_list = self.product_manager.get_all().keys()
        self.product_group_manager.from_dict([{"id":0,"name":"ALL PRODUCTS", "products":prods_list},{"id":1,"name":"OLD PRODUCTS", "products":[]}])

        self.load()

    def save (self, command=False):
        if command:
            return "Save"

        final_dict = dict() 
        final_dict["products"] = self.product_manager.to_dict()["products"]
        final_dict["warehouses"] = self.warehouse_manager.to_dict()["warehouses"]
        final_dict["orders"] = self.order_manager.to_dict()["orders"]
        final_dict["clients"] = self.client_manager.to_dict()["clients"]
        final_dict["product_groups"] = self.product_group_manager.to_dict()["product_groups"]

        with open("data.json", "w") as file:
            json.dump(final_dict, file)

    def load (self, command=False):
        if command:
            return "Load"

        with open("data.json", "r") as file:
            data = json.load(file)

        
        self.product_manager.from_dict(data["products"])
        self.warehouse_manager.from_dict(data["warehouses"])
        self.order_manager.from_dict(data["orders"])
        self.client_manager.from_dict(data["clients"])
        self.product_group_manager.from_dict(data["product_groups"])

    def get_order_by_client (self, command=False):
        if command:
            return "Order By Client"

        self.list_clients()
        client = 0
        while client not in self.client_manager.get_all().keys():
            client = int(input("Which Client? "))

        for ident, order in self.order_manager.get_by_client(client).items():
            products = {ref:product.get_amount() for ref, product in order.get_products().items()}
            print("\t"+str(ident)+" -> "+str(products)+" - "+str(order.total_price())+"$")

    def search_client (self, command=False):
        if command:
            return "Search Client"

        for client in self.client_manager.search_by_query(input("Query: ")):
            print("\t"+client.get_name()+"\t\t"+str(client.get_nif())+"\t"+str(client.get_mobile()))

    def discontinue_product (self, command=False):
        if command:
            return "Discontinue"

        self.list_products()
        product = ""
        while product not in self.product_manager.get_all().keys():
            product = input("Which Product? ")

        if self.product_group_manager.get_by_id(0).is_in_group(product):
            self.product_group_manager.get_by_id(0).remove_product(product)
            self.product_group_manager.get_by_id(1).add_product(product)
        else:
            print("Product is already discontinued")

    def make_current (self, command=False):
        if command:
            return "Make Current"

        self.list_products()
        product = ""
        while product not in self.product_manager.get_all().keys():
            product = input("Which Product? ")

        if self.product_group_manager.get_by_id(1).is_in_group(product):
            self.product_group_manager.get_by_id(1).remove_product(product)
            self.product_group_manager.get_by_id(0).add_product(product)
        else:
            print("Product is already current")

    def create_client (self, command=False):
        if command:
            return "Create Client"

        self.client_manager.new_client(input("Client Name: "), int(input("Client NIF: ")), int(input("Client Mobile: ")))        

    def create_product_group (self, command=False):
        if command:
            return "Create Product Group"

        self.product_group_manager.new_group(input("Group Name: "))
        
    def add_to_group (self, command=False):
        if command:
            return "Add To Group"

        self.list_groups()
        group = ""
        while group not in self.product_group_manager.get_groups().keys():
            group = int(input("To Which Group? "))

        self.list_products()
        product = ""
        while product not in self.product_manager.get_all().keys():
            product = input("Which Product? ")

        self.product_group_manager.get_by_id(group).add_product(product)        

    def list_groups (self, command=False):
        if command:
            return "List Groups"

        for ident, group in self.product_group_manager.get_groups().items():
            print("\t"+str(ident)+" -> "+group.name+" - "+", ".join(group.get_products()))

    def list_clients (self, command=False):
        if command:
            return "List Clients"

        for ident, client in self.client_manager.get_all().items():
            print("\t"+str(ident)+" -> "+client.get_name()+" :\t"+str(client.get_nif())+"\t"+str(client.get_mobile()))
        
    def create_order (self, command=False):
        if command:
            return "Create Order"

        self.list_products()
        print("Select the products and then enter 'quit' when you've finished")

        order = CreateOrder(self.product_manager.get_all(), self.client_manager.get_all())
        order.run()
        self.order_manager.add_order(order.order)

    def create_warehouse (self, command=False):
        if command:
            return "Create Warehouse"

        self.warehouse_manager.new_warehouse(input("Warehouse Name: "))

    def list_warehouses (self, command=False):
        if command:
            return "List Warehouses"

        for ident, warehouse in self.warehouse_manager.get_all().items():
            print("\t"+str(ident)+" -> "+warehouse.name)

    def add_stock_to_warehouse (self, command=False):
        if command:
            return "Add To Stock"

        self.list_warehouses()

        warehouse_selected = -1
        while warehouse_selected < 0 or warehouse_selected > self.warehouse_manager.get_warehouses_num()-1:
            warehouse_selected = int(input("Which Warehouse To? "))

        product_reference = ""
        while product_reference not in self.product_manager.get_all():
            product_reference = input("Product Reference: ")

        amount = 0
        while amount <= 0:
            amount = int(input("Amount: "))

        self.warehouse_manager.get_by_id(warehouse_selected).add_to_stock(product_reference, amount)   

    def take_stock_from_warehouse (self, command=False):
        if command:
            return "Take From Stock"

        self.list_warehouses()

        warehouse_selected = -1
        while warehouse_selected < 0 or warehouse_selected > self.warehouse_manager.get_warehouses_num()-1:
            warehouse_selected = int(input("Which Warehouse To? "))

        product_reference = ""
        while product_reference not in self.product_manager.get_all():
            product_reference = input("Product Reference: ")

        amount = 0
        while amount <= 0:
            amount = int(input("Amount: "))

        self.warehouse_manager.get_by_id(warehouse_selected).take_from_stock(product_reference, amount)

    def check_product_stock (self, command=False):
        if command:
            return "Check Product Stock"

        product_reference = ""
        while product_reference not in self.product_manager.get_all():
            product_reference = input("Product Reference: ")
            
        for warehouse in self.warehouse_manager.get_all().values():
            print("\t"+warehouse.name+" -> "+str(warehouse.get_stock_by_reference(product_reference)))        

    def create_product (self, command=False):
        if command:
            return "Create Product"
            
        if self.product_manager.new_product(input("Product Name:"), int(input("Product Price:")), input("Product Reference:")):
            print("Product created successfully!")
        else:
            print("Error while creating the product...")

    def list_products (self, command=False):
        if command:
            return "List Products"

        self.list_groups()
        group = ""
        while group not in self.product_group_manager.get_groups().keys():
            group = int(input("Which Group? "))

        group = self.product_group_manager.get_by_id(group)

        for ref in group.get_products():
            product = self.product_manager.get_by_reference(ref)
            print("\t"+ref+" -> "+product.get_name()+" :\t"+str(product.get_price())+"$")

    def get_product_by_reference (self, command=False):
        if command:
            return "Get Reference"

        reference = input("Reference: ")
        product = self.product_manager.get_by_reference(reference)

        if product:
            print("\t"+reference+" -> "+product.get_name()+" :\t"+str(product.get_price())+"$")
        else:
            print("No such reference")

    def search_product (self, command=False):
        if command:
            return "Search Product"

        for ref, product in self.product_manager.search_by_query(input("Query: ")).items():
            print("\t"+ref+" -> "+product.get_name()+" :\t"+str(product.get_price())+"$")
            
    def behaviour (self):
        return [self.create_product, self.list_products, self.get_product_by_reference, self.search_product,
                self.create_warehouse, self.list_warehouses, self.add_stock_to_warehouse,
                self.take_stock_from_warehouse, self.check_product_stock, self.create_order,
                self.create_client, self.create_product_group, self.add_to_group, self.list_groups,
                self.list_clients, self.discontinue_product, self.make_current, self.search_client,
                self.get_order_by_client, self.save, self.load]

    def run(self):
        super().run(self.behaviour())
        
        
a = Inventory()
a.run()
            
