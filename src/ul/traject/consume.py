# -*- coding: utf-8 -*-

from grokcore.component import context, order, Subscription
from zope.interface import Interface, implements
from dawnlight.interfaces import IConsumer
from .model import default_component


class TrajectConsumer(Subscription):
    order(700)
    context(Interface)
    implements(IConsumer)

    def __call__(self, request, root, stack):
        # FIXME : PATTERNS is not defined. We need a better way to consume
        left = '/'.join((name for ns, name in reversed(stack)))
        Default = default_component(root, request)
        unconsumed, consumed, obj = PATTERNS.consume(root, left, Default)
        if consumed:
            return True, obj, stack[:-len(consumed)]
        return False, obj, stack
