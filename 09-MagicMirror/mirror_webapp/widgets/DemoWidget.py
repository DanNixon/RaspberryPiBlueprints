from AbstractWidget import AbstractWidget


class DemoWidget(AbstractWidget):

    def get_data(self, config):
        self.logger.info('Getting data for demo widget')
        data = dict()
        data['greeting'] = config.get('widget', 'text')
        return data
