from shino.parser import Parser, Tree
from shino.grammar import Token, TokenType
from shino import grammar

class ShiftReduceParser(Parser):
    @classmethod
    def make_sample(cls):
        return ShiftReduceParser(grammar.sample_grammar)
    
    def parse(self, tokens):
        '''
        >>> p = ShiftReduceParser(grammar.sample_grammar)
        >>> p.parse('the cat likes a dog'.split())
        Tree('S', (Tree('NP', (Tree('Det', (Tree('the', ()),)), Tree('N', (Tree('cat', ()),)))), Tree('VP', (Tree('V', (Tree('likes', ()),)), Tree('NP', (Tree('Det', (Tree('a', ()),)), Tree('N', (Tree('dog', ()),))))))))
        >>> p.parse('a dog likes the dog'.split())
        Tree('S', (Tree('NP', (Tree('Det', (Tree('a', ()),)), Tree('N', (Tree('dog', ()),)))), Tree('VP', (Tree('V', (Tree('likes', ()),)), Tree('NP', (Tree('Det', (Tree('the', ()),)), Tree('N', (Tree('dog', ()),))))))))
        '''


        remainings = [Token(v) for v in tokens]
        stack = []
        
        while remainings:
            self._shift(stack, remainings)
            while True:
                tree = self._reduce(stack, remainings)
                if not tree:
                    break
                stack.append(tree)

        if not(len(stack) == 1 and isinstance(stack[0], Tree)):
            raise ValueError('Parsing Failed') 
        return stack[0] 

    def _shift(self, stack, remainings):
        stack.append(remainings.pop(0))

    def _reduce(self, stack, remainings):
        for i in range(len(stack)):
            tokens = stack[i:]
            rules = self.grammar.rules
            for rule_name in rules:
                for rule in rules[rule_name]:
                    if self._match(rule, tokens):
                        for j in range(len(stack) - i):
                            stack.pop()
                        return Tree(rule_name, [t if isinstance(t, Tree) else Tree(t.surface, tuple()) for t in tokens])
        return None


    def _match(self, rule, tokens):
        if len(rule) != len(tokens):
            return False
        
        for i in range(len(rule)):
            if isinstance(tokens[i], Tree):
                if rule[i].type != TokenType.nonterminal:
                    return False
                if rule[i].surface != tokens[i].label:
                    return False
                continue
            
            if rule[i].type != TokenType.terminal:
                return False 
            if rule[i].surface != tokens[i].surface:
                return False
        return True
