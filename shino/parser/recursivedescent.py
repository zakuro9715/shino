from shino import grammar
from shino.grammar import Token, TokenType
from shino.parser import Parser, Tree

class RecursiveDescentParser(Parser):
    @classmethod
    def make_sample(cls):
        return RecursiveDescentParser(grammar.sample_grammar)

    def parse(self, tokens):
        '''
        >>> p = RecursiveDescentParser(grammar.sample_grammar)
        >>> p.parse('the cat likes a dog'.split())
        Tree('S', (Tree('NP', (Tree('Det', (Tree('the', ()),)), Tree('N', (Tree('cat', ()),)))), Tree('VP', (Tree('V', (Tree('likes', ()),)), Tree('NP', (Tree('Det', (Tree('a', ()),)), Tree('N', (Tree('dog', ()),))))))))
        >>> p.parse('a dog likes the dog'.split())
        Tree('S', (Tree('NP', (Tree('Det', (Tree('a', ()),)), Tree('N', (Tree('dog', ()),)))), Tree('VP', (Tree('V', (Tree('likes', ()),)), Tree('NP', (Tree('Det', (Tree('the', ()),)), Tree('N', (Tree('dog', ()),))))))))
        '''

        tree = self._match_rule('S', tokens)
        if not tree:
            raise ValueError("Don't match any rules")
        return tree

    def _match_rule(self, rule_name, tokens):
        if rule_name not in self.grammar.rules:
            raise ValueError('{0} is undefined rule'.format(rule_name))
        
        for rule in self.grammar.rules[rule_name]:
            first = self._match(rule[0], tokens)
            if first:
                children = [first]
                for i, r in enumerate(rule[1:]):
                    m = self._match(r, tokens)
                    children.append(m)
                    if not m:
                        raise ValueError('{0} expected but {1} found'.format(r.surface, tokens[0] if tokens else 'EOF'))
                else:
                    return Tree(rule_name, children)
        return None


    def _match(self, rule, tokens):
        if rule.type == TokenType.nonterminal:
            return self._match_rule(rule.surface, tokens)

        if tokens and rule.surface == tokens[0]:
            return Tree(tokens.pop(0), tuple())
        
        if not tokens and rule.type == TokenType.terminal and rule.surface == '':
            return Tree('', tuple())
        return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
