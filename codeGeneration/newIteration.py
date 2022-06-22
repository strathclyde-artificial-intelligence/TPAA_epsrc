import random
import re
import sys

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
        self.available_slots = {}

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
            slots = list(self.available_slots.get(random_key))
            
            #get a random integer within the range of the slots list, e.g., if there is 2 slots [A] or [B] can be taken
            if len(slots) == 1:
                index = 0
            else:
                #if there exists only one slots then there is not need to geneerate randint, as only possible spot for op is index 0
                index = random.randint(0, len(slots)) 

            if random_slot in slots and self.available_slots.get(random_slot) == None:
                key = self.assign_new_node(self.generate(random_one), key)
                self.available_slots[random_key][random_slot] = key

        ret_statement = list(operation_ret.items())
        print(ret_statement[0][1])

        #after we have assigned a bunch of random nodes to some free operation slow, we conclude by adding return statements to the last free slots
        slot_keys = self.available_slots.keys()
        for index in slot_keys:

            if "[A]" in self.available_slots[index]:
                if self.available_slots[index]["[A]"] == None:
                    self.available_slots[index]["[A]"] = ret_statement[0][1]
            if "[B]" in self.available_slots[index]:
                if self.available_slots[index]["[B]"] == None:
                    self.available_slots[index]["[B]"] = ret_statement[0][1]
        return self.graph, self.available_slots 


    def assign_new_node(self, statement, key):
        key+=1
        if "[A]" and "[B]" in statement:
            self.graph[key] = {statement: key}
            self.available_slots[key] = {"[A]": None, "[B]": None}
        else:
            self.graph[key] = {statement: key}
            self.available_slots[key] = {"[A]": None}
        return key

    '''
    We used the following algorithm in assigning node parameters. 

    First, we define the depth of a node N as the number of steps needed to reach node N from the start node.  -- how do we do this (try count the amount of dots from start)?

    Next, we define critical_nodes to be a list of critical nodes. We define a critical node as a node whose operation affects the outcome of the function. Initially, we add all return nodes and condition nodes to Clist. 

    Return nodes directly affect the return value of the function by their definition, while condition nodes affect which branch to take, thus affecting which return node will be reached.
    '''

    def node_parameters(self, statement):

        critical_nodes = []
        statements = statement.replace(".", "%replace").replace(":", "%replace").split("%replace")
        for i in range(len(statements)):
            if "If" in statements[i]:
                critical_nodes.append((i, statements[i]))
            elif "return" in statements[i]: 
                critical_nodes.append((i, statements[i]))

        statements = self.create_variables(statements, critical_nodes)
        return statements, len(statements) 

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

    '''
    Next, we set a counter variable i=1. We loop through the remaining operation nodes in descending depth. 
    For each operation node N, we create a unique variable Xi, assign it as the output variable of N, and then increment i. 
    Then, we select a random node C from Clist that satisfy the following conditions: C has at least one operand that is not yet defined and C is reachable from N. 
    If no nodes satisfy the above conditions, the generation is treated as a failure. Otherwise, the variable Xi is assigned as one of the operands of C. 
    Since C is a critical node and the output variable of N is now used as an operand of C, it follows that N is now a critical node as well, so we add it to Clist. 
    Randomly, the algorithm may repeat assigning Xi to more nodes from Clist, but only the first assignment is required. This process is repeated until all nodes are already in Clist.
    '''

    '''
    how do we do this???

        do x + y = z

        if x == 1:
            if y >= 2:
                x2 = x + 3
                return x2
            else:
                return x
        else:
            if x2 == 3: --- this is wrong
                x3 = x + 33
                return x3
    '''

    def is_reachable(self, rand_node, node_nr, statements, statement_index):

        tabs = 0 
        #does not quite work
        for stmnt in statements:
            if "If" in stmnt:
                print(tabs * ' '+stmnt)
                tabs+=2
            elif "otherwise" in stmnt:
                tabs-=2
                print(tabs * ' '+stmnt)
            elif "return" in stmnt:
                print(tabs * ' '+stmnt)
                tabs-=2

    def check_conditions(self, critical_nodes, statements, statement_index, rand_node, x_var):
        operands_choice = ["{1}", "{2}"]
        #C is reachable from  N -> how do we prove this condition
        number, node = rand_node 
        #this rule does not hold for all cases we need to check how the statements can reach each other
        if ("{1}" in node or "{2}" in node) and (statement_index < number):
            return node, node.replace(random.choice(operands_choice), x_var)
        else:
            for i in range(10):
                if ("{1}" in node or "{2}" in node) and (statement_index < number):
                    return node, node.replace(random.choice(operands_choice), x_var)
        return [], []

    def create_variables(self, statements, critical_nodes):
        cnt = 1
        for i in range(len(statements)):
            if "{O}" in statements[i]:
                x_var = "x" + str(cnt)
                statements[i] = statements[i].replace("{O}", x_var)
                random_entry = random.randint(0, len(statements) - 1)
                #more of algorithm with critical_nodes
                random_critical_node = random.choice(critical_nodes)
                node, new_node = self.check_conditions(critical_nodes, statements[i], i, random_critical_node, x_var)
                self.is_reachable(random_critical_node, random_entry, statements, i)
                if node == [] and new_node == []:
                    print("Failed")
                    sys.exit(1)
                for j in range(len(statements)):
                    if statements[j] == node:
                        statements[j] = new_node
                        critical_nodes.append((j, statements[j]))
                cnt+=1
        return statements

generator = ProgrammingGenerator()
print(generator.start(3))
#print(generator.node_parameters(generator.start(3)))

