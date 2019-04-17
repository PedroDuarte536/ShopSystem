from products import Product
class CheckOutDesk:
    def __init__ (self, warehouse=-1):
        self.shop = shop_id
        self.warehouse = int(warehouse)


class Shop:
    def __init__ (self):
        self.checkout_desks = dict()
        self.orders = dict()


class ProductOrder:
    def __init__ (self, product, amount=0):
        self.product = product
        self.amount = amount

    def get_product (self):
        return self.product

    def get_amount (self):
        return self.amount

    def increase_amount (self, amount):
        self.amount += amount

    def decrease_amount (self, amount):
        if self.amount - amount >= 0:
            self.amount -= amount
            return True
        return False

    def total_price (self):
        return self.product.price*self.amount

    def to_dict (self):
        if self.get_amount() > 0:
            product_dict = self.product.to_dict()
            product_dict["amount"] = self.get_amount()
            return product_dict
        return False
        

class Order:
    def __init__ (self, products=dict(), client=0):
        self.products = products
        self.client = client

    def get_client (self):
        return self.client

    def set_client (self, client):
        self.client = client

    def get_products (self):
        return self.products
    
    def add_product (self, reference, product, amount):
        if reference in self.products:
            self.products[reference].increase_amount(amount)

        else:
            self.products[reference] = ProductOrder(product, amount)

    def remove_product (self, reference):
        if self.products.pop(reference, False) == False:
            return False
        return True

    def total_price (self):
        total = 0
        for prod in self.products.values():
            total += prod.total_price()

        return total

    def to_dict (self):
        product_list = []
        for reference, product in self.products.items():
            product_dict = product.to_dict()
            if product_dict:
                product_dict["reference"] = reference
                product_list.append(product_dict)

        if product_list:
            return {"products":product_list,"client":self.client}
        return False

class OrderManager:
    def __init__ (self):
        self.orders = dict()

    def next_id (self):
        if self.orders:
            max_id = max(self.orders.keys())
            return max_id+1
        return 1
        
    def add_order (self, order):
        self.orders[self.next_id()] = order

    def get_by_client (self, client):
        results = []

        for ident, order in self.orders.items():
            if order.get_client() == client:
                results.append({ident:order})
                 
        # {id:Order()}
        results = {ident:client for r in results for ident, client in r.items()}

        return results

    def to_dict (self):
        order_list = []
        for ident, order in self.orders.items():
            order = order.to_dict()
            if order:
                order["id"] = ident
                order_list.append(order)

        return {"orders":order_list}

    def from_dict (self, orders):
        for order in orders:
            products_dict = dict()
            for product in order["products"]:
                product_order = ProductOrder(Product(product["name"], product["price"], product["unit"]), product["amount"])
                products_dict[product["reference"]] = product_order
                
            self.orders[order["id"]] = Order(products_dict, order["client"])
        
