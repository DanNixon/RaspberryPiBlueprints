# -*- coding: utf-8 -*-
"""
"""

import importlib
from flask import Flask, render_template, jsonify


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True
))
app.config.from_envvar('MAGIC_MIRROR_SETTINGS', silent=True)


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

    demo = dict()
    demo_obj = get_widget('DemoWidget')
    demo['data'] = demo_obj.get_data(app.config)
    demo['name'] = demo_obj.name()
    demo['id'] = demo_obj.string_id()
    demo['template_filename'] = demo_obj.get_template_filename()
    widgets_to_render.append(demo)

    return render_template('mirror.html', widgets=widgets_to_render)


@app.route('/<widget_class>')
def get_json_data(widget_class):
    """
    Gets data for a widget.

    @param widget_class Name of widget class
    @return JSON formatted widget data
    """

    widget = get_widget(widget_class)
    data = widget.get_data(app.config)

    return jsonify(data)
