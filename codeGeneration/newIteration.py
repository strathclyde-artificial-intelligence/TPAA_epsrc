import random
import re
import sys
import time

node_conf1 = {
        "operation1": "{0} = {1} + {2}; [A]", 
        "operation2": "{0} = {1} * {2}; [A]", 
        "operation3": "{0} = {1} - {2}; [A]", 
        }

node_conf2 = {
        "condition1": "if {1} == {2}: {A} else: {B}", 
        "condition2": "if {1} >= {2}: {A} else {B}", 
        }

node_conf3 = {
        "operation_ret": "return {1}"
        }

node_conf4 = {
        "iterator1": "for i in {1}: [A]", 
        "iterator2": "while {1}: [A]"
        }

operations = {
        "operation1": "Get the total of {1} + {2}, store the result in {O}. [A]", 
        "operation2": "Get the product of {1} * {2}, store the result in {O}. [A]", 
        "operation3": "Get the total of {1} - {2}, store the result in {O}. [A]", 
        }

conditionals = {
        "condition1": "If {1} and {2} are equal: [A]. otherwise, [B]", 
        "condition2": "If {1} is greater than or equal to {2}: [A]. otherwise, [B]", 
        }

iterators = {
        "iterator2": "As long as {1}, [A].", 

        }
operation_ret = {
        "operation_ret1": "return {1}", 
        }

''' First, we set either an operation node or a condition node as the head node, which is the first operation to be performed.  -- Done

    Then, we attach either an operation node or a condition node to an available slot in the structure randomly. -- Done

    We continue attaching new nodes until the structure contains exactly c nodes. -- Done

    Finally, we attach return nodes to all the remaining slots. Figure 7 shows some generated structures of varying complexity.

'''


class ProgrammingGenerator:

    def __init__(self):
        self.graph = {}
        self.connection_slots = {}

    def start(self, complexity):
        choices = ["operation", "condition"]
        options = ["[A]", "[B]"]
        choice = random.choice(choices)
        random_slot = random.choice(options)
        statement = self.generate(choice)
        key = 0 
        key = self.assign_new_node(statement, key)
        for i in range(complexity):
            #we pick one random choice from the operations to change these with some statement
            random_slot = random.choice(options)
            random_one = random.choice(choices)
            random_key = random.choice(list(self.graph))
           
            #unpack the operations for each graph statement i.e., all [A], [B] with corresponding slot
            graph_value = self.graph.get(random_key)
            slots = list(self.connection_slots.get(random_key))
            
            #get a random integer within the range of the slots list, e.g., if there is 2 slots [A] or [B] can be taken
            if len(slots) == 1:
                index = 0
            else:
                #if there exists only one slots then there is not need to geneerate randint, as only possible spot for op is index 0
                index = random.randint(0, len(slots)) 

            if random_slot in slots and self.connection_slots.get(random_slot) == None:
                key = self.assign_new_node(self.generate(random_one), key)
                self.connection_slots[random_key][random_slot] = key
    

        ret_statement = list(operation_ret.items())


        #after we have assigned a bunch of random nodes to some free operation slow, we conclude by adding return statements to the last free slots
        slot_keys = self.connection_slots.keys()

        #we need to create new return nodes and add these as connections but since dict cannot be changed we keep a list of how many return nodes we need to add.
        #we initalise counter for amount of new nodes created and add key to corresponding statement
        count = 1 
        for index in slot_keys:
            if options[0] in self.connection_slots[index]:
                if self.connection_slots[index][options[0]] == None:
                    self.connection_slots[index][options[0]] = key+count
            if options[1] in self.connection_slots[index]:
                if self.connection_slots[index][options[1]] == None:
                    self.connection_slots[index][options[1]] = key+count
                    count+=1
        
        #creation of all nodes in graph 
        for i in range(count):
            key = self.assign_new_node(ret_statement[0][1], key)

        return self.graph, self.connection_slots 


    def assign_new_node(self, statement, key):
        key+=1
        if "[A]" and "[B]" in statement:
            self.graph[key] = {statement: key}
            self.connection_slots[key] = {"[A]": None, "[B]": None}
        elif "[A]" in statement:
            self.graph[key] = {statement: key}
            self.connection_slots[key] = {"[A]": None}
        else:
            self.graph[key] = {statement: key}
            self.connection_slots[key] = {"return" : "{1}"}
        return key

    '''
    We used the following algorithm in assigning node parameters. 

    First, we define the depth of a node N as the number of steps needed to reach node N from the start node.  -- this is just the key of each node in the graph

    Next, we define critical_nodes to be a list of critical nodes. We define a critical node as a node whose operation affects the outcome of the function. Initially, we add all return nodes and condition nodes to Clist. 

    Return nodes directly affect the return value of the function by their definition, while condition nodes affect which branch to take, thus affecting which return node will be reached.
    '''

    def node_parameters(self):

        operands = ["{1}", "{2}"]
        critical_nodes = []
        #a node is critical if its a conditional or if it is a return statement, we can look for length, if it is 2 then we add because conditionals are the only one with 2 statements
        slot_keys = self.connection_slots.keys()
        for index in slot_keys:
            if len(self.connection_slots[index]) == 2:
                critical_nodes.append(index)
            elif "return {1}" in self.connection_slots[index]:
                critical_nodes.append(index)

        #we have all critical_nodes in the list
        count = 1
        for i in range(len(slot_keys)):
            #For each operation node N, we create a unique variable Xi, assign it as the output variable of N, and then increment i. 
            if i+1 not in critical_nodes:
                choice = random.choice(operands)
                #change string with new x_var
                key_value = list(self.graph[i+1].items())
                new_statement = key_value[0][0].replace(choice, "x"+str(count))
                #we assign the same key number but with a new statement
                self.graph[i+1] = {i+1: {new_statement: i+1}}
                '''error from here -> self condition check not working as intended'''
                self.condition_check(count, i+1, critical_nodes)
                #increment the x_var so that next assignment will be different
                count+=1
    

    def condition_check(self, x_var, current_node_index, critical_nodes):
        random_node = random.choice(critical_nodes)
        key_value = list(self.graph[random_node].items())
        if "{1}" in key_value[0][0] or "{2}" in key_value[0][0]:
            #now we need to check that this node is reachable
            print(key_value[0][0])
            if self.is_reachable(current_node_index, random_node) == True:
                print('yes haha')
                pass
            else:
                sys.exit(9)
                pass


    def is_reachable(self, current_node_index, target_node_index):

        #incomplete
        print(f'here = {self.connection_slots[current_node_index]}')
        value = list(self.connection_slots[current_node_index].values())
        #if the next connection is the target node then we know that it is true
        if value[0] == target_node_index:
            return True
        else:
            #we have to traverse until we find a return node, which is the bottom of the stack
            while "return {1}" not in value:
                print(value)
                try:
                    value = list(self.connection_slots[value[0]].values())
                except:
                    print(self.connection_slots)
                    return "failed"
            print('OUT!!!')

    def generate(self, type_of_thing):
        if type_of_thing == "operation":
            entry_list = list(operations.items())
            random_entry = random.choice(entry_list)
            statement_str = random_entry[1]
            return statement_str
        elif type_of_thing == "condition":
            entry_list = list(conditionals.items())
            random_entry = random.choice(entry_list)
            statement_str = random_entry[1]
            return statement_str

generator = ProgrammingGenerator()
x, y = generator.start(3)
print(generator.node_parameters())

