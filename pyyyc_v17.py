from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import properties


class PyYYCPresentation(properties.PropertyClass):
    """ class PyYYCPresentation

    This class contains info about basic presentations at the
    PyYYC meetup. It generates some really useful summary info
    about the presentation.
    """

    presenter = properties.String('Name of presenter')
    topic = properties.String('Topic of presentation')
    time_limit = properties.Float('Time limit in minutes')
    nslides = properties.Int('Number of powerpoint slides')
    slide_color = properties.Color('Color of the slides')

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


class YYCjsPresentation(WithSpecialProps):
    """ class YYCjsPresentation

    This class contains info about basic presentations at the
    YYCjs meetup. It generates some really useful summary info
    about the presentation.
    """

    presenter = properties.String('Name of presenter')
    topic = properties.String('Topic of presentation')
    time_limit = properties.Float('Time limit in minutes')
    nslides = properties.Int('Number of powerpoint slides')
    slide_color = properties.Color('Color of the slides')

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


class FreeSpiritPresentation(WithSpecialProps):
    """ class FreeSpiritPresentation

    This class contains info about basic free-spirit presentations
    """

    presenter = properties.String('Name of presenter')
    favorite_color = properties.Color('Favorite color of presenter')

    def summarize(self):
        """Print a short description of the presentation. Useful for
        press junkets.
        """
        print('{name} loves {topic}.'.format(
            name=self.presenter,
            topic=self.favorite_color
        ))
