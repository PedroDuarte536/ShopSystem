from contacts import Contacts

# Only used for rating searches in Client.search_by_query
# It will be summed to the position of query in word
# in case it is not in the begginning so that result
# appears later - DOES NOT ENFORCE ANYTHING
NUM_WORDS_CLIENT_NAME = 5

class Owner:
    def __init__ (self, name, contacts=Contacts()):
        self.name = name
        self.contacts = contacts

    def get_name (self):
        return self.name

    def get_contacts (self):
        return self.contacts

    def to_dict (self):
        return {"name": self.name, "contacts":self.get_contacts().to_dict()}


class Client(Owner):
    def search_by_query (self, query):
        if self.get_contacts().search_by_query():
            return 0
        
        name_words = self.name.upper().split()              # Every word in the client name
        name_query_pos = self.name.upper().find(query)      # Position of query in client name
        
        for word in name_words:                             # Check if any of the words in 
            if word.startswith(query):                      # client name starts with query
                return name_words.index(word)
            
        if name_query_pos > 0:                              # Check if query is in the middle
            return name_query_pos + NUM_WORDS_CLIENT_NAME  # of a word

        return -1


class ClientManager:
    def __init__ (self):
        self.clients = dict()

    def get_all (self):
        return self.clients
    
    def next_id (self):
        if self.clients:
            max_id = max(self.orders.keys())
            return max_id+1
        return 1

    def new_client (self, name):
        self.clients[self.next_id()] = Client(name)

    def get_by_id (self, ident):
        return self.clients[ident]

    def search_by_query (self, query):
        query = query.upper()
        results = []                                        # [[match_rating, {reference:Client()}]]
        
        for ident, client in self.clients.items():
            client_search = client.search_by_query(query)

            if client_search >= 0:                       # Check for Product().search_by_query()
                if len(results) > 0:                        # Order result by its rating
                    for r in results:
                        if client_search < r[0]:
                            results.insert(results.index(r), [client_search, client])
                            break
                        
                        elif results.index(r) == len(results)-1:
                            results.append(results.index(r), [client_search, client])
                            break
                else:
                    results.append([client_search, client])

        # [Client]
        results = [r[1] for r in results]                   
        
        return results

    def to_dict (self):
        client_list = []

        for ident, client in self.clients.items():
            client_dict = client.to_dict()
            client_dict["id"] = ident
            client_list.append(client_dict)

        return {"clients":client_list}

    def from_dict (self, client_list):
        for client in client_list:
            contacts = Contacts(client["contacts"]["adress"], client["contacts"]["mobile"],
                                client["contacts"]["nif"], client["contacts"]["email"])
            self.clients[client["id"]] = Client(client["name"], contacts)
            
