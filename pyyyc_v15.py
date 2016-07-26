from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from six import string_types
from six import with_metaclass


class SpecialProp(object):
    """ class SpcecialProp

    This class is used for assigning properties. It validates the
    property, then sets it to a secret name, defined in a metaclass.
    """

    secret_name = None

    def __init__(self, doc):
        self.doc = doc

    def __get__(self, instance, owner):
        if self.secret_name is None:
            raise ValueError('secret_name not set!')
        if not hasattr(instance, self.secret_name):
            raise ValueError('{}: property not set'.format(
                self.secret_name[1:]
            ))
        return getattr(instance, self.secret_name)

    def __set__(self, instance, value):
        if self.secret_name is None:
            raise ValueError('secret_name not set!')
        value = self.confirm(value)
        setattr(instance, self.secret_name, value)

    def confirm(self, value):
        """ This function validates value. It is overwritten by different
        subclasses of SpecialProp
        """
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
    """ metaclass SecretNameMeta

    This metaclass manipulate its classes by creating a _props
    attribute that doesn't exist in the original definition and
    setting the secret_name of all the SpecialProp attributes
    """

    def __new__(mcs, name, bases, attrs):
        _props = []
        keys = [k for k in attrs]
        for key in keys:
            if isinstance(attrs[key], SpecialProp) and key == 'props':
                raise ValueError('Cannot have a SpecialProp named \'props\'')
            if isinstance(attrs[key], SpecialProp):
                _props += [key]
                attrs[key].secret_name = '_' + key

        attrs['_props'] = _props

        if '__doc__' not in attrs:
            attrs['__doc__'] = ''

        attrs['__doc__'] += '\n\n    Properties:\n'
        for prop in _props:
            attrs['__doc__'] += '        {prop} - {doc}\n'.format(
                prop=prop,
                doc=attrs[prop].doc
            )

        return super().__new__(mcs, name, bases, attrs)


class WithSpecialProps(with_metaclass(SecretNameMeta, object)):
    """ class WithSpecialProps

    This class contains the __init__ function to set SpecialProp
    properties through keyword arguments
    """

    def __init__(self, **kwargs):
        for key in kwargs:
            if key[0] == '_':
                raise KeyError('Cannot set private property: {}'.format(key))
            if key not in self._props:
                raise KeyError('Property is unavailable: {}'.format(key))
            setattr(self, key, kwargs[key])


class PyYYCPresentation(WithSpecialProps):
    """ class PyYYCPresentation

    This class contains info about basic presentations at the
    PyYYC meetup. It generates some really useful summary info
    about the presentation.

    Properties:
        presenter   - Name of the presenter
        topic       - Brief explanation of the topic
        time_limit  - Time limit of the presentation
        nslides     - Number of slides (because all presentations
                      have slides!)
        slide_color - RGB color of all the slides
    """

    presenter = StrProp('Name of the presenter')
    topic = StrProp('Brief explanation of the topic')
    time_limit = FloatProp('Time limit of the presentation in minutes')
    nslides = IntProp('Number of powerpoint slides')
    slide_color = ColorProp('RGB color of the slides')

    def summarize(self):
        """Print a short description of the presentation. Useful for
        press junkets.
        """
        print('Pythonista {name} talking about {topic}.'.format(
            name=self.presenter,
            topic=self.topic
        ))

    def time_per_slide(self):
        """Time available for each slide"""
        return self.time_limit / self.nslides

    def strains_eyes(self):
        """Determines if the slides will cause eye strain"""
        return(any([rgb > 200 for rgb in self.slide_color]) and
               any([rgb < 50 for rgb in self.slide_color]))
