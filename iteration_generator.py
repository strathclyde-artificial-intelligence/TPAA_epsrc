import random

tabs = '    '

node_iteration = {
        "iterator1": "avg = 0\nfor num in {list}:\navg += num%end\n{O} = avg // len({list})[A]", 
        "iterator2": "{O} = 0\nfor num in {list}:\nif num % 2 == 1:\n{O} += num %end[A]", 
        "iterator3": "{O} = 0\nfor num in {list}:\nif num % 2 == 0:\n{O} += num %end[A]", 
        "iterator4": "{O} = -999999\nfor num in {list}:\nif num > {O} == 0:\n{O} = num %end[A]", 
        "iterator5": "{O} = 999999\nfor num in {list}:\nif num < {O} == 0:\n{O} = num %end[A]", 
        }

iteration = {
        "iterator1": "Get the average from the {list} and store it in {O}.:[A]", 
        "iterator2": "Get all the odd numbers from {list} and add them together in {O}.:[A]", 
        "iterator3": "Get all the even numbers from {list} and add them together in {O}.:[A]", 
        "iterator4": "Find the largest number in {list} and store it in {O}.:[A]", 
        "iterator5": "Find the smallest number in {list} and store it in {O}.:[A]", 
        }

def generate():

    random_node = random.choice(list(iteration))
    statement = iteration[random_node]
    code = node_iteration[random_node]
    return statement, code

