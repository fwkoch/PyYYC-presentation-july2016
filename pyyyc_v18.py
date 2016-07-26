from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import properties


class Person(properties.PropertyClass):
    """ class Person

    This class contains basic info about people
    """

    name = properties.String(
        'Name of person',
        required=True
    )
    bio = properties.String(
        'Short biography'
    )


class Slide(properties.PropertyClass):
    """ class Slide

    This class contains info about individual slides
    """

    topic = properties.String(
        'Topic of presentation',
        default='Python!'
    )
    slide_color = properties.Color(
        'Color of the slides',
        default='white'
    )

    def strains_eyes(self):
        return(any([rgb > 200 for rgb in self.slide_color]) and
               any([rgb < 50 for rgb in self.slide_color]))


class PyYYCPresentation(properties.PropertyClass):
    """ class PyYYCPresentation

    This class contains info about basic presentations at the
    PyYYC meetup. It generates some really useful summary info
    about the presentation.
    """

    presenter = properties.Pointer(
        'Presenter info',
        ptype=Person,
        required=True
    )
    topic = properties.String(
        'Topic of presentation',
        default='Python!'
    )
    time_limit = properties.Float(
        'Time limit in minutes',
        default=90.
    )
    slides = properties.Pointer(
        'Slideshow',
        ptype=Slide,
        repeated=True
    )

    def summarize(self):
        """Print a short description of the presentation. Useful for
        press junkets.
        """
        print('Pythonista {name} talking about {topic}.'.format(
            name=self.presenter.name,
            topic=self.topic
        ))

    def cliff_notes(self):
        """Print a long description of the presentation. """
        self.summarize()
        for i, slide in enumerate(self.slides):
            print('Slide {num}: {topic}'.format(
                num=i,
                topic=slide.topic
            ))

    def time_per_slide(self):
        """Time available for each slide"""
        return self.time_limit / len(self.slides)

    def strains_eyes(self):
        """Determines if the slides will cause eye strain"""
        return any(s.strains_eyes() for s in self.slides)
