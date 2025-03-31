from numpy import random
from distributed_event_factory.graph_builder.node import Node

class GraphBuilder:
    #ToDos: alle fixen parameter als eingaben hinzunehmen,temp_name_list mit einem name_provider ersetzen
    def __init__(self):
        self.probability_straight = 0.4
        self.probability_split = 0.3
        self.probability_join = 0.3
        self.max_length = -1
        self.max_var = 10
        self.total_var = 0
        self.active_children = []
        self.graph = {}
        self.temp_name_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","V","W","X","Y","Z",
                               'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1', 'S1', 'T1', 'V1', 'W1', 'X1', 'Y1', 'Z1',
                               'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2', 'Q2', 'R2', 'S2', 'T2', 'V2', 'W2', 'X2', 'Y2', 'Z2',
                               'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3', 'K3', 'L3', 'M3', 'N3', 'O3', 'P3', 'Q3', 'R3', 'S3', 'T3', 'V3', 'W3', 'X3', 'Y3', 'Z3',
                               "A4","B4","C4","D4","E4","F4","G4","H4","I4","J4","K4","L4","M4","N4","O4","P4","Q4","R4","S4","T4","V4","W4","X4","Y4","Z4",
                               "A5","B5","C5","D5","E5","F5","G5","H5","I5","J5","K5","L5","M5","N5","O5","P5","Q5","R5","S5","T5","V5","W5","X5","Y5","Z5",
                               "A6","B6","C6","D6","E6","F6","G6","H6","I6","J6","K6","L6","M6","N6","O6","P6","Q6","R6","S6","T6","V6","W6","X6","Y6","Z6",
                               "A7","B7","C7","D7","E7","F7","G7","H7","I7","J7","K7","L7","M7","N7","O7","P7","Q7","R7","S7","T7","V7","W7","X7","Y7","Z7",
                               "A8","B8","C8","D8","E8","F8","G8","H8","I8","J8","K8","L8","M8","N8","O8","P8","Q8","R8","S8","T8","V8","W8","X8","Y8","Z8",
                               "A9","B9","C9","D9","E9","F9","G9","H9","I9","J9","K9","L9","M9","N9","O9","P9","Q9","R9","S9","T9","V9","W9","X9","Y9","Z9"]
        self.end_nodes = []

    # requires the wanted amount of variations as int
    # returns tuple of (graph: {"name":Node}, number of variations: int})
    def build_graph_var(self, max_var):
        self.max_var = max_var
        self.max_length = -1
        self.graph["<start>"] = Node("<start>", 0, 1)
        possibilities = ["straight", "split", "join"]
        probabilities = [self.probability_straight, self.probability_split, self.probability_join]

        while self.total_var < self.max_var:
            self.active_children.append("<start>")
            self.total_var += 1
            while len(self.active_children) > 0:
                action = random.choice(possibilities, p=probabilities)
                match action:
                    case "straight":
                        self.straight()
                    case "split":
                        self.split()
                    case "join":
                        self.join()
                    case _:
                        print("Something went horribly wrong in the switch statement of the graph_builder")

        return self.graph, self.total_var

    #requires the wanted length as int
    # returns tuple of (graph: {"name":Node}, number of variations: int})
    def build_graph_length(self, max_length):
        self.max_length = max_length
        self.active_children.append("<start>")
        self.graph["<start>"] = Node("<start>", 0, 1)
        possibilities = ["straight", "split", "join"]
        probabilities = [self.probability_straight, self.probability_split, self.probability_join]
        # print("TEST1:" + self.graph.__str__())
        # print("TEST2:" + self.graph["start"].__str__())

        while len(self.active_children) > 0:
            action = random.choice(possibilities, p=probabilities)
            match action:
                case "straight":
                    self.straight()
                case "split":
                    self.split()
                case "join":
                    self.join()
                case _:
                    print("Something went horribly wrong in the switch statement of the graph_builder")


        all_variations = 0
        for end_node in self.end_nodes:
            all_variations += self.graph[end_node].get_variations()

        return self.graph, all_variations


    #for now only splitting in 2 branches
    def split (self):
        active_node = self.active_children.pop(0)

        #this case is worked on, if the length is restricted
        if self.max_length > -1:
            if self.graph[active_node].get_length() > self.max_length:
                print("Error: Graph too long")
            elif self.graph[active_node].get_length() == self.max_length:
                self.end_nodes.append(active_node)
            else:
                #in case of allowing more than 2 branches, just loop the spawn child the amount you want
                self.spawn_child([active_node])
                self.spawn_child([active_node])

        #this case is worked on, if the variations are restricted
        else:
            #in case of allowing more than 2 branches, just multiply the variations by the given number of branches
            if self.total_var + self.graph[active_node].get_variations() > self.max_var:
                self.end_nodes.append(active_node)
            else:
                self.spawn_child([active_node])
                self.spawn_child([active_node])
                self.total_var += self.graph[active_node].get_variations()



    #for now only joins up to 2 nodes, by creating a node they are joining in, if possible
    def join(self):
        #to change the amount of allowed joins, just take number of joins as parameter
        number_of_joins = 2
        active_nodes = []

        while len(active_nodes) < number_of_joins and len(self.active_children) > 0:
            active_nodes.append(self.active_children.pop(0))
            #executed in case of length
            if self.max_length > -1:
                if self.graph[active_nodes[len(active_nodes) - 1]].get_length() > self.max_length:
                    print("Error: Graph too long")
                elif self.graph[active_nodes[len(active_nodes) - 1]].get_length() == self.max_length:
                    self.end_nodes.append(active_nodes[len(active_nodes) - 1])
                    active_nodes.pop()



        if len(active_nodes) < number_of_joins:
            active_nodes.reverse()
            for temp_node in active_nodes:
                self.active_children = [temp_node] + self.active_children
        else:
            self.spawn_child(active_nodes)



    def straight(self):
        active_node = self.active_children.pop(0)

        #executed in case of length
        if self.max_length > -1:
            if self.graph[active_node].get_length() > self.max_length:
                print("Error: Graph too long")
            elif self.graph[active_node].get_length() == self.max_length:
                self.end_nodes.append(active_node)
            else:
                self.spawn_child([active_node])
        #executed in case of var
        else:
            self.spawn_child([active_node])

    # takes a list of parents and adds a child to them
    def spawn_child(self, parent_list):
        new_name = self.temp_name_list.pop(0)
        current_variations = 0
        current_length = 0

        #finding current length and number of variations in case of join
        for parent in parent_list:
            self.graph[parent].add_child(new_name)
            current_variations += self.graph[parent].get_variations()
            temp_length = self.graph[parent].get_length()
            if temp_length > current_length:
                current_length = temp_length

        self.graph[new_name] = Node(new_name, current_length + 1, current_variations)
        self.active_children.append(new_name)