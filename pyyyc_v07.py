from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from six import string_types


class SpecialProp(object):

    def __init__(self, secret_name):
        self.secret_name = secret_name

    def __get__(self, instance, owner):
        return getattr(instance, self.secret_name)

    def __set__(self, instance, value):
        value = self.confirm(value)
        setattr(instance, self.secret_name, value)

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


class ReallyBasicPresentation(object):
    """This whole thing is just such a mess let's not even bother with
    these doc strings...

    Ugh...
    """

    presenter = StrProp('_presenter')

    def __init__(self, presenter):
        self.presenter = presenter


class NormalPresentation(ReallyBasicPresentation):

    topic = StrProp('_topic')
    time_limit = FloatProp('_time_limit')

    def __init__(self, presenter, topic, time_limit):
        super().__init__(presenter)
        self.topic = topic
        self.time_limit = time_limit


class PowerpointPresentation(NormalPresentation):

    nslides = IntProp('_nslides')
    slide_color = ColorProp('_slide_color')

    def __init__(self, presenter, topic, time_limit, nslides, slide_color):
        super().__init__(presenter, topic, time_limit)
        self.nslides = nslides
        self.slide_color = slide_color


class PyYYCPresentation(PowerpointPresentation):

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


class YYCjsPresentation(PowerpointPresentation):

    def summarize(self):
        print('JavaScripter {name} talking about {topic}.'.format(
            name=self.presenter,
            topic=self.topic
        ))

    def time_per_slide(self):
        return self.time_limit / self.nslides

    def strains_eyes(self):
        return False


class FreeSpiritPresentation(ReallyBasicPresentation):

    favorite_color = ColorProp('_favorite_color')

    def __init__(self, presenter, favorite_color):
        super().__init__(self, presenter)
        self.favorite_color = favorite_color

    def summarize(self):
        print('{name} loves {topic}.'.format(
            name=self.presenter,
            topic=self.favorite_color
        ))
