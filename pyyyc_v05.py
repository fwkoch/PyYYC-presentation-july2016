from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import super
from six import string_types


def confirm_color(value):
    """ This function validates colors, either 'red', 'green', 'blue', or
    rgb color
    """
    if value == 'red':
        value = [255, 0, 0]
    if value == 'green':
        value = [0, 255, 0]
    if value == 'blue':
        value = [0, 0, 255]
    if not isinstance(value, (list, tuple)) or not len(value) == 3:
        raise ValueError('{}: must be rgb color'.format(value))
    # for v in value:
    #     if not isinstance(v, int):
    #         raise ValueError('{}: rgb must be ints'.format(value))
    #     if not 0 <= v < 256:
    #         raise ValueError('{}: rgb must be 0-255'.format(value))
    return value

def confirmFloat(value):
    """ This function validates floats """
    if not isinstance(value, float):
        raise ValueError('{}: must be float'.format(value))
    return value

def confirmInt(value):
    """ This function validates integers """
    if not isinstance(value, int):
        raise ValueError('{}: must be int'.format(value))
    return value

def confirmStr(value):
    """ This function validates strings """
    if not isinstance(value, string_types):
        raise ValueError('{}: must be string'.format(value))
    return value


class ReallyBasicPresentation(object):
    """ class ReallyBasicPresentation

    This class contains info about really basic presentations.

    Inputs:
        presenter    - All presentations have presenters
    """

    def __init__(self, presenter):
        self.presenter = presenter

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, value):
        self._presenter = confirmStr(value)


class NormalPresentation(ReallyBasicPresentation):
    """ class NormalPresentation

    This class contains some more normal presentation stuff.

    Inputs:
        topic        - Most normal presentations have a topic
        time_limit   - and a time limit
    """

    def __init__(self, presenter, topic, time_limit):
        super().__init__(presenter)
        self.topic = topic
        self.time_limit = time_limit

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, value):
        self._topic = confirmStr(value)

    @property
    def time_limit(self):
        return self._time_limit

    @time_limit.setter
    def time_limit(self, value):
        self._time_limit = confirmFloat(value)


class PowerpointPresentation(NormalPresentation):
    """ class PowerpointPresentation

    This class contains some additional ppt stuff.

    Inputs:
        nslides      - Number of slides
        slide_color  - Background color, rgb
    """

    def __init__(self, presenter, topic, time_limit, nslides, slide_color):
        super().__init__(presenter, topic, time_limit)
        self.nslides = nslides
        self.slide_color = slide_color

    @property
    def nslides(self):
        return self._nslides

    @nslides.setter
    def nslides(self, value):
        self._nslides = confirmInt(value)

    @property
    def slide_color(self):
        return self._slide_color

    @slide_color.setter
    def slide_color(self, value):
        self._slide_color = confirmColor(value)


class PyYYCPresentation(PowerpointPresentation):
    """ class PyYYCPresentation

    This class generates some really useful info about PyYYC presentations.
    """

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


class YYCjsPresentation(PowerpointPresentation):
    """ class YYCjsPresentation

    This class generates some really useful info about YYCjs presentations.
    """

    def summarize(self):
        """Print a short description of the presentation. Useful for
        press junkets.
        """
        print('JavaScripter {name} talking about {topic}.'.format(
            name=self.presenter,
            topic=self.topic
        ))

    def time_per_slide(self):
        """Time available for each slide"""
        return self.time_limit / self.nslides

    def strains_eyes(self):
        """Determines if the slides will cause eye strain"""
        return False


class FreeSpiritPresentation(ReallyBasicPresentation):
    """ class FreeSpiritPresentation

    These presentations are just silly.

    Inputs:
        favorite_color - Presenter's favorite color
    """

    def __init__(self, presenter, favorite_color):
        super().__init__(presenter)
        self.favorite_color = favorite_color

    @property
    def favorite_color(self):
        return self._favorite_color

    @favorite_color.setter
    def favorite_color(self, value):
        self._favorite_color = confirmColor(value)

    def summarize(self):
        """Print a short description of the presentation. Useful for
        press junkets.
        """
        print('{name} loves {topic}.'.format(
            name=self.presenter,
            topic=self.favorite_color
        ))
