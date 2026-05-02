# Collaborators
# Muhammad Haziq Mirza Ab Rahman
# Filzah Amiynah Shamshudin

def parser(file_name):
    grammar = {} # dictionary to store grammar rules

    file = open(file_name, "r")
    lines = file.readlines()
    file.close()

    n = int(lines[0].strip()) # This is to show that first line is number of rules in grammar

    # Traverse each rule in grammar
    for i in range(1, n + 1):
        line = lines[i].strip()
        if line == "":
            continue # This is for empty space lines in input text files
        parts = line.split("=")
        left = parts[0].strip() # This is for LHS non-terminals
        right = parts[1].strip() # This is for RHS terminals
        separator = right.split("|") # This is for OR cases in rules

        # Adding rules into dictionary
        if left not in grammar:
            grammar[left] = []

        for p in separator:
            grammar[left].append(p.strip())
    
    return grammar

def is_cnf(file_name):
    grammar = parser(file_name)

    # This is to go through each non-terminal
    for left in grammar:

        # This is to go through each case in each rules
        for separator in grammar[left]:

            # Case 1: epsilon 
            if separator == "$":
                continue

            # Case 2: single terminal (A --> a)
            if len(separator) == 1:
                single_char = separator[0]

                # This is to check if terminal is lowercase or digit
                if not (single_char.islower() or single_char.isdigit()):
                    return "no"
            
            # Case 3: more than one non-terminal (A --> BC)
            elif len(separator) == 2:
                first = separator[0]
                second = separator[1]

                if not (first.isupper() and second.isupper()):
                    return "no"
            
            # Anything else in invalid
            else:
                return "no"
    
    return "yes"

def generates_string(file_name, w):
    grammar = parser(file_name)

    # This is to check if CNF first
    if is_cnf(file_name) == "no":
        return "no"
    
    # This is to check if S directly produces the target string
    if "S" in grammar and w in grammar["S"]:
        return "yes"
    
    n = len(w)

    # Maximum number of steps is 2n - 1
    max_steps = 2 * n - 1

    # Start from S symbol
    current_set = set()
    current_set.add("S")
        
    # Continuation from start symbol
    for step in range(max_steps):
        next_set = set()

        # This is to go through all current strings
        for string in current_set:

            # This is to go through each position in string
            for i in range(len(string)):
                symbol = string[i]

                # If the symbol is non-terminal, we need to expand it
                if symbol in grammar:

                    for separator in grammar[symbol]:

                        # This is to replace symbol for production rules
                        new_string = string[:i] + separator + string[i + 1:]

                        if new_string == w:
                            return "yes"
                        
                        # Only add if length is valid, pruning
                        if len(new_string) <= len(w):
                            next_set.add(new_string)
        
        current_set = next_set

        if w in current_set:
            return "yes" # After generating new strings, this is to check if target string is achieved at this step

        if not current_set:
            break

    # This is to check if w is in our results
    if w in current_set:
        return "yes"
    else:
        return "no"
    
def run_in_one_minute(file_name,n):
    grammar = parser(file_name)

    # This is to check if CNF first
    if is_cnf(file_name) == "no":
        return "no"
    
    # This is to find maximum branching factor
    max_branch = 0
    for left in grammar:
        num_separators = len(grammar[left])
        if num_separators > max_branch:
            max_branch = num_separators

    # This is to calculate number of steps
    steps = 2 * n - 1

    # This is the limit for derivations
    limit = 10**7
    
    # This is to estimate total number of possibilities
    total = 1
    for i in range(steps):
        total = total * max_branch
        if total > limit:
            return "no"
    
    return "yes"
    
if __name__ == "__main__":
    file_name = "grammarG.txt"

    print("CNF check:", is_cnf(file_name))

    test_string = "acbcc"
    print("Generate string:", generates_string(file_name, test_string))

    n = len(test_string)
    print("Run in 1 minute:", run_in_one_minute(file_name, n))