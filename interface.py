class Interface:
    def update_behaviour (self, methods):
        self.behav = dict()

        for m in methods:
            self.behav[m(True).upper()] = m
        
    def run (self, methods):
        self.update_behaviour(methods)
        while True:
            command = input("> ").upper()
            if command in self.behav:
                self.behav[command]()
            elif command == "HELP":
                print("Valid Commands:")
                for c in self.behav.keys():
                    print("\t"+c)
            elif command == "QUIT":
                break
            else:
                print("Command was not recognized!")
