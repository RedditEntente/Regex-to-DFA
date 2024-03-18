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
        # Remove state from set of states
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

    def print_dfa(self):
        print("DFA:")
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

    parse_regex(regex, start_state, final_state, dfa)

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
            bracket_start_state= current_state
            
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
            
            

            
            current_state.add_transition(regex[j-1], current_state)
        
        
            
        else:
            
            new_state = State(str(len(dfa.states)))
            current_state.add_transition(char, new_state)
            dfa.add_state(new_state)
            current_state = new_state

        j = j +1
    current_state.add_transition(None, final_state)

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
    regex = "abaa*"
    dfa = regex_to_dfa(regex)
    dfa.print_dfa()
    