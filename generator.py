#!/usr/bin/env python
import random
from math import inf
import json 

node_op = {
        "operation1": "{O} = {1} + {2} [A]", 
        "operation2": "{O} = {1} * {2} [A]", 
        "operation3": "{O} = {1} - {2} [A]", 
        }

node_cond = {
        "condition1": "if {1} == {2}: [A]else: [B]", 
        "condition2": "if {1} >= {2}: [A]else: [B]", 
        "condition3": "if {1} <= {2}: [A]else: [B]", 
        "condition4": "if {1} < {2}: [A]else: [B]", 
        "condition5": "if {1} > {2}: [A]else: [B]", 
        }

node_ret = "return {1}"


operations = {
        "operation1": "Get the total of {1} + {2}, store the result in {O}.:[A]", 
        "operation2": "Get the product of {1} * {2}, store the result in {O}.:[A]", 
        "operation3": "Get the total of {1} - {2}, store the result in {O}.:[A]", 
        }

conditionals = {
        "condition1": "If {1} and {2} are equal:[A]:otherwise,:[B]", 
        "condition2": "If {1} is greater than or equal to {2}:[A]:otherwise,:[B]", 
        "condition3": "If {1} is less than or equal to {2}:[A]:otherwise,:[B]", 
        "condition4": "If {1} is less than {2}:[A]:otherwise,:[B]", 
        "condition5": "If {1} is greater than {2}:[A]:otherwise,:[B]", 
        }

operation_ret = {
        "operation_ret1": "return {1}", 
        }


