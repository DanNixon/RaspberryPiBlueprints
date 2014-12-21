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

    @abc.abstractmethod
    def name(self):
        """
        Gets the user friendly name for the widget.
        Used for the title on the UI.

        @return Widget title
        """
        return

    def string_id(self):
        """
        Gets a string ID for the widget.
        Currently just using the class name.

        @return A unique ID for the widget
        """
        return self.__class__.__name__


    def get_template_filename(self):
        """
        Gets the filename for the Flask template.

        @return Full template filename
        """
        template_filename = 'widgets/%s.html' % self.string_id()
        return template_filename
