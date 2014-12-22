# -*- coding: utf-8 -*-
"""
"""

import importlib, ConfigParser, os, logging
from ConfigParser import NoOptionError
from flask import Flask, render_template, jsonify


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    LOG_LEVEL='DEBUG',
    LOG_FILE='mirror_app.log'
))
app.config.from_envvar('MAGIC_MIRROR_SETTINGS', silent=False)

log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), None)
logging.basicConfig(level=log_level, filename=app.config['LOG_FILE'])


def get_widget_configs(directory):
    """
    Reads the widget configuration files from a given directory.

    @param directory Directory to reaf diles from
    @return A dictionary of widget IDs to configurations
    """

    logging.getLogger(__name__).info('Parsing widget configuration files')
    configs = dict()

    for name in os.listdir(directory):
        file_path = os.path.join(directory, name)
        if os.path.isfile(file_path):
            logging.getLogger(__name__).debug('Reading config file %s' % name)
            widget_id = name.split('.')[0]
            configs[widget_id] = ConfigParser.ConfigParser()
            configs[widget_id].read(file_path)

    return configs


WIDGETS = get_widget_configs(app.config['WIDGET_CONFIG_DIR'])


def get_widget(widget_class):
    """
    Gets an instance of a widget class given it's name.

    @param widget_class Name of widget class
    @return Widget instance
    """

    logging.getLogger(__name__).info('Getting widget instance for %s' % widget_class)
    widget = importlib.import_module('widgets.%s' % widget_class)
    widget_obj = getattr(widget, widget_class)()

    return widget_obj


@app.route('/')
def render_mirror():
    """
    Renders the main widget screen for the mirror web application.
    """

    logging.getLogger(__name__).info('Rendering main page')
    widgets_to_render = {'floating':list(),
                         'top':list(),
                         'left':list(),
                         'right':list(),
                         'bottom':list()}

    for w_id, config in WIDGETS.items():
        logging.getLogger(__name__).debug('Configuring widget %s' % w_id)

        widget_data = dict()

        try:
            widget = get_widget(config.get('core', 'class'))
            widget_data['id'] = w_id
            try:
                widget_data['name'] = config.get('core', 'title')
            except NoOptionError:
                widget_data['name'] = None
            widget_data['data'] = widget.get_data(config)
            widget_data['template_filename'] = widget.get_template_filename()
            widget_data['show_borders'] = config.get('ui', 'show_borders')
            widget_data['layout_mode'] = config.get('position', 'mode')

            position = config.get('position', 'mode')

            if position == 'floating':
                widget_data['pos_x'] = config.get('position', 'x')
                widget_data['pos_y'] = config.get('position', 'y')
            else:
                widget_data['pos_index'] = config.get('position', 'index')

            widgets_to_render[position].append(widget_data)

        # TODO: sorting

        except NoOptionError:
            logging.getLogger(__name__).error('Configuration broken for widget %s' % w_id)

    return render_template('mirror.html', widgets=widgets_to_render)


@app.route('/widget_data/<widget_id>')
def get_json_data(widget_id):
    """
    Gets data for a widget.

    @param widget_id Widget ID given by config file name
    @return JSON formatted widget data
    """

    logging.getLogger(__name__).info('Getting data for widget %s' % widget_id)

    widget_class = WIDGETS[widget_id].get('core', 'class')
    widget = get_widget(widget_class)
    data = widget.get_data(WIDGETS[widget_id])

    return jsonify(data)
