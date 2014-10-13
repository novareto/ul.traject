# -*- coding: utf-8 -*-

import traject
from dawnlight import ModelLookup
from .model import DefaultModel


class TrajectLookup(ModelLookup):

    def __init__(self, default=DefaultModel):
        self.patterns = traject.Patterns()
        self.default = default

    def register(self, model, root, pattern, factory, arguments):
        self.patterns.register(root, pattern, factory)
        self.patterns.register_inverse(root, model, pattern, arguments)

    def __call__(self, request, obj, stack):
        left = '/'.join((name for ns, name in reversed(stack)))
        unconsumed, consumed, obj = self.patterns.consume(
            obj, left, self.default)
        if consumed:
            return obj, stack[:-len(consumed)]
        return obj, stack
