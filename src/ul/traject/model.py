# -*- coding: utf-8 -*-

from uvclight.directives import context
from cromlech.browser import redirect_response
from cromlech.webob import response
from zope.interface import Interface
from dolmen.location import get_absolute_url


class DefaultModel(object):

    def __init__(self, **kws):
        self.kws = kws


class Model(object):
    context(Interface)

    model = None
    pattern = None

    def factory(*args):
        raise NotImplementedError

    def arguments(*args):
        raise NotImplementedError


def default_component(root, request):
    def factory(**kwargs):
        url = get_absolute_url(root, request)
        return redirect_response(response.Response, url)
    return factory

    
def register_models(registry, *models):
    for model in models:
        pattern = model.pattern
        factory = model.factory.im_func
        arguments = model.arguments.im_func
        root = context.bind(default=Interface).get(model)
        registry.register(model.model, root, pattern, factory, arguments)
