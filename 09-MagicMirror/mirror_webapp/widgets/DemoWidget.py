from AbstractWidget import AbstractWidget


class DemoWidget(AbstractWidget):

    def get_data(self, config):
        self.logger.info('Getting data for demo widget')

        data = { 'greeting':'No Text Set!' }

        if 'text' in config:
            data['greeting'] = config['text']

        return data
