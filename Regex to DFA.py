class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}

class DFA:
    def __init__(self):
        self.states = set()
        self.start_state = None
        self.accept_states = set()

    def add_state(self, state):
        self.states.add(state)

    def set_start_state(self, state):
        self.start_state = state

    def add_accept_state(self, state):
        self.accept_states.add(state)
    def delete_state(self, state):
        
        self.states.remove(state)

        
        if state in self.accept_states:
            self.accept_states.remove(state)

        
        for s in self.states:
            transitions = s.transitions.copy()  
            for symbol, destinations in transitions.items():
                if state in destinations:
                    destinations.remove(state)
                    if not destinations:  
                        del s.transitions[symbol]
    
    def get_state(self, name):
        for state in self.states:
            if state.name == name:
                return state
        return None
    
    def is_accepted(self, input_string):
        current_state = self.start_state
        input_string = input_string + " "
        for symbol in input_string:
            
            if symbol in current_state.transitions:
                current_state = next(iter(current_state.transitions[symbol]))
            else:
                
                return False
        
        return current_state in self.accept_states

    def print_dfa(self):
       
        print("States:", ", ".join(s.name for s in self.states)+", f")
        print("Start state:", self.start_state.name)
        print("Accept states:", ", ".join(s.name for s in self.accept_states))
        print("Transitions:")
        for state in self.states:
            for symbol, destinations in state.transitions.items():
                for dest in destinations:
                    print(f"{state.name} -- {symbol} --> {dest.name}")

def regex_to_dfa(regex):
    dfa = DFA()
    start_state = State("s")
    dfa.set_start_state(start_state)
    dfa.add_state(start_state)
    final_state = State("f")
    dfa.add_accept_state(final_state)

    current_state = parse_regex(regex, start_state, final_state, dfa)
    current_state.add_transition(" ", final_state)
    

    return dfa

def parse_regex(regex, start_state, final_state, dfa):
    current_state = start_state
    i = 0
    n = len(regex)
    j = 0
    while j < n:
        
        
        char = regex[j]
        if char == '(':
            group_end_index = find_group_end_index(regex, i)
            bracket_start_state = current_state
            bracket_index= j +1
            
            group_regex = regex[i+1:group_end_index]
            parse_regex(group_regex, current_state, final_state, dfa)
            i = group_end_index
            j = group_end_index
        
        elif char == '|':
            
            branch_start_state = State(str(len(dfa.states)))
            dfa.add_state(branch_start_state)
            current_state.add_transition(None, branch_start_state)
            branch_final_state = State(str(len(dfa.states)))
            dfa.add_state(branch_final_state)
            parse_regex(regex[i+1:], branch_start_state, branch_final_state, dfa)
            current_state = branch_final_state
            break
        elif char == '*':
            prev_state = current_state
            
            
            if regex[j-1] == ")":
                new_state = State(str(len(dfa.states)-1))
                dfa.add_state(new_state)
                
                current_state = new_state
                second_state = dfa.get_state(str(bracket_index))
                
                current_state.add_transition(regex[bracket_index],second_state)
                
            else:

            
                current_state.add_transition(regex[j-1], current_state)
        
            
            
        else:
            
            new_state = State(str(len(dfa.states)))
            current_state.add_transition(char, new_state)
            dfa.add_state(new_state)
            
            current_state = new_state

        j = j +1
        
    return current_state

def find_group_end_index(regex, start_index):
    
    stack = []
    for i in range(start_index + 1, len(regex)):
        if regex[i] == '(':
            stack.append('(')
        elif regex[i] == ')':
            if not stack:
                return i
            stack.pop()
    return -1
if __name__ == "__main__":
    regex = "baba"
    dfa = regex_to_dfa(regex)
    dfa.print_dfa()
    test_string = "baba"
    if dfa.is_accepted(test_string):
        print(f"The string '{test_string}' is accepted by the DFA.")
    else:
        print(f"The string '{test_string}' is not accepted by the DFA.")
    
    
    
    