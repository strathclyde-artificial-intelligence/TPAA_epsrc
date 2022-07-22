import random
node_op = {
        "operation1": "{O} = {1} + {2} [A]", 
        "operation2": "{O} = {1} * {2} [A]", 
        "operation3": "{O} = {1} - {2} [A]", 
        "operation4": "z = {1} + {2}\n{O} = z // 2 [A]", 
        }

operations = {
        "operation1": "Get the total of {1} + {2}, store the result in {O}.:[A]", 
        "operation2": "Get the product of {1} * {2}, store the result in {O}.:[A]", 
        "operation3": "Get the total of {1} - {2}, store the result in {O}.:[A]", 
        "operation4": "Get the average of {1} and {2}, store the result in {O}.:[A]", 
        }

def generate():
    random_key = random.choice(list(operations))
    code_str = node_op[random_key]
    statement_str = operations[random_key]
    return statement_str, code_str
