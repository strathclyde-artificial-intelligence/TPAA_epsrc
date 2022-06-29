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

''' First, we set either an operation node or a condition node as the head node, which is the first operation to be performed

    Then, we attach either an operation node or a condition node to an available slot in the structure randomly.

    We continue attaching new nodes until the structure contains exactly c nodes.

    Finally, we attach return nodes to all the remaining slots. Figure 7 shows some generated structures of varying complexity.

'''

'''
    graph.statement
    graph.connections = A -> key, B -> key

'''

class ProgrammingGenerator:
    def __init__(self):
        self.graph = {}
        self.statements = {}
        self.statement_options = ["operation", "condition"]
        self.actions = ["A", "B"]
        self.operands = ["{1}", "{2}"]
        self.output = "{O}"


    def start(self, complexity):
        random_option = random.choice(self.statement_options)
        head_node, type_of_operation = self.generate(random_option)
        key = 1
        self.statements = {key: head_node}
        if type_of_operation == "operation":
            self.graph = {key: ["A"]}
        else:
            self.graph = {key: ["A", "B"]}

        for i in range(complexity):
            #generate random condition or operation node
            random_option = random.choice(self.statement_options)
            new_statement, type_of_operation = self.generate(random_option)
            key = self.attach_nodes(new_statement, key, type_of_operation)


        #Finally, we attach return nodes to all the remaining slots. return nodes are terminal and there fore lead to none
        for index in range(1, len(self.graph) + 1):
            if self.actions[0] in self.graph[index]:
                key+=1
                self.graph[index][0] = key
                self.statements[key] = "return {1}"
                self.graph[key] = None
            if self.actions[1] in self.graph[index]:
                key+=1
                self.graph[index][1] = key
                self.statements[key] = "return {1}"
                self.graph[key] = None

        self.assign_node_parameters()


    def assign_node_parameters(self):
        graph_list_keys = list(self.graph.keys())
        #We define a critical node as a node whose operation affects the outcome of the function. Initially, we add all return nodes and condition nodes to critical_nodes
        critical_nodes = []

        #start by adding all the nodes which are critical to critical_nodes
        for index in graph_list_keys:
            if "return {1}" in self.statements[index] or "If" in self.statements[index]:
                critical_nodes.append(index)

        x_var = "x"
        count = 1

        stack = []
        #might have to change how the loop works just now
        for index in graph_list_keys:
            if index not in critical_nodes:
                statement = self.statements[index]
                operand_to_replace = random.choice(self.operands)
                new_statement = statement.replace(self.output, x_var+str(count))
                self.statements[index] = new_statement

                random_node = random.choice(critical_nodes)

                if self.operands[0] in self.statements[random_node] or self.operands[1] in self.statements[random_node]:
                    visited = set()
                    #here we check if it is reachable
                    visited = self.dfs(visited, index)
                    if random_node in visited:
                        statement = self.statements[random_node]
                        operand_to_replace = random.choice(self.operands)
                        if operand_to_replace in statement:
                            new_statement = statement.replace(operand_to_replace, x_var+str(count))
                            self.statements[random_node] = new_statement
                        #if we the other slot is the free one
                        elif operand_to_replace == self.operands[0]:
                            new_statement = statement.replace(self.operands[1], x_var+str(count))
                            self.statements[random_node] = new_statement
                        #if we the other slot is the free one
                        elif operand_to_replace == self.operands[1]:
                            new_statement = statement.replace(self.operands[0], x_var+str(count))
                            self.statements[random_node] = new_statement

    
    def dfs(self, visited, node):  #function for dfs 
        if node not in visited:
            visited.add(node)
            if self.graph[node] == None:
                return visited
            else:
                for neighbour in self.graph[node]:
                    self.dfs(visited, neighbour)
        return visited





    def create_node(self, new_statement, type_of_operation, key):
        key+=1
        self.statements[key] = new_statement
        if type_of_operation == "operation":
            self.graph[key] = ["A"]
        else:
            self.graph[key] = ["A", "B"]
        return key


    def attach_nodes(self, new_statement, key, type_of_operation):
        random_key = random.choice(list(self.graph.keys()))
        new_list = self.graph[random_key]
        slot = random.choice(new_list)

        if slot in self.actions:
            #create new statement
            key = self.create_node(new_statement, type_of_operation, key)
            #replace the current index with the key of the next node
            if random_key < key:
                new_list[new_list.index(slot)] = key
                self.graph[random_key] = new_list 
            else:
                #we can only assign the new node to a node that has come before it, therefore, we can only assign when condition random_key < key is true
                for i in range(10):
                    random_key = random.choice(list(self.graph.keys()))
                    if random_key < key and slot in self.actions:
                        new_list[new_list.index(slot)] = key
                        self.graph[random_key] = new_list 
                        return key

                return False

        return key


    def generate(self, type_of_operation):
        if type_of_operation == "operation":
            entry_list = list(operations.items())
            random_entry = random.choice(entry_list)
            statement_str = random_entry[1]
            return statement_str, type_of_operation

        elif type_of_operation == "condition":
            entry_list = list(conditionals.items())
            random_entry = random.choice(entry_list)
            statement_str = random_entry[1]
            return statement_str, type_of_operation



generator = ProgrammingGenerator()
generator.start(3)
