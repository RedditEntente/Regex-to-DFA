def to_postfix(regex):
    """Convert infix regex to postfix notation with explicit concatenation operator."""
    output = []  # Output list of tokens
    stack = []  # Operator stack
    precedence = {'*': 3, '.': 2, '|': 1}  # Precedence of operators

    # Add explicit concatenation operators
    enhanced_regex = []
    for i, token in enumerate(regex):
        if i > 0 and (regex[i-1].isalnum() or regex[i-1] in ['*', ')']) and (token.isalnum() or token == '('):
            enhanced_regex.append('.')
        enhanced_regex.append(token)

    # Convert to postfix
    for token in enhanced_regex:
        if token.isalnum():  # Operand
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            top = stack.pop()
            while top != '(':
                output.append(top)
                top = stack.pop()
        else:  # Operator
            while (stack and precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ''.join(output)




class SyntaxTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Assuming the SyntaxTreeNode class and print_tree function are defined as before

def construct_tree(postfix):
    stack = []
    for char in postfix:
        if char in ['*', '|', '.']:
            node = SyntaxTreeNode(char)
            if char in ['*']:  # Unary operator, requires one operand only
                if stack:  # Check if the stack is not empty
                    node.left = stack.pop()
            else:  # Binary operators: '.' and '|'
                if len(stack) >= 2:  # Ensure there are at least two nodes to pop
                    node.right = stack.pop()
                    node.left = stack.pop()
            stack.append(node)
        else:
            stack.append(SyntaxTreeNode(char))
    return stack[-1]  # The root of the syntax tree



def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.value)
        print_tree(node.left, level + 1)


def match_tree(node, string):
    if node is None:
        return string == ""

    # Leaf node (literal character)
    if node.left is None and node.right is None:
        return string == node.value

    # Alternation
    if node.value == '|':
        return match_tree(node.left, string) or match_tree(node.right, string)

    # Concatenation
    if node.value == '.':
        for i in range(len(string) + 1):
            # Split the string for the left and right part to match
            if match_tree(node.left, string[:i]) and match_tree(node.right, string[i:]):
                return True
        return False

    # This basic matcher does not support '*' (Kleene star) or other operators effectively.
    # Implementing support for '*' would require a more complex handling to iterate over
    # multiple lengths of the beginning of the string that could be matched by the repeating
    # part of the pattern.
    
    return False  # For unsupported operations

# Example usage
regex = "a.b|c"  # Matches "ab" or "c"
postfix = to_postfix(regex)
tree = construct_tree(postfix)

# Test the matcher
test_strings = ["ab", "c", "abc", ""]
for s in test_strings:
    print(f"Does '{s}' match the pattern '{regex}'? {match_tree(tree, s)}")


