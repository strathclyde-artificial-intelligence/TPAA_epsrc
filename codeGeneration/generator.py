import random

node_op = {
        "operation1": "{O} = {1} + {2} [A]", 
        "operation2": "{O} = {1} * {2} [A]", 
        "operation3": "{O} = {1} - {2} [A]", 
        }

node_cond = {
        "condition1": "if {1} == {2}: [A]else: [B]", 
        "condition2": "if {1} >= {2}: [A]else: [B]", 
        }

node_ret = "return {1}"


operations = {
        "operation1": "Get the total of {1} + {2}, store the result in {O}. [A]", 
        "operation2": "Get the product of {1} * {2}, store the result in {O}. [A]", 
        "operation3": "Get the total of {1} - {2}, store the result in {O}. [A]", 
        }

conditionals = {
        "condition1": "If {1} and {2} are equal: [A]. otherwise, [B]", 
        "condition2": "If {1} is greater than or equal to {2}: [A]. otherwise, [B]", 
        }

operation_ret = {
        "operation_ret1": "return {1}", 
        }


class ProgrammingGenerator:
    def __init__(self):
        self.graph = {}
        self.statements = {}
        self.code = {}
        self.statement_options = ["operation", "condition"]
        self.actions = ["A", "B"]
        self.action_slots = ["[A]", "[B]"]
        self.operands = ["{1}", "{2}"]
        self.output = "{O}"
        self.keywords = ["return {1}", "If", "Get"]


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
                    self.graph[key] = None
                if self.actions[1] in self.graph[index]:
                    key+=1
                    self.graph[index][1] = key
                    self.statements[key] = "return {1}"
                    self.code[key] = node_ret
                    self.graph[key] = None

            self.assign_node_parameters(complexity)
            self.indent_code()

            return self.statements[1]


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
        self.add_function_input(complexity)
        self.fill_remaining()
        self.build_statements()


    def update_statements(self, index, statement, code_str, operand_to_replace, x_var, count):
        if self.operands[0] in statement and self.operands[1] in statement:
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
                new_code = code_str.replace(operand_to_replace, x_var + str(count))
                self.statements[index] = new_statement

    #this function adds input parameters into the statement
    def add_function_input(self, complexity):
        y_var = "y"
        #we create the number of input nodes, we do this by creating complexity - 1 input nodes, 
        inputs_to_add = []
        for i in range(1, complexity):
            inputs_to_add.append(y_var+str(i))

        graph_list_keys = list(self.graph.keys()) #we pick any random node from the graph and check if it has some free slot of any sort random_node = random.choice(graph_list_keys)
        operand_to_replace = random.choice(self.operands)

        max_tries = 100
        count = 0

        while count < len(inputs_to_add):
            random_node = random.choice(graph_list_keys)
            operand_to_replace = random.choice(self.operands)
            if operand_to_replace in self.statements[random_node]:
                new_statement = self.statements[random_node].replace(operand_to_replace, inputs_to_add[count])
                new_code = self.code[random_node].replace(operand_to_replace, inputs_to_add[count])
                self.statements[random_node] = new_statement
                self.code[random_node] = new_code
                count+=1
            

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
            visited.add(node)
            if self.graph[node] == None:
                return visited
            else:
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
            if node_numbers == None:
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


    def indent_code(self):
        #how is this done in a good way?

        new_list = self.code[1].split('\n')

        final_list = []
        #we have to remove empty spaces from list
        for node in new_list:
            if '' != node:
                final_list.append(node)


        stack = []
        prev = ""

        for nodes in final_list:
            if "if" in nodes:
                print(len(stack)*'\t' + nodes)
                stack.append(nodes)
            elif "else" in nodes:
                stack.pop()
                print(len(stack)*'\t' + nodes)
            else:
                print(len(stack)*'\t' + nodes)



generator = ProgrammingGenerator()
generator.start(3)
