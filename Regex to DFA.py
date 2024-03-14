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

    def print_dfa(self):
        print("DFA:")
        print("States:", ", ".join(s.name for s in self.states))
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
    for char in regex:
        if char == '(':
            # Handle group
            pass
        elif char == '|':
            # Handle alternation
            pass
        elif char == '*':
            # Handle Kleene star
            pass
        else:
            # Handle literals
            new_state = State(str(len(dfa.states)))
            current_state.add_transition(char, new_state)
            dfa.add_state(new_state)
            current_state = new_state

    
    current_state.add_transition(None, final_state)


if __name__ == "__main__":
    regex = "b*abb"
    dfa = regex_to_dfa(regex)
    dfa.print_dfa()
