
def to_postfix(infix):

   
    specialChars = {'*': 5, '+': 4, '?': 3, '.':2, '|':1}
    
    pofix, stack = "", ""

    
    for c in infix:
        
        if c =='(':
            stack = stack + c
        
        elif c ==')':
            
            while stack[-1] != '(':
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        
        elif c in specialChars:
            
            while stack and specialChars.get(c, 0) <= specialChars.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        
        else:
            pofix = pofix + c
    
    while stack:
        pofix, stack = pofix + stack[-1], stack[:-1]

   
    return pofix



class state:
   
    label, arrow1, arrow2 = None, None, None

class nfa:
    
    initial, accept = None, None 

    
    def __init__(self, initial, accept):
        self.initial = initial 
        self.accept =  accept
        


def compile(pofix):
    
    nfaStack = []

    for c in pofix:
       
        if c == '*':
            
            nfa1 = nfaStack.pop()
            
            initial, accept = state(), state()
            
            initial.arrow1, initial.arrow2 = nfa1.initial, accept
            
            nfa1.accept.arrow1, nfa1.accept.arrow2 = nfa1.initial, accept
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '.':
            
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            
            nfa1.accept.arrow1 = nfa2.initial
            
            nfaStack.append(nfa(nfa1.initial, nfa2.accept))
        
        elif c == '|':
            
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            
            initial = state()
            
            initial.arrow1, initial.arrow2 = nfa1.initial, nfa2.initial
            
            accept = state()
            
            nfa1.accept.arrow1, nfa2.accept.arrow1 = accept, accept
        
            nfaStack.append(nfa(initial, accept))
       
        elif c == '+':
            
            nfa1 = nfaStack.pop()
            
            accept, initial = state(), state()
            
            initial.arrow1 = nfa1.initial
            
            nfa1.accept.arrow1, nfa1.accept.arrow2 = nfa1.initial, accept
            
            nfaStack.append(nfa(initial, accept))
        
        elif c == '?':
            
            nfa1 = nfaStack.pop()
            
            accept, initial = state(), state()
            
            initial.arrow1, initial.arrow2 = nfa1.initial, accept
            
            nfa1.accept.arrow1 = accept
            
            nfaStack.append(nfa(initial, accept))
        else:
            
            accept, initial = state(), state()
            
            initial.label, initial.arrow1 = c, accept
           
            nfaStack.append(nfa(initial, accept))
        
    
    return nfaStack.pop()


def followes(state):
   
    states = set()
    states.add(state)

    
    if state.label is None:
       
        if state.arrow1 is not None:
            
            states |= followes(state.arrow1)
       
        if state.arrow2 is not None:
           
            states |= followes(state.arrow2)

   
    return states


def matchString(infix, string):
    
    postfix = to_postfix(infix)
    nfa = compile(postfix)

    
    currentState = set()
    nextState = set()

    
    currentState |= followes(nfa.initial)

   
    for s in string:
        
        for c in currentState:
            
            if c.label == s:
                
                nextState |= followes(c.arrow1)
        
        currentState = nextState
        nextState = set()
    
   
    return (nfa.accept in currentState)


class DFAState:
    def __init__(self, states):
        self.states = states
        self.transitions = {}


def nfa_to_dfa(nfa):
    alphabet = set()
    for c in nfa:
        if c.label is not None:
            alphabet.add(c.label)

    initial_states = followes(nfa.initial)
    dfa_initial = DFAState(initial_states)

    unmarked_states = [dfa_initial]
    dfa_states = [dfa_initial]

    while unmarked_states:
        current_dfa_state = unmarked_states.pop(0)

        for symbol in alphabet:
            next_states = set()
            for nfa_state in current_dfa_state.states:
                if nfa_state.label == symbol:
                    next_states |= followes(nfa_state.arrow1)

            if not next_states:
                continue

            next_dfa_state = None
            for dfa_state in dfa_states:
                if dfa_state.states == next_states:
                    next_dfa_state = dfa_state
                    break

            if next_dfa_state is None:
                next_dfa_state = DFAState(next_states)
                dfa_states.append(next_dfa_state)
                unmarked_states.append(next_dfa_state)

            current_dfa_state.transitions[symbol] = next_dfa_state

    return dfa_initial, dfa_states


def match_dfa(dfa_initial, string):
    current_state = dfa_initial

    for symbol in string:
        if symbol not in current_state.transitions:
            return False
        current_state = current_state.transitions[symbol]

    return True


def print_dfa(dfa_initial):
    dfa_states = [dfa_initial]
    while dfa_states:
        current_dfa_state = dfa_states.pop(0)
        print("DFA State:", current_dfa_state.states)
        for symbol, next_dfa_state in current_dfa_state.transitions.items():
            print("Transition on", symbol, "to DFA State:", next_dfa_state.states)
            if next_dfa_state not in dfa_states:
                dfa_states.append(next_dfa_state)


infixes = ["(a*.(a))*"]
strings = ["aaaaa"]

for infix in infixes:
    postfix = to_postfix(infix)
    nfa = compile(postfix)
    dfa_initial, dfa_states = nfa_to_dfa(nfa)

    print("NFA for infix:", infix)
    print_dfa(dfa_initial)

    for string in strings:
        print("Match for string:", string, match_dfa(dfa_initial, string))