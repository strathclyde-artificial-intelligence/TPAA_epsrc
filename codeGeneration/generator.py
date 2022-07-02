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


class ProgrammingGenerator:
    def __init__(self):
        self.graph = {}
        self.statements = {}
        self.statement_options = ["operation", "condition"]
        self.actions = ["A", "B"]
        self.operands = ["{1}", "{2}"]
        self.output = "{O}"
        self.keywords = ["return {1}", "If", "Get"]


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

        self.assign_node_parameters(complexity)
        return self.statements[1]


    def assign_node_parameters(self, complexity):
        graph_list_keys = list(self.graph.keys())
        #We define a critical node as a node whose operation affects the outcome of the function. Initially, we add all return nodes and condition nodes to critical_nodes
        critical_nodes = set()

        #start by adding all the nodes which are critical to critical_nodes
        for index in graph_list_keys:
            if self.keywords[0] in self.statements[index] or self.keywords[1] in self.statements[index]:
                critical_nodes.add(index)

        x_var = "x"
        count = 1
        stack = []

        #this needs to be refactored into more functions, rather then being a huge cluster....
        for index in graph_list_keys:
            if index not in critical_nodes:
                statement = self.statements[index]
                new_statement = statement.replace(self.output, x_var+str(count))
                self.statements[index] = new_statement
                stack.append(x_var+str(count))

                visited = set()
                #get the path that the index is traversing
                visited = self.dfs(visited, index)

                #we loop through all of the visited node from index, then we check for all conditional statements that follows node
                list_of_statements = []
                for node in visited:
                    if node in critical_nodes and self.keywords[1] in self.statements[node]:
                        list_of_statements.append(node)

                #if there follows more then 0 If nodes from index, then we pick a random one and assign X_num to one of its operands
                if len(list_of_statements) > 0:
                    node = random.choice(list_of_statements)
                    operand_to_replace = random.choice(self.operands)
                    statement = self.statements[node]
                    if self.operands[0] in self.statements[index] and self.operands[1] in self.statements[index]:
                        if operand_to_replace in statement:
                            new_statement = statement.replace(self.operands[0], x_var +str(count))
                            self.statements[node] = new_statement
                        #if we the other slot is the free one
                        elif operand_to_replace == self.operands[0]:
                            new_statement = statement.replace(self.operands[0], x_var +str(count))
                            self.statements[node] = new_statement
                        #if we the other slot is the free one
                        elif operand_to_replace == self.operands[1]:
                            new_statement = statement.replace(self.operands[1], x_var +str(count))
                            self.statements[node] = new_statement
                else:
                    #we check if there is more then 1 node that is folling, and if this nodes is an operation node if this is the case then we assign one of the variables to this
                    next_node = (list(visited)[1])
                    if self.keywords[2] in self.statements[next_node]:
                        operand_to_replace = random.choice(self.operands)
                        statement = self.statements[next_node]
                        if self.operands[0] in self.statements[next_node] and self.operands[1] in self.statements[next_node]:
                            if operand_to_replace in statement:
                                new_statement = statement.replace(self.operands[0], x_var +str(count))
                                self.statements[next_node] = new_statement
                            #if the other slot was the random one then we assign this to the 
                            elif operand_to_replace == self.operands[0]:
                                new_statement = statement.replace(self.operands[0], x_var +str(count))
                                self.statements[next_node] = new_statement
                            #if we the other slot is the free one
                            elif operand_to_replace == self.operands[1]:
                                new_statement = statement.replace(self.operands[1], x_var +str(count))
                                self.statements[next_node] = new_statement
                    #if the following statements is a return statement then we can return the variable we just stored
                    elif self.keywords[0] in self.statements[next_node]:
                        statement = self.statements[next_node]
                        new_statement = statement.replace(self.operands[0], x_var +str(count))
                        self.statements[next_node] = new_statement
                count+=1
            else:
                #we check if it is a conditional statement, if it is we add a random number to one of the operands
                if self.keywords[1] in self.statements[index]:
                    rand_number = random.randint(0,100)
                    operand_to_replace = random.choice(self.operands)
                    statement = self.statements[index]
                    if self.operands[0] in self.statements[index] and self.operands[1] in self.statements[index]:
                        if operand_to_replace in statement:
                            new_statement = statement.replace(operand_to_replace, str(rand_number))
                            self.statements[index] = new_statement
                        #if we the other slot is the free one
                        elif operand_to_replace == self.operands[0]:
                            new_statement = statement.replace(self.operands[1], str(rand_number))
                            self.statements[index] = new_statement
                        #if we the other slot is the free one
                        elif operand_to_replace == self.operands[1]:
                            new_statement = statement.replace(self.operands[0], str(rand_number))
                            self.statements[index] = new_statement


        #get the statements that have 2 wholes to fill up and assign at least one random int to these, no matter if it is a critical node or not

        self.add_function_input(complexity)
        self.fill_remaining()
        self.build_statements()
        print(self.graph)


    #this function adds input parameters into the statement
    def add_function_input(self, complexity):
        y_var = "y"
        #we create the number of input nodes, we do this by creating complexity - 1 input nodes, 
        inputs_to_add = []
        for i in range(1, complexity):
            inputs_to_add.append(y_var+str(i))

        graph_list_keys = list(self.graph.keys())
        #we pick any random node from the graph and check if it has some free slot of any sort
        random_node = random.choice(graph_list_keys)
        operand_to_replace = random.choice(self.operands)

        max_tries = 100
        count = 0

        while count < len(inputs_to_add):
            random_node = random.choice(graph_list_keys)
            operand_to_replace = random.choice(self.operands)
            if operand_to_replace in self.statements[random_node]:
                new_statement = self.statements[random_node].replace(operand_to_replace, inputs_to_add[count])
                self.statements[random_node] = new_statement
                count+=1
            

    def fill_remaining(self):
        graph_list_keys = list(self.graph.keys())

        #for all the statements in the graph, we add random numbers to all available slots
        for index in graph_list_keys:
            if self.operands[0] in self.statements[index]:
                rand_number = str(random.randint(0, 100))
                new_statement = self.statements[index].replace(self.operands[0], rand_number)
                self.statements[index] = new_statement
            if self.operands[1] in self.statements[index]:
                rand_number = str(random.randint(0, 100))
                new_statement = self.statements[index].replace(self.operands[1], rand_number)
                self.statements[index] = new_statement

    
    def dfs(self, visited, node):  #function for dfs 
        if node not in visited:
            visited.add(node)
            if self.graph[node] == None:
                return visited
            else:
                for neighbour in self.graph[node]:
                    self.dfs(visited, neighbour)
        return visited
    

    def bfs(self, visited, node): 
        queue = []
        visited.append(node)
        queue.append(node)
        while queue:
            m = queue.pop(0) 
            if self.graph[m] == None:
                return visited
            for neighbour in self.graph[m]:
                if neighbour not in visited:
                    visited.append(neighbour)
                    queue.append(neighbour)
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
                max_tries = 10
                #we can only assign the new node to a node that has come before it, therefore, we can only assign when condition random_key < key is true
                for i in range(max_tries):
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
    

    def build_statements(self):
        #think about how to create this build statement in a good way. Will be needed for code generation as well.
        graph_list_keys = list(self.graph.keys())

        for node in graph_list_keys:
            node_numbers = self.graph[node]
            if node_numbers == None:
                break
            elif len(node_numbers) == 2:
                self.statements[node] = self.statements[node].replace("[A]", "{" + str(node_numbers[0]) + "}").replace("[B]", "{" + str(node_numbers[1]) + "}")
            else:
                self.statements[node] = self.statements[node].replace("[A]", "{" + str(node_numbers[0]) + "}")

            
        for node in graph_list_keys:
            for i in range(1, len(graph_list_keys)+1):
                current = "{" + str(i) + "}"
                if current in self.statements[node]:
                    self.statements[node] = self.statements[node].replace(current, self.statements[i])



generator = ProgrammingGenerator()
print(generator.start(3))
