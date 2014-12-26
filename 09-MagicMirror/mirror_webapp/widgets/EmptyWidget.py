from AbstractWidget import AbstractWidget


class EmptyWidget(AbstractWidget):

    def get_data(self, config):
        data = dict()
        return data
