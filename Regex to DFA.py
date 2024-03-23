import string

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
        self.alphabet = {'a', 'b'}

    def add_state(self, state):
        self.states.add(state)

    def set_start_state(self, state):
        self.start_state = state

    def add_accept_state(self, state):
        self.accept_states.add(state)
    def add_to_alphabet(self, symbol):
        self.alphabet.add(symbol)
    def set_alphabet(self,alphabet):
        self.alphabet = alphabet
    def dot_product(self, current_state,second_state):
        for i in self.alphabet:
            current_state.add_transition(i,second_state)
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
    
    def is_accepted(self, input_string,regex):
        current_state = self.start_state
        n = len(regex)
        input_string = input_string + " "* n
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
    def convert_alphabet_to_set(self, new_alphabet_set):
        self.alphabet = new_alphabet_set

def regex_to_dfa(regex):
    dfa = DFA()
    start_state = State("s")
    dfa.set_start_state(start_state)
    dfa.add_state(start_state)
    final_state = State("f")
    dfa.add_accept_state(final_state)
    alphanumeric_set = generate_alphanumeric_set()
    """dfa.set_alphabet(alphanumeric_set)"""

    current_state = parse_regex(regex, start_state, dfa, 0)
    current_state.add_transition(" ", final_state)
    final_state.add_transition(" ", final_state)
    

    return dfa

    
def parse_regex(regex, start_state, dfa , j):
    current_state = start_state
    
    n = len(regex)
    
    while j < n:
        
        
        
        char = regex[j]
        if char == '(':
            group_end_index = find_group_end_index(regex, j)
            bracket_start_state = current_state
            bracket_index= j +1
            
            group_regex = regex[j+1:group_end_index]
            parse_regex(group_regex, current_state, dfa, j)
            
            j = group_end_index
        
        elif char == '|':
            try:
                if bracket_start_state:
                    second_state = bracket_start_state
                    p = parse_regex(regex[j+1:],start_state,dfa,0)
                    p.add_transition(" ", second_state)
                    break
            
            except UnboundLocalError:
                start_state = dfa.get_state("s")
                second_state = current_state
                p = parse_regex(regex[j+1:],start_state,dfa,0)
                p.add_transition(" ", second_state)
                break
                
    
                           
        elif char == '*':
            if regex[j-1] == ".":
                
                    
                        
                dfa.dot_product(current_state,current_state)
            
            
            elif regex[j-1] == ")":
                
                
                current_state = dfa.get_state(str(len(dfa.states)-1))
                second_state = dfa.get_state(str(bracket_index))
                bracket_start_state.add_transition(" ", current_state)
                
                while regex[bracket_index] == "(":
                    bracket_index =bracket_index +1
                if regex[bracket_index] == ".":
                    dfa.dot_product(current_state,second_state)
                else:

                    current_state.add_transition(regex[bracket_index],second_state)

                
                
                
            else:

            
                current_state.add_transition(regex[j-1], current_state)
                prev_state = dfa.get_state(str(len(dfa.states)-2))
                if prev_state:

                    prev_state.add_transition(" ",current_state)
                else:
                    prev_state = dfa.get_state("s")
                    prev_state.add_transition(" ",current_state)
                
        elif char == '+':
            
            if regex[j-1] == ".":
                dfa.dot_product(current_state,current_state)
            
            elif regex[j-1] == ")":
                
                
                current_state = dfa.get_state(str(len(dfa.states)-1))
                second_state = dfa.get_state(str(bracket_index))
                
                while regex[bracket_index] == "(":
                    bracket_index =bracket_index +1
                if regex[bracket_index] == ".":
                    dfa.dot_product(current_state,second_state)
                else:

                    current_state.add_transition(regex[bracket_index],second_state)
                
                
            else:

                
                current_state.add_transition(regex[j-1], current_state)
                
                
            
            
        else:
            new_state = State(str(len(dfa.states)))
            if char == '.':
                
                
                dfa.dot_product(current_state,new_state)
            
            
            else:
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
def parse_string(string,regex,outputstring =""):
    for i in string:
        for j in regex:
            if i == j:
                outputstring = outputstring + j
                
            elif j == "*":
                outputstring = outputstring + " "
                break
    return outputstring

def generate_alphanumeric_set():
    alphanumeric_set = {chr(i) for i in range(48, 58)}  
    alphanumeric_set.update({chr(i) for i in range(65, 91)}) 
    alphanumeric_set.update({chr(i) for i in range(97, 123)})  
    return alphanumeric_set
        
if __name__ == "__main__":
    
    
    regex = "(aaabbb)*"
    dfa = regex_to_dfa(regex)
    
    dfa.print_dfa()
    test_string = "aaabbb"
    
    
    
    

    
    
    
    
    if dfa.is_accepted(test_string,regex):
        print(f"The string '{test_string}' is accepted by the DFA.")
    else:
        print(f"The string '{test_string}' is NOT accepted by the DFA.")
    
    
    
    