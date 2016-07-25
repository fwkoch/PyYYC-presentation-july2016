from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from six import string_types


def confirmColor(func):
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
        return func(self, value)
    return confirm

def confirmFloat(func):
    def confirm(self, value):
        if not isinstance(value, float):
            raise ValueError('{}: must be float'.format(value))
        return func(self, value)
    return confirm

def confirmInt(func):
    def confirm(self, value):
        if not isinstance(value, int):
            raise ValueError('{}: must be int'.format(value))
        return func(self, value)
    return confirm

def confirmStr(func):
    def confirm(self, value):
        if not isinstance(value, string_types):
            raise ValueError('{}: must be string'.format(value))
        return func(self, value)
    return confirm


class ReallyBasicPresentation(object):
    """This whole thing is just such a mess let's not even bother with
    these doc strings...

    Ugh...
    """
    def __init__(self, presenter):
        self.presenter = presenter

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    @confirmStr
    def presenter(self, value):
        self._presenter = value


class NormalPresentation(ReallyBasicPresentation):

    def __init__(self, presenter, topic, time_limit):
        super().__init__(presenter)
        self.topic = topic
        self.time_limit = time_limit

    @property
    def topic(self):
        return self._topic

    @topic.setter
    @confirmStr
    def topic(self, value):
        self._topic = value

    @property
    def time_limit(self):
        return self._time_limit

    @time_limit.setter
    @confirmFloat
    def time_limit(self, value):
        self._time_limit = value


class PowerpointPresentation(NormalPresentation):

    def __init__(self, presenter, topic, time_limit, nslides, slide_color):
        super().__init__(presenter, topic, time_limit)
        self.nslides = nslides
        self.slide_color = slide_color

    @property
    def nslides(self):
        return self._nslides

    @nslides.setter
    @confirmInt
    def nslides(self, value):
        self._nslides = value

    @property
    def slide_color(self):
        return self._slide_color

    @slide_color.setter
    @confirmColor
    def slide_color(self, value):
        self._slide_color = value


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

    def __init__(self, presenter, favorite_color):
        super().__init__(self, presenter)
        self.favorite_color = favorite_color

    @property
    def favorite_color(self):
        return self._favorite_color

    @favorite_color.setter
    @confirmColor
    def favorite_color(self, value):
        self._favorite_color = value

    def summarize(self):
        print('{name} loves {topic}.'.format(
            name=self.presenter,
            topic=self.favorite_color
        ))
