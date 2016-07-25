from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import string_types


class PyYYCPresentation(object):
    """ class PyYYCPresentation

    This class contains info about basic presentations at the
    PyYYC meetup. It generates some really useful summary info
    about the presentation.

    Inputs:
        presenter   - Name of the presenter
        topic       - Brief explanation of the topic
        time_limit  - Time limit of the presentation
        nslides     - Number of slides (because all presentations
                      have slides!)
        slide_color - RGB color of all the slides
    """

    def __init__(self, presenter, topic, time_limit, nslides, slide_color):
        self.presenter = presenter
        self.topic = topic
        self.time_limit = time_limit
        self.nslides = nslides
        self.slide_color = slide_color

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, value):
        if not isinstance(value, string_types):
            raise ValueError('{}: presenter must be string'.format(value))
        self._presenter = value

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, value):
        if not isinstance(value, string_types):
            raise ValueError('{}: topic must be string'.format(value))
        self._topic = value

    @property
    def time_limit(self):
        return self._time_limit

    @time_limit.setter
    def time_limit(self, value):
        if not isinstance(value, float):
            raise ValueError('{}: time_limit must be float'.format(value))
        self._time_limit = value

    @property
    def nslides(self):
        return self._nslides

    @nslides.setter
    def nslides(self, value):
        if not isinstance(value, int):
            raise ValueError('{}: nslides must be int'.format(value))
        self._nslides = value

    @property
    def slide_color(self):
        return self._slide_color

    @slide_color.setter
    def slide_color(self, value):
        if value == 'red':
            value = [255, 0, 0]
        if value == 'green':
            value = [0, 255, 0]
        if value == 'blue':
            value = [0, 0, 255]
        if not isinstance(value, (list, tuple)) or not len(value) == 3:
            raise ValueError('{}: slide_color must be rgb color'.format(value))
        self._slide_color = value

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
        """Determines if the slides will cause eye strain based on their
        color
        """
        return(any([rgb > 200 for rgb in self.slide_color]) and
               any([rgb < 50 for rgb in self.slide_color]))
