# -*- coding: utf-8 -*-
"""
"""

import importlib, ConfigParser, os
from flask import Flask, render_template, jsonify


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True
))
app.config.from_envvar('MAGIC_MIRROR_SETTINGS', silent=False)


def get_widget_configs(directory):
    configs = dict()

    for name in os.listdir(directory):
        file_path = os.path.join(directory, name)
        if os.path.isfile(file_path):
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

    widget = importlib.import_module('widgets.%s' % widget_class)
    widget_obj = getattr(widget, widget_class)()

    return widget_obj


@app.route('/')
def render_mirror():
    widgets_to_render = list()

    for w_id, config in WIDGETS.items():
        widget_data = dict()
        widget = get_widget(config.get('core', 'class'))
        widget_data['data'] = widget.get_data(config)
        widget_data['name'] = config.get('core', 'title')
        widget_data['id'] = w_id
        widget_data['template_filename'] = widget.get_template_filename()

        widgets_to_render.append(widget_data)

    return render_template('mirror.html', widgets=widgets_to_render)


@app.route('/widget_data/<widget_id>')
def get_json_data(widget_id):
    """
    Gets data for a widget.

    @param widget_id Widget ID given by config file name
    @return JSON formatted widget data
    """

    widget_class = WIDGETS[widget_id].get('core', 'class')
    widget = get_widget(widget_class)
    data = widget.get_data(WIDGETS[widget_id])

    return jsonify(data)
