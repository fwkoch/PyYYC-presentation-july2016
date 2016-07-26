from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from six import string_types
from six import with_metaclass


class SpecialProp(object):

    def _set_secret_name(self):
        scope = self
        def fget(self):
            return getattr(self, '_' + scope.name, None)
        def fset(self, value):
            value = scope.confirm(value)
            setattr(self, '_' + scope.name, value)
        return property(fget=fget, fset=fset)

    def confirm(self, value):
        return value


class ColorProp(SpecialProp):

    def confirm(self, value):
        if value == 'red':
            value = [255, 0, 0]
        if value == 'green':
            value = [0, 255, 0]
        if value == 'blue':
            value = [0, 0, 255]
        if not isinstance(value, (list, tuple)) or not len(value) == 3:
            raise ValueError('{}: must be rgb color'.format(value))
        for v in value:
            if not isinstance(v, int):
                raise ValueError('{}: rgb must be ints'.format(value))
            if not 0 <= v < 256:
                raise ValueError('{}: rgb must be 0-255'.format(value))
        return value


class FloatProp(SpecialProp):

    def confirm(self, value):
        if not isinstance(value, float):
            raise ValueError('{}: must be float'.format(value))
        return value


class IntProp(SpecialProp):

    def confirm(self, value):
        if not isinstance(value, int):
            raise ValueError('{}: must be int'.format(value))
        return value


class StrProp(SpecialProp):

    def confirm(self, value):
        if not isinstance(value, string_types):
            raise ValueError('{}: must be string'.format(value))
        return value


class SecretNameMeta(type):

    def __new__(mcs, name, bases, attrs):
        _props = []
        keys = [k for k in attrs]
        for key in keys:
            if isinstance(attrs[key], SpecialProp):
                _props += [key]
                attrs[key].name = key
                attrs[key] = attrs[key]._set_secret_name()

        attrs['_props'] = _props

        return super().__new__(mcs, name, bases, attrs)


class WithSpecialProps(with_metaclass(SecretNameMeta, object)):

    def __init__(self, **kwargs):
        for key in kwargs:
            if key[0] == '_':
                raise KeyError('Cannot set private property: {}'.format(key))
            if key not in self._props:
                raise KeyError('Property is unavailable: {}'.format(key))
            setattr(self, key, kwargs[key])


class PyYYCPresentation(WithSpecialProps):

    presenter = StrProp()
    topic = StrProp()
    time_limit = FloatProp()
    nslides = IntProp()
    slide_color = ColorProp()

    def summarize(self):
        print('Pythonista {name} talking about {topic}.'.format(
            name=self.presenter,
            topic=self.topic
        ))

    def time_per_slide(self):
        return self.time_limit / self.nslides

    def strains_eyes(self):
        return(any([rgb > 200 for rgb in self.slide_color]) and
               any([rgb < 50 for rgb in self.slide_color]))


class YYCjsPresentation(WithSpecialProps):

    presenter = StrProp()
    topic = StrProp()
    time_limit = FloatProp()
    nslides = IntProp()
    slide_color = ColorProp()

    def summarize(self):
        print('JavaScripter {name} talking about {topic}.'.format(
            name=self.presenter,
            topic=self.topic
        ))

    def time_per_slide(self):
        return self.time_limit / self.nslides

    def strains_eyes(self):
        return False


class FreeSpiritPresentation(WithSpecialProps):

    presenter = StrProp()
    favorite_color = ColorProp()

    def summarize(self):
        print('{name} loves {topic}.'.format(
            name=self.presenter,
            topic=self.favorite_color
        ))
