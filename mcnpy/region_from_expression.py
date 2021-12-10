from mcnpy.region import Intersection, Union, Complement

def from_expression(expression, surfaces, cells):
        """Generate a region given an infix expression.

        Parameters
        ----------
        expression : str
            Boolean expression relating surface half-spaces. The possible
            operators are union '|', intersection ' ', and complement '~'. For
            example, '(1 -2) | 3 ~(4 -5)'.
        surfaces : dict
            Dictionary whose keys are suface IDs that appear in the Boolean
            expression and whose values are Surface objects.

        """

        # Strip leading and trailing whitespace
        expression = expression.strip()

        # Convert the string expression into a list of tokens, i.e., operators
        # and surface half-spaces, representing the expression in infix
        # notation.
        i = 0
        i_start = -1
        tokens = []
        while i < len(expression):
            if expression[i] in '()|~ ':
                # If special character appears immediately after a non-operator,
                # create a token with the apporpriate half-space
                if i_start >= 0:
                    j = int(expression[i_start:i])
                    if j < 0:
                        tokens.append(-surfaces[str(abs(j))])
                    else:
                        if len(tokens) > 0:
                            if tokens[len(tokens)-1] == '~':
                                tokens.append(cells[str(abs(j))])
                            else:
                                tokens.append(+surfaces[str(abs(j))])
                        else:
                            tokens.append(+surfaces[str(abs(j))])

                if expression[i] in '()|~':
                    # For everything other than intersection, add the operator
                    # to the list of tokens
                    tokens.append(expression[i])
                else:
                    # Find next non-space character
                    while expression[i+1] == ' ':
                        i += 1

                    # If previous token is a halfspace or right parenthesis and next token
                    # is not a left parenthese or union operator, that implies that the
                    # whitespace is to be interpreted as an intersection operator
                    if (i_start >= 0 or tokens[-1] == ')') and \
                       expression[i+1] not in ')|':
                        tokens.append(' ')

                i_start = -1
            else:
                # Check for invalid characters
                if expression[i] not in '-+0123456789':
                    raise SyntaxError("Invalid character '{}' in expression"
                                      .format(expression[i]))

                # If we haven't yet reached the start of a word, start one
                if i_start < 0:
                    i_start = i
            i += 1

        # If we've reached the end and we're still in a word, create a
        # half-space token and add it to the list
        if i_start >= 0:
            j = int(expression[i_start:])
            if j < 0:
                tokens.append(-surfaces[str(abs(j))])
            else:
                if len(tokens) > 0:
                    if tokens[len(tokens)-1] == '~':
                        tokens.append(cells[str(abs(j))])
                    else:
                        tokens.append(+surfaces[str(abs(j))])
                else:
                    tokens.append(+surfaces[str(abs(j))])

        # The functions below are used to apply an operator to operands on the
        # output queue during the shunting yard algorithm.
        def can_be_combined(region):
            return isinstance(region, Complement) or hasattr(region, 'surface')

        def apply_operator(output, operator):
            r2 = output.pop()
            if operator == ' ':
                r1 = output.pop()
                if isinstance(r1, Intersection):
                    r1 &= r2
                    output.append(r1)
                elif isinstance(r2, Intersection) and can_be_combined(r1):
                    r2.insert(0, r1)
                    output.append(r2)
                else:
                    output.append(r1 & r2)
            elif operator == '|':
                r1 = output.pop()
                if isinstance(r1, Union):
                    r1 |= r2
                    output.append(r1)
                elif isinstance(r2, Union) and can_be_combined(r1):
                    r2.insert(0, r1)
                    output.append(r2)
                else:
                    output.append(r1 | r2)
            elif operator == '~':
                output.append(~r2)

        # The following is an implementation of the shunting yard algorithm to
        # generate an abstract syntax tree for the region expression.
        output = []
        stack = []
        precedence = {'|': 1, ' ': 2, '~': 3}
        associativity = {'|': 'left', ' ': 'left', '~': 'right'}
        #print('TOKENS:\n' + str(tokens) + '\n')
        for token in tokens:
            if token in (' ', '|', '~'):
                # Normal operators
                while stack:
                    op = stack[-1]
                    if (op not in ('(', ')') and
                        ((associativity[token] == 'right' and
                          precedence[token] < precedence[op]) or
                         (associativity[token] == 'left' and
                          precedence[token] <= precedence[op]))):
                        apply_operator(output, stack.pop())
                    else:
                        break
                stack.append(token)
            elif token == '(':
                # Left parentheses
                stack.append(token)
            elif token == ')':
                # Right parentheses
                while stack[-1] != '(':
                    apply_operator(output, stack.pop())
                    if len(stack) == 0:
                        raise SyntaxError('Mismatched parentheses in '
                                          'region specification.')
                stack.pop()
            else:
                # Surface halfspaces
                output.append(token)
        while stack:
            if stack[-1] in '()':
                raise SyntaxError('Mismatched parentheses in region '
                                  'specification.')
            apply_operator(output, stack.pop())

        # Since we are generating an abstract syntax tree rather than a reverse
        # Polish notation expression, the output queue should have a single item
        # at the end
        #print('OUTPUT:'+'\n'+str(output[0])+'\n')
        return output[0]