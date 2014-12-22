import abc
from abc import ABCMeta


class AbstractWidget():
    """
    Base class for mirror widgets.
    """

    __metaclass__ = ABCMeta

    def get_data(self, config):
        """
        Gets data for widget if applicable.

        @param config COnfiguration data as dictionary
        @return Widget data as dictionary
        """
        return dict()


    def get_template_filename(self):
        """
        Gets the filename for the Flask template.

        @return Full template filename
        """
        template_filename = 'widgets/%s.html' % self.__class__.__name__
        return template_filename
