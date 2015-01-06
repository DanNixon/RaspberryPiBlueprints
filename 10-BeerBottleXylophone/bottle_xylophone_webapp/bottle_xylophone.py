# -*- coding: utf-8 -*-

from flask import Flask, render_template


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True
))
app.config.from_envvar('BOTTLE_XYLOPHONE_SETTINGS', silent=True)


@app.route('/')
def show_home():
    return render_template('home.html')
