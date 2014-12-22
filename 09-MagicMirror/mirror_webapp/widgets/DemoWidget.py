from AbstractWidget import AbstractWidget


class DemoWidget(AbstractWidget):

    def get_data(self, params):
        data = dict()
        data['greeting'] = 'Hello, world!'
        return data
