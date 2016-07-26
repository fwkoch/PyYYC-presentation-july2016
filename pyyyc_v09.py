from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from six import string_types


class SpecialProp(object):
    """ class SpcecialProp

    This class is used for assigning properties. It validates the
    property, then sets it to a secret name.

    Input:
        secret_name - the name where the actual property value is assigned
    """

    def __init__(self, secret_name):
        self.secret_name = secret_name

    def __get__(self, instance, owner):
        # if not hasattr(instance, self.secret_name):
        #     raise ValueError('{}: property not set'.format(
        #         self.secret_name[1:]
        #     ))
        return getattr(instance, self.secret_name)

    def __set__(self, instance, value):
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


class PyYYCPresentation(object):
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

    presenter = StrProp('_presenter')
    topic = StrProp('_topic')
    time_limit = FloatProp('_time_limit')
    nslides = IntProp('_nslides')
    slide_color = ColorProp('_slide_color')

    def __init__(self, **kwargs):
        for key in kwargs:
            # if key[0] == '_':
            #     raise KeyError('Cannot set private property: {}'.format(key))
            # if not isinstance(kwargs[key], SpecialProp):
            #     raise KeyError('Property not available: {}'.format(key))
            # if not hasattr(self, key):
            #     raise KeyError('Attribute does not exist: {}'.format(key))
            # if not isinstance(self.__class__.__dict__[key], SpecialProp):
            #     raise KeyError('Attribute not a property: {}'.format(key))
            setattr(self, key, kwargs[key])

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
