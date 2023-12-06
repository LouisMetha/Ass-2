class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children else []
        self.achievable = False


def process_conditions(conditions):
    if '^' in conditions:
        return [condition.strip() for condition in conditions.split('^')], 'conjunctive'
    elif 'v' in conditions:
        return list(map(lambda x: [x.strip()], conditions.split('v'))), 'disjunctive'
    elif 'V' in conditions:
        return list(map(lambda x: [x.strip()], conditions.split('V'))), 'disjunctive'
    else:
        return [[conditions.strip()]], 'None'


def build_knowledge_base(rules):

    knowledge_base = {}

    for rule in rules:
        if '=>' in rule:
            condition, result = rule.split('=>')
            result = result.strip()
            conditions, condition_type = process_conditions(condition)
            
            if result not in knowledge_base:
                knowledge_base[result] = []

            if condition_type == 'conjunctive':
                knowledge_base[result].append(conditions)
            elif condition_type == 'disjunctive':
                knowledge_base[result].extend(conditions)
            else:
                knowledge_base[result].append(conditions[0])
        else:
            if rule not in knowledge_base:
                knowledge_base[rule] = [[]]
            else:
                knowledge_base[rule].insert(0,[])

    return [Node(key, value) for key, value in knowledge_base.items()]


def backward_chaining(goal, knowledge_base, visited=None):

    if visited is None:
        visited = set()

    for node in knowledge_base:
        if goal == node.value and node.achievable:
            return True
        
    if goal in visited:
        return False

    visited.add(goal)

    for node in knowledge_base:
        if goal == node.value:
            if [] in node.children:
                node.achievable = True
                return True

            for child_group in node.children:
                can_achieve_goal = True
                for conditions in child_group:
                    if not all(backward_chaining(cond, knowledge_base, visited) for cond in conditions):
                        can_achieve_goal = False
                        break

                if can_achieve_goal:
                    node.achievable = True
                    return True

    return False


def main():

    rules = []
    print("This is an extended propositional backward chaining system.\n")
    print("Enter facts to build knowledge base tree.\nType 'nil' to finish.\nExample for each fact: AvB=>E, D^E=>F etc.")
    
    while True:
        rule = input("Enter facts: ")
        if rule.lower() == 'nil':
            break
        rules.append(rule.upper())

    print('\nSee knowledge base nodes below:\n')
    knowledge_base = build_knowledge_base(rules)

    for node in knowledge_base:
        print(f'Node {node.value} : {node.children}')
    
    print("\nTest the system by entering a letter to be proven. Type 'quit' to exit\n")

    while True:
        goal = input("Prove: ")

        if goal.lower() == 'quit':
            break

        if backward_chaining(goal.upper(), knowledge_base):
            print(f"Yes, {goal.upper()} can be achieved.")
        else:
            print(f"No, {goal.upper()} cannot be achieved.")

if __name__ == "__main__":
    main()