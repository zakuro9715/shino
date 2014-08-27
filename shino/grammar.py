from enum import Enum

class TokenType(str, Enum):
    allow = 'ALLOW'
    separator = 'SEP'
    terminal = 'TS'
    nonterminal = 'NTS'
    eol = 'EOL'
    

class Token(object):
    def __init__(self, surface, type = None):
        self._surface = surface
        if type:
            self._type = type
            return

        quote = '"'
        if surface == '->':
            self._type = TokenType.allow
        elif len(surface) >= 2 and surface[0] == quote and surface[-1] == quote:
            self._type = TokenType.terminal
            self._surface = surface[1:-1]
        elif surface == '|':
            self._type = TokenType.separator
        else:
            self._type = TokenType.nonterminal

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Token({0}, {1})".format(self.surface, self.type)

    @property
    def surface(self):
        return self._surface

    @property
    def type(self):
        return self._type

class CFG(object):
    def __init__(self, rules):
        self.rules = rules


def _found_syntax_error(line, expected, found):
    if expected:
        raise ValueError('line {0}: {1} expected but "{2}" ({3}) found'.format(line, expected, found.surface, found.type))
    else:   
        raise ValueError('line {0}: Unexpected  "{1}" ({2}) found'.format(line, found.surface, found.type))

def parse_string(text):
    """
    Parse string

    >>> parse_string(
    ...     'A -> "A" \\n'
    ... ).rules
    {'A': [[Token(A, TS)]]}

    >>> parse_string(
    ...     'A -> "A" "B" "C" \\n'
    ... ).rules
    {'A': [[Token(A, TS), Token(B, TS), Token(C, TS)]]}
    """
    if not isinstance(text, str):
        raise ValueError()
    
    token_lines = [[Token(s) for s in line.split()] for line in text.split('\n') if line]
    rules = dict()
    for line, tokens in enumerate(token_lines):
        if not tokens:
            continue

        # parse left
        if len(tokens) < 1 or tokens[0].type != TokenType.nonterminal:
            found = tokens[0] if len(tokens) else Token('EOL', TokenType.eol)
            _found_syntax_error(line, TokenType.nonterminal, found)
        left = tokens[0]

        # parse allow
        if len(tokens) < 2 or tokens[1].type != TokenType.allow:
            found = tokens[1] if len(tokens) > 1 else Token('EOL', TokenType.eol)
            _found_syntax_error(line, TokenType.allow, found)

        # parse rights
        if len(tokens) < 3:
            _found_syntax_error(line, None, Token('EOL', TokenType.eol))
    
        rights = []
        pool = []
        for token in tokens[2:]:
            if token.type == TokenType.separator:
                if not pool:
                    _found_syntax_error(line, None, token)
                rights.append(pool)
                pool = []
            else:
                pool.append(token)
        rights.append(pool)
        rules[left.surface] = rights

    return CFG(rules)

sample_grammar = parse_string('''
S -> NP VP
NP -> Det N
N -> "cat" | "dog"
Det -> "the" | "a"
VP -> V NP
V -> "likes"
''')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
