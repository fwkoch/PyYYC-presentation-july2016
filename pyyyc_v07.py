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
    """ class ColorProp

    This SpecialProp validates colors
    """

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
    """ class FloatProp

    This SpecialProp validates floats
    """

    def confirm(self, value):
        if not isinstance(value, float):
            raise ValueError('{}: must be float'.format(value))
        return value


class IntProp(SpecialProp):
    """ class IntProp

    This SpecialProp validates integers
    """

    def confirm(self, value):
        if not isinstance(value, int):
            raise ValueError('{}: must be int'.format(value))
        return value


class StrProp(SpecialProp):
    """ class StrProp

    This SpecialProp validates strings
    """

    def confirm(self, value):
        if not isinstance(value, string_types):
            raise ValueError('{}: must be string'.format(value))
        return value


class ReallyBasicPresentation(object):
    """ class ReallyBasicPresentation

    This class contains info about really basic presentations.

    Inputs:
        presenter    - All presentations have presenters
    """

    presenter = StrProp('_presenter')

    def __init__(self, presenter):
        self.presenter = presenter


class NormalPresentation(ReallyBasicPresentation):
    """ class NormalPresentation

    This class contains some more normal presentation stuff.

    Inputs:
        topic        - Most normal presentations have a topic
        time_limit   - and a time limit
    """

    topic = StrProp('_topic')
    time_limit = FloatProp('_time_limit')

    def __init__(self, presenter, topic, time_limit):
        super().__init__(presenter)
        self.topic = topic
        self.time_limit = time_limit


class PowerpointPresentation(NormalPresentation):
    """ class PowerpointPresentation

    This class contains some additional ppt stuff.

    Inputs:
        nslides      - Number of slides
        slide_color  - Background color, rgb
    """

    nslides = IntProp('_nslides')
    slide_color = ColorProp('_slide_color')

    def __init__(self, presenter, topic, time_limit, nslides, slide_color):
        super().__init__(presenter, topic, time_limit)
        self.nslides = nslides
        self.slide_color = slide_color


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

    favorite_color = ColorProp('_favorite_color')

    def __init__(self, presenter, favorite_color):
        super().__init__(self, presenter)
        self.favorite_color = favorite_color

    def summarize(self):
        """Print a short description of the presentation. Useful for
        press junkets.
        """
        print('{name} loves {topic}.'.format(
            name=self.presenter,
            topic=self.favorite_color
        ))
