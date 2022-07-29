# coding : utf 8
import random

#%end keyword is used for splitting the code so that indentation works properly
#: are used to split the statement phrases
#indentation is carried out in main function

node_iteration = {
        "iterator1": "avg = 0\nfor num in {list}:\navg += num %end\n{O} = (avg // len({list})) + {1}[A]", 
        "iterator2": "odds = 0\nfor num in {list}:\nif num % 2 == 1:\nodds += num %end\n{O} = odds + {1}[A]", 
        "iterator3": "evens = 0\nfor num in {list}:\nif num % 2 == 0:\nevens += num %end\n{O} = evens + {1}[A]", 
        "iterator4": "max_num = -math.inf\nfor num in {list}:\nif max_num < num:\nmax_num = num %end\n{O} = max_num + {1}[A]", 
        "iterator5": "min_num = math.inf\nfor num in {list}:\nif num < min_num:\nmin_num = num %end\n{O} = min_num + {1}[A]", 
        "iterator6": "avg = 0\nfor num in {list}:\navg += num %end\n{O} = (avg // len({list})) - {1}[A]", 
        "iterator7": "odds = 0\nfor num in {list}:\nif num % 2 == 1:\nodds += num %end\n{O} = odds - {1}[A]", 
        "iterator8": "evens = 0\nfor num in {list}:\nif num % 2 == 0:\nevens += num %end\n{O} = evens - {1}[A]", 
        "iterator9": "max_num = -math.inf\nfor num in {list}:\nif max_num < num:\nmax_num = num %end\n{O} = max_num - {1}[A]", 
        "iterator10": "min_num = math.inf\nfor num in {list}:\nif num < min_num:\nmin_num = num %end\n{O} = min_num - {1}[A]", 
        }

iteration = {
        "iterator1": "Get the average from the {list} rounded down,:add {1} to the average,:and store the result in {O}.:[A]", 
        "iterator2": "Get the sum off all the odd numbers from {list},:add {1} to the sum,:and store the result in {O}.:[A]", 
        "iterator3": "Get the sum off all even numbers from {list},:add {1} to the sum,:and store the result in {O}.:[A]", 
        "iterator4": "Find the largest number in {list},:add {1} to it,:and store the result in {O}.:[A]", 
        "iterator5": "Find the smallest number in {list},:add {1} to it,:and store the result in {O}.:[A]", 
        "iterator6": "Get the average from the {list} rounded down,:subtract {1} from the average,:and store the result in {O}.:[A]", 
        "iterator7": "Get the sum off all the odd numbers from {list},:subtract {1} from the sum,:and store the result in {O}.:[A]", 
        "iterator8": "Get the sum off all even numbers from {list},:subtract {1} from the sum,:and store the result in {O}.:[A]", 
        "iterator9": "Find the largest number in {list},:subtract {1} from it,:and store the result in {O}.:[A]", 
        "iterator10": "Find the smallest number in {list},:subtract {1} from it,:and store the result in {O}.:[A]", 
        }

def generate():

    random_node = random.choice(list(iteration))
    statement = iteration[random_node]
    code = node_iteration[random_node]
    return statement, code