class ProgrammingGenerator:
    def __init__(self):
        self.graph = {}
        self.statements = {}
        self.code = {}
        self.problem_object = {}
        self.statement_options = ["operation", "condition"]
        self.actions = ["A", "B"]
        self.action_slots = ["[A]", "[B]"]
        self.operands = ["{1}", "{2}"]
        self.output = "{O}"
        self.keywords = ["return {1}", "If", "Get", "otherwise"]
        self.code_keywords = ["if", "else", "return"]


    def start(self, complexity):
        balance_counter = 0
        random_option = random.choice(self.statement_options)
        if random_option == self.statement_options[1]:
            balance_counter+=1
        head_node, code_str, type_of_operation = self.generate(random_option)
        key = 1
        self.statements = {key: head_node}
        self.code = {key: code_str}

        if type_of_operation == "operation":
            self.graph = {key: ["A"]}
        else:
            self.graph = {key: ["A", "B"]}
        
        for i in range(complexity):
            #generate random condition or operation node
            random_option = random.choice(self.statement_options)
            if random_option == self.statement_options[1]:
                balance_counter+=1
            new_statement, code_str, type_of_operation = self.generate(random_option)
            key = self.attach_nodes(new_statement, code_str, key, type_of_operation)

        #if we have generated to many of conditional statements we treat the generation as a failure
        if balance_counter >= complexity:
            return False

        else:
            #Finally, we attach return nodes to all the remaining slots. return nodes are terminal and there fore lead to none
            for index in range(1, len(self.graph) + 1):
                if self.actions[0] in self.graph[index]:
                    key+=1
                    self.graph[index][0] = key
                    self.statements[key] = "return {1}"
                    self.code[key] = node_ret
                    self.graph[key] = [] 
                if self.actions[1] in self.graph[index]:
                    key+=1
                    self.graph[index][1] = key
                    self.statements[key] = "return {1}"
                    self.code[key] = node_ret
                    self.graph[key] = [] 

            if self.assign_node_parameters(complexity) == False:
                return False
            else:
                return json.dumps(self.problem_object)


    def assign_node_parameters(self, complexity):
        graph_list_keys = list(self.graph.keys())
        #We define a critical node as a node whose operation affects the outcome of the function. Initially, we add all return nodes and condition nodes to critical_nodes
        critical_nodes = set()

        #start by adding all the nodes which are critical to critical_nodes
        for index in graph_list_keys:
            if self.keywords[0] in self.statements[index] or self.keywords[1] in self.statements[index]:
                critical_nodes.add(index)

        #we have a counter i which we assign to x variables for each operand node
        x_var = "x"
        count = 1

        #this needs to be refactored into more functions, rather then being a huge cluster....
        for index in graph_list_keys:
            if index not in critical_nodes:
                statement = self.statements[index]
                code_str = self.code[index]
                new_statement = statement.replace(self.output, x_var+str(count))
                new_code = code_str.replace(self.output, x_var+str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code

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
                    code_str = self.code[node]
                    self.update_statements(node, statement, code_str, operand_to_replace, x_var, count)
                else:
                    #we check if there is more then 1 node that is following, and if this nodes is an operation node if this is the case then we assign one of the variables to this
                    next_node = (list(visited)[1])
                    statement = self.statements[next_node]
                    code_str = self.code[next_node]

                    if self.keywords[2] in statement:
                        operand_to_replace = random.choice(self.operands)
                        self.update_statements(next_node, statement, code_str, operand_to_replace, x_var, count)
                    #if the following statements is a return statement then we can return the variable we just stored
                    elif self.keywords[0] in statement:
                        new_statement = statement.replace(self.operands[0], x_var +str(count))
                        new_code = code_str.replace(self.operands[0], x_var + str(count))
                        self.statements[next_node] = new_statement
                        self.code[next_node] = new_code
                count+=1
            else:
                #we check if it is a conditional statement, if it is we add a random number to one of the operands
                if self.keywords[1] in self.statements[index]:
                    rand_number = str(random.randint(0,100))
                    operand_to_replace = random.choice(self.operands)
                    statement = self.statements[index]
                    code_str = self.code[index]

                    if operand_to_replace in statement:
                        new_statement = statement.replace(operand_to_replace, rand_number)
                        new_code = code_str.replace(operand_to_replace, rand_number)
                    elif operand_to_replace == self.operands[0]:
                        new_statement = statement.replace(self.operands[1], rand_number)
                        new_code = code_str.replace(self.operands[1], rand_number)
                    elif operand_to_replace == self.operands[1]:
                        new_statement = statement.replace(self.operands[0], rand_number)
                        new_code = code_str.replace(self.operands[0], rand_number)
                    self.statements[index] = new_statement
                    self.code[index] = new_code

        #get the statements that have 2 wholes to fill up and assign at least one random int to these, no matter if it is a critical node or not
        check = self.add_function_input(complexity)
        if check == False:
            return False
        self.fill_remaining()
        self.build_statements()
        problem_statement, solution_code = self.indent_code()
        self.build_problem(complexity, problem_statement, solution_code)


    def update_statements(self, index, statement, code_str, operand_to_replace, x_var, count):
        if self.operands[0] in statement or self.operands[1] in statement:
            if operand_to_replace in statement:
                new_statement = statement.replace(operand_to_replace, x_var +str(count))
                new_code = code_str.replace(operand_to_replace, x_var + str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code
            #if the other slot was the random one then we assign this to the 
            elif operand_to_replace == self.operands[0]:
                new_statement = statement.replace(self.operands[1], x_var +str(count))
                new_code = code_str.replace(self.operands[1], x_var + str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code
            #if we the other slot is the free one
            elif operand_to_replace == self.operands[1]:
                new_statement = statement.replace(self.operands[0], x_var +str(count))
                new_code = code_str.replace(self.operands[0], x_var + str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code

    #this function adds input parameters into the statement
    def add_function_input(self, complexity):
        y_var = "y"
        #we create the number of input nodes, we do this by creating complexity - 1 input nodes, 
        inputs_to_add = []
        for i in range(1, complexity):
            inputs_to_add.append(y_var+str(i))

        graph_list_keys = list(self.graph.keys()) #we pick any random node from the graph and check if it has some free slot of any sort random_node = random.choice(graph_list_keys)
        operand_to_replace = random.choice(self.operands)

        max_tries = 0
        count = 0

        while count < len(inputs_to_add):
            #run time check
            if max_tries == 100:
                return False
            random_node = random.choice(graph_list_keys)
            operand_to_replace = random.choice(self.operands)
            if operand_to_replace in self.statements[random_node]:
                new_statement = self.statements[random_node].replace(operand_to_replace, inputs_to_add[count])
                new_code = self.code[random_node].replace(operand_to_replace, inputs_to_add[count])
                self.statements[random_node] = new_statement
                self.code[random_node] = new_code
                count+=1
            max_tries+=1
            

    def fill_remaining(self):
        graph_list_keys = list(self.graph.keys())

        #for all the statements in the graph, we add random numbers to all available slots
        for index in graph_list_keys:
            if self.operands[0] in self.statements[index]:
                rand_number = str(random.randint(0, 100))
                new_statement = self.statements[index].replace(self.operands[0], rand_number)
                new_code = self.code[index].replace(self.operands[0], rand_number)
                self.statements[index] = new_statement
                self.code[index] = new_code
            if self.operands[1] in self.statements[index]:
                rand_number = str(random.randint(0, 100))
                new_statement = self.statements[index].replace(self.operands[1], rand_number)
                new_code = self.code[index].replace(self.operands[1], rand_number)
                self.statements[index] = new_statement
                self.code[index] = new_code

    
    def dfs(self, visited, node):  #function for dfs 
        if node not in visited:
            if node not in visited:
                visited.add(node)
            for neighbour in self.graph[node]:
                self.dfs(visited, neighbour)
        return visited
    

    def create_node(self, new_statement, code_str, type_of_operation, key):
        key+=1
        self.statements[key] = new_statement
        self.code[key] = code_str
        if type_of_operation == "operation":
            self.graph[key] = ["A"]
        else:
            self.graph[key] = ["A", "B"]
        return key


    def attach_nodes(self, new_statement, code_str, key, type_of_operation):
        random_key = random.choice(list(self.graph.keys()))
        new_list = self.graph[random_key]
        slot = random.choice(new_list)

        if slot in self.actions:
            #create new statement
            key = self.create_node(new_statement, code_str, type_of_operation, key)
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
            code_str = node_op[random_entry[0]]
            return statement_str, code_str, type_of_operation

        elif type_of_operation == "condition":
            entry_list = list(conditionals.items())
            random_entry = random.choice(entry_list)
            statement_str = random_entry[1]
            code_str = node_cond[random_entry[0]]
            return statement_str, code_str, type_of_operation
    

    def build_statements(self):
        #think about how to create this build statement in a good way. Will be needed for code generation as well.
        graph_list_keys = list(self.graph.keys())

        for node in graph_list_keys:
            node_numbers = self.graph[node]
            statement = self.statements[node]
            code_str = self.code[node]
            if node_numbers == []:
                break
            elif len(node_numbers) == 2:
                #we add replace each action with its corresponding key in the statements slot
                statement = self.statements[node]
                code_str = self.code[node]
                first_key = str(node_numbers[0])
                second_key = str(node_numbers[1])
                self.statements[node] = statement.replace(self.action_slots[0], f"{ {first_key} }").replace(self.action_slots[1], f"{ {second_key} }")
                self.code[node] = code_str.replace(self.action_slots[0], f"{ {first_key} }").replace(self.action_slots[1], f"{ {second_key} }")
            else:
                first_key = str(node_numbers[0])
                self.statements[node] = statement.replace(self.action_slots[0], f"{ {first_key} }")
                self.code[node] = code_str.replace(self.action_slots[0], f"{ {first_key} }")


        for node in graph_list_keys:
            for i in range(1, len(graph_list_keys) + 1):
                current = f"{ {str(i)} }"
                if current in self.statements[node]:
                    self.statements[node] = self.statements[node].replace(current, self.statements[i])
                    self.code[node] = self.code[node].replace(current, '\n' + self.code[i] + '\n')

    def build_problem(self, complexity, problem_statement, solution_code):
        #self.problem_object["code"] = solution_code 
        y_var = "y"

        number_of_tests = 3
        test_cases = []
        input_parameters = []

        for j in range(complexity - 1):
            rand_num = random.randint(1,100)
            input_parameters.append(rand_num)

        input_var = ""
        for i in range(1, complexity):
            if i == complexity - 1:
                input_var += y_var+str(i)
            else:
                input_var += y_var+str(i)+", "


        test_variables = ""

        for i in range(len(input_parameters)):
            if i == len(input_parameters) - 1:
                test_variables += str(input_parameters[i]) 
            else:
                test_variables += str(input_parameters[i]) + ", "

        function_str = f"def problem({input_var}):"
        run_str = f"print(problem({test_variables}))"

        self.problem_object["statement"] = problem_statement
        self.problem_object["code"] = function_str 
        self.problem_object["testCase"] = function_str + solution_code
        self.problem_object["testCaseStr"] = run_str
        self.problem_object["solution"] = function_str + solution_code


    def indent_code(self):
        #how is this done in a good way?
        new_list = self.code[1].split('\n')
        output_statements = self.statements[1].split(':')

        final_list = []
        #we have to remove empty spaces from list
        for node in new_list:
            if '' != node:
                final_list.append(node)

        stack = []
        solution_code = ""
        problem_statement = ""

        stack.append(-1)
        #this does work for all cases, but its not a pretty solution, based on return always ending each code segment
        for node in final_list:
            if self.code_keywords[0] in node:
                solution_code += '\n' + len(stack)*'\t' + node
                stack.append(0)
            elif self.code_keywords[1] in node:
                solution_code += '\n' + len(stack)*'\t' + node
                stack.append(1)
            elif self.code_keywords[2] in node:
                solution_code += '\n' + len(stack)*'\t' + node
                if len(stack) > 0:
                    popped = -inf
                    while popped != 0 and len(stack) > 1:
                        popped = stack.pop()
            else:
                solution_code += '\n' + len(stack)*'\t' + node

        for node in output_statements:
            if self.keywords[1] in node:
                problem_statement += '\n' + len(stack)*'  ' + node
                stack.append(0)
            elif self.keywords[3] in node:
                problem_statement += '\n' + len(stack)*'  ' + node
                stack.append(1)
            #we can use code keywords, because return is the same in both
            elif self.code_keywords[2] in node:
                problem_statement += '\n' + len(stack)*'  ' + node
                if len(stack) > 0:
                    popped = -inf
                    while popped != 0 and len(stack) > 1:
                        popped = stack.pop()
            else:
                problem_statement += '\n' + len(stack)*'  ' + node
        return problem_statement, solution_code
        


generator = ProgrammingGenerator()
print(generator.start(3))