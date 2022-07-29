# coding : utf 8
import random
node_cond = {
        "condition1": "if {1} == {2}: [A]else: [B]", 
        "condition2": "if {2} <= {1}: [A]else: [B]", 
        "condition3": "if {1} <= {2}: [A]else: [B]", 
        "condition4": "if {1} < {2}: [A]else: [B]", 
        "condition5": "if {2} < {1}: [A]else: [B]", 
        }

conditionals = {
        "condition1": "If {1} and {2} are equal:[A]:otherwise,:[B]", 
        "condition2": "If {1} is greater than or equal to {2}:[A]:otherwise,:[B]", 
        "condition3": "If {1} is less than or equal to {2}:[A]:otherwise,:[B]", 
        "condition4": "If {1} is less than {2}:[A]:otherwise,:[B]", 
        "condition5": "If {1} is greater than {2}:[A]:otherwise,:[B]", 
        }

def generate():
    random_key = random.choice(list(conditionals))
    statement_str = conditionals[random_key]
    code_str = node_cond[random_key]
    return statement_str, code_str
