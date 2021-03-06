from abc import ABCMeta, abstractmethod

class Parser(object):
    __metaclass__ = ABCMeta

    def __init__(self, grammar):
        self._grammar = grammar

    @abstractmethod
    def parse(self, tokens):
        pass

    @property
    def grammar(self):
        return self._grammar


class Tree(object):
    def __init__(self, label, children):
        self._label = label
        self._children = children if isinstance(children, tuple) else tuple(children)

    def __repr__(self):
        return "Tree('{0}', {1})".format(self.label, self.children)

    def __str__(self):
        t = ' '.join([str(c)[:] for c in self.children])
        if t:
            return '({0} {1})'.format(self.label, t)
        return "'{0}'".format(self.label)

    @property
    def label(self):
        return self._label

    @property
    def children(self):
        return self._children

from shino.parser.recursivedescent import RecursiveDescentParser
from shino.parser.shiftreduce import ShiftReduceParser
