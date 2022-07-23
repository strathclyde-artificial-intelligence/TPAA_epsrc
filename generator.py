#!/usr/bin/env python
import random
from math import inf
import json 
import sys
import time
import iteration_generator
import cond_generator
import operation_generator


node_ret = "return {1}"

class ProgrammingGenerator:
    def __init__(self):
        self.graph = {}
        self.statements = {}
        self.code = {}
        self.problem_object = {}
        self.starter_options = ["operation", "condition"]
        self.statement_options = ["operation", "condition", "iterator"]
        self.actions = ["A", "B"]
        self.action_slots = ["[A]", "[B]"]
        self.operands = ["{1}", "{2}"]
        self.output = "{O}"
        self.keywords = ["return {1}", "If", "Get", "otherwise"]
        self.code_keywords = ["if", "else", "return", "for", "%end"]
        self.input_lists = []
        self.list_variables = []
        self.generated_nodes = 0
        self.created_nodes = 0


    def start(self, complexity):
        """
        Driver of the program initalises the first head node 

        Parameters:
        complexity (int): a number representing the difficulty of the problem

        Returns:
        (bool): False if failed
        problem_object (str): a dict with the problem statement, code, solution in json format
        """
        balance_counter = 0
        random_option = random.choice(self.starter_options)
        if random_option == self.statement_options[1]:
            balance_counter+=1
        head_node, code_str, type_of_operation = self.generate(random_option)
        key = 1
        self.statements[key] = head_node
        self.code[key] = code_str

        if type_of_operation == self.statement_options[0]:
            self.graph = {key : [self.actions[0]]}
        elif type_of_operation == self.statement_options[1]:
            self.graph = {key: [self.actions[0], self.actions[1]]}

        
        if self.create_base_nodes(key, complexity, balance_counter) == False:
            return False
        else:
            if self.assign_node_parameters(complexity) == False:
                return False
            return json.dumps(self.problem_object)


    def create_base_nodes(self, key, complexity, balance_counter):
        """
        Creates the defined amount of base nodes and craetes remaining return nodes

        Parameters:
        key (int): the key for the graph and the statements and code dict
        complexity (int): the amount of base nodes to create
        balance_counter (int): a check to make sure that the statements are balanced

        Returns:
        (bool): False if generation fails
        """
        for i in range(1, complexity):
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
            self.created_nodes+=1
            #Finally, we attach return nodes to all the remaining slots. return nodes are terminal and there fore lead to none
            for index in range(1, len(self.graph) + 1):
                if self.actions[0] in self.graph[index]:
                    key+=1
                    self.graph[index][0] = key
                    self.statements[key] = self.keywords[0]
                    self.code[key] = node_ret
                    self.graph[key] = [] 
                if self.actions[1] in self.graph[index]:
                    key+=1
                    self.graph[index][1] = key
                    self.statements[key] = self.keywords[0]
                    self.code[key] = node_ret
                    self.graph[key] = [] 

    def assign_node_parameters(self, complexity):
        graph_list_keys = list(self.graph.keys())
        #We define a critical node as a node whose operation affects the outcome of the function. Initially, we add all return nodes and condition nodes to critical_nodes
        critical_nodes = set()

        #start by adding all the nodes which are critical to critical_nodes
        for index in graph_list_keys:
            if self.keywords[0] in self.statements[index] or self.keywords[1] in self.statements[index]:
                critical_nodes.add(index)

        #we have a counter i which we assign to x variables for each operand node
        y_var = "y"
        x_var = "x"
        count = 1
        x_que = []
        x_que
        for i in range(1, complexity):
            x_que.append(x_var + str(i))

        #this needs to be refactored into more functions, rather then being a huge cluster....
        for index in graph_list_keys:
            if index not in critical_nodes:
                statement = self.statements[index]
                code_str = self.code[index]
                new_statement = statement.replace(self.output, y_var+str(count))
                new_code = code_str.replace(self.output, y_var+str(count))
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

                count = self.assign_yvar_predecessor(y_var, count, list_of_statements, visited)
            #we check if it is a conditional statement, if it is we add a random number to one of the operands
            elif self.keywords[1] in self.statements[index]:
                operand_to_replace = random.choice(self.operands)
                statement = self.statements[index]
                code_str = self.code[index]
                if operand_to_replace in statement:
                    rand_number = x_que.pop(0) 
                    new_statement = statement.replace(operand_to_replace, rand_number)
                    new_code = code_str.replace(operand_to_replace, rand_number)
                    self.statements[index] = new_statement
                    self.code[index] = new_code
                elif operand_to_replace == self.operands[0] and self.operands[1] in statement:
                    rand_number = x_que.pop(0) 
                    new_statement = statement.replace(self.operands[1], rand_number)
                    new_code = code_str.replace(self.operands[1], rand_number)
                    self.statements[index] = new_statement
                    self.code[index] = new_code
                elif operand_to_replace == self.operands[1] and self.operands[0] in statement:
                    rand_number = x_que.pop(0) 
                    new_statement = statement.replace(self.operands[0], rand_number)
                    new_code = code_str.replace(self.operands[0], rand_number)
                    self.statements[index] = new_statement
                    self.code[index] = new_code

        #get the statements that have 2 wholes to fill up and assign at least one random int to these, no matter if it is a critical node or not
        check = self.add_function_input(complexity, x_que)
        if check == False:
            return False
        self.fill_remaining()
        self.build_statements()
        problem_statement, solution_code = self.indent_code()
        self.build_problem(complexity, problem_statement, solution_code)
    
    def assign_yvar_predecessor(self, y_var, count, list_of_statements, visited):
        """
        Assigns the Yi variable to an appropriate predecessors of the current node

        Parameters:
        y_var (str): 'y' letter
        count (int): an int i which is combined with y_var
        list_of_statements (list): list of int with the keys that are predecessors to current node
        visited (list): list of int with the reachable nodes from current node

        Returns:
        count (int): an int i which is combined with y_var
        """
        #if there follows more then 0 If nodes from index, then we pick a random one and assign y_num to one of its operands
        if len(list_of_statements) > 0:
            node = random.choice(list_of_statements)
            operand_to_replace = random.choice(self.operands)
            statement = self.statements[node]
            code_str = self.code[node]
            self.update_statements(node, statement, code_str, operand_to_replace, y_var, count)
        else:
            #we check if there is more then 1 node that is following, and if this nodes is an operation node if this is the case then we assign one of the variables to this
            next_node = (list(visited)[1])
            statement = self.statements[next_node]
            code_str = self.code[next_node]

            if self.keywords[2] in statement:
                operand_to_replace = random.choice(self.operands)
                self.update_statements(next_node, statement, code_str, operand_to_replace, y_var, count)
            #if the followig statements is a return statement then we can return the variable we just stored
            elif self.keywords[0] in statement:
                new_statement = statement.replace(self.operands[0], y_var +str(count))
                new_code = code_str.replace(self.operands[0], y_var + str(count))
                self.statements[next_node] = new_statement
                self.code[next_node] = new_code
        count+=1
        return count


    def update_statements(self, index, statement, code_str, operand_to_replace, y_var, count):
        if self.operands[0] in statement or self.operands[1] in statement:
            if operand_to_replace in statement:
                new_statement = statement.replace(operand_to_replace, y_var +str(count))
                new_code = code_str.replace(operand_to_replace, y_var + str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code
            #if the other slot was the random one then we assign this to the 
            elif operand_to_replace == self.operands[0]:
                new_statement = statement.replace(self.operands[1], y_var +str(count))
                new_code = code_str.replace(self.operands[1], y_var + str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code
            #if we the other slot is the free one
            elif operand_to_replace == self.operands[1]:
                new_statement = statement.replace(self.operands[0], y_var +str(count))
                new_code = code_str.replace(self.operands[0], y_var + str(count))
                self.statements[index] = new_statement
                self.code[index] = new_code

    #this function adds input parameters into the statement
    def add_function_input(self, complexity, x_que):
        x_var = "x"
        #we create the number of input nodes, we do this by creating complexity - 1 input nodes, 
        inputs_to_add = []
        for i in range(1, complexity):
            inputs_to_add.append(x_var+str(i))

        graph_list_keys = list(self.graph.keys()) #we pick any random node from the graph and check if it has some free slot of any sort random_node = random.choice(graph_list_keys)
        operand_to_replace = random.choice(self.operands)

        max_tries = 0
        count = 0

        while count <= len(x_que) and len(x_que) != 0:
            #run time check
            if max_tries == 100:
                return False
            random_node = random.choice(graph_list_keys)
            operand_to_replace = random.choice(self.operands)
            if operand_to_replace in self.statements[random_node]:
                inputs_to_add = x_que.pop(0)
                new_statement = self.statements[random_node].replace(operand_to_replace, inputs_to_add)
                new_code = self.code[random_node].replace(operand_to_replace, inputs_to_add)
                self.statements[random_node] = new_statement
                self.code[random_node] = new_code
                count+=1
            max_tries+=1
            
    def fill_remaining(self):
        graph_list_keys = list(self.graph.keys())

        #for all the statements in the graph, we add random numbers to all available slots
        for index in graph_list_keys:
            if self.operands[0] in self.statements[index]:
                rand_number = str(random.randint(1, 100))
                new_statement = self.statements[index].replace(self.operands[0], rand_number)
                new_code = self.code[index].replace(self.operands[0], rand_number)
                self.statements[index] = new_statement
                self.code[index] = new_code
            if self.operands[1] in self.statements[index]:
                rand_number = str(random.randint(1, 100))
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
        if type_of_operation == self.statement_options[0]:
            self.graph[key] = ["A"]
        elif type_of_operation == self.statement_options[1]:
            self.graph[key] = ["A", "B"]
        elif type_of_operation == self.statement_options[2]:
            self.graph[key] = ["A"]
        self.created_nodes+=1
        return key


    def attach_nodes(self, new_statement, code_str, key, type_of_operation):
        random_key = random.choice(list(self.graph.keys()))
        new_list = self.graph[random_key]
        slot = random.choice(new_list)

        key = self.create_node(new_statement, code_str, type_of_operation, key)
        if slot in self.actions and random_key < key:
                new_list[new_list.index(slot)] = key
                self.graph[random_key] = new_list 
                return key
        else:
            all_keys = list(self.graph.keys())
            for current_key in all_keys:
                if current_key < key and self.actions[0] in self.graph[current_key]:
                    self.graph[current_key][0] = key
                    return key
                elif current_key < key and self.actions[1] in self.graph[current_key]:
                    self.graph[current_key][1] = key
                    return key
        return False


    def generate(self, type_of_operation):
        self.generated_nodes+=1
        if type_of_operation == self.statement_options[0]:
            statement_str, code_str = operation_generator.generate()
            return statement_str, code_str, type_of_operation
        elif type_of_operation == self.statement_options[1]:
            statement_str, code_str = cond_generator.generate()
            return statement_str, code_str, type_of_operation
        elif type_of_operation == self.statement_options[2]:
            statement_str, code_str = iteration_generator.generate()
            list_var = "list" + str(len(self.list_variables) + 1)
            statement_str = statement_str.replace("{list}", list_var)
            code_str = code_str.replace("{list}", list_var)
            self.list_variables.append(list_var)
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
        x_var = "x"
        separator = ", "
        number_of_tests = 4 
        test_cases = []
        test_lists = []
        list_size = random.randint(4, 6)

        occurences_of_lists = solution_code.count(self.code_keywords[3])

        for i in range(number_of_tests):
            input_parameters = []
            input_lists = []
            for j in range(complexity - 1):
                rand_num = random.randint(1,100)
                input_parameters.append(rand_num)
            for j in range(occurences_of_lists):
                input_lists = "["
                for k in range(list_size):
                    rand_int = random.randint(1,100)
                    if k == list_size - 1:
                        input_lists += str(rand_int)
                    else:
                        input_lists += str(rand_int) + separator
                input_lists += "]"
                test_lists.append(input_lists)

            test_cases.append(input_parameters)
        
        input_var = ""
        for i in range(1, complexity):
            if i == complexity - 1:
                input_var += x_var+str(i)
            else:
                input_var += x_var+str(i)+separator

        for i in range(occurences_of_lists):
            if i == occurences_of_lists - 1:
                input_var += separator + self.list_variables[i]
            else:
                input_var += separator + self.list_variables[i] 

        test_case_array = []

        for i in range (len(test_cases)):
            test_variables = ""
            for j in range(len(test_cases[i])):
                if j == len(test_cases[i]) - 1:
                    test_variables += str(test_cases[i][j])
                else:
                    test_variables += str(test_cases[i][j]) + separator
            for j in range(occurences_of_lists):
                if j == occurences_of_lists - 1:
                    test_variables += separator + str(test_lists[i])
                else:
                    test_variables += separator + str(test_lists[i]) 
        
            run_str = f"print(problem({test_variables}))"
            test_case_array.append(run_str)

        
        function_str = f"def problem({input_var}):"

        self.problem_object["statement"] = problem_statement
        self.problem_object["testCases"] = test_case_array
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
        spaces = '  '  
        tab = '    '

        stack.append(-1)
        #this does work for all cases, but its not a pretty solution, based on return always ending each code segment
        for node in final_list:
            if self.code_keywords[0] in node:
                solution_code += '\n' + len(stack)*tab+ node
                stack.append(0)
            elif self.code_keywords[1] in node:
                solution_code += '\n' + len(stack)*tab+ node
                stack.append(1)
            elif self.code_keywords[2] in node:
                solution_code += '\n' + len(stack)*tab + node
                if len(stack) > 0:
                    popped = -inf
                    while popped != 0 and len(stack) > 1:
                        popped = stack.pop()
            elif self.code_keywords[3] in node:
                solution_code += '\n' + len(stack)*tab + node
                stack.append(2)
            elif self.code_keywords[4] in node:
                solution_code += '\n' + len(stack)*tab + node
                if len(stack) > 0:
                    popped = -inf
                    while popped != 2 and len(stack) > 1:
                        popped = stack.pop()
            else:
                solution_code += '\n' + len(stack)*tab + node

        solution_code = solution_code.replace(self.code_keywords[4], "")

        for node in output_statements:
            if self.keywords[1] in node:
                problem_statement += '\n' + len(stack)*spaces + node
                stack.append(0)
            elif self.keywords[3] in node:
                problem_statement += '\n' + len(stack)*spaces + node
                stack.append(1)
            #we can use code keywords, because return is the same in both
            elif self.code_keywords[2] in node:
                problem_statement += '\n' + len(stack)* spaces + node
                if len(stack) > 0:
                    popped = -inf
                    while popped != 0 and len(stack) > 1:
                        popped = stack.pop()
            else:
                problem_statement += '\n' + len(stack)* spaces + node
        return problem_statement, solution_code
        
generator = ProgrammingGenerator()
print(generator.start(3))
