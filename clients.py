# Only used for rating searches in Client.search_by_query
# It will be summed to the position of query in word
# in case it is not in the begginning so that result
# appears later - DOES NOT ENFORCE ANYTHING
NUM_WORDS_CLIENT_NAME = 5

class Client:
    def __init__ (self, name, nif, mobile):
        self.name = name
        self.nif = nif
        self.mobile = mobile

    def get_name (self):
        return self.name

    def get_nif (self):
        return self.nif

    def get_mobile (self):
        return self.mobile

    def search_by_query (self, query):
        if str(self.nif).startswith(query) or str(self.mobile).startswith(query):
            return 0
        
        name_words = self.name.upper().split()              # Every word in the client name
        name_query_pos = self.name.upper().find(query)      # Position of query in client name
        
        for word in name_words:                             # Check if any of the words in 
            if word.startswith(query):                      # client name starts with query
                return name_words.index(word)
            
        if name_query_pos > 0:                              # Check if query is in the middle
            return name_query_pos + NUM_WORDS_CLIENT_NAME  # of a word

        return -1

    def to_dict (self):
        return {"name": self.name, "nif":self.nif, "mobile":self.mobile}


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

    def new_client (self, name, nif, mobile):
        self.clients[self.next_id()] = Client(name, nif, mobile)

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
            self.clients[client["id"]] = Client(client["name"], client["nif"], client["mobile"])
            
