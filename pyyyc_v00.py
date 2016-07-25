from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


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
