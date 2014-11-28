# -*- coding: utf-8 -*-
"""
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template


app = Flask(__name__)
app.config.update(dict(DEBUG=True))


@app.route('/')
def show_control():
    return render_template('control.html')

@app.route('/control_w_video')
def show_control_with_video():
    return render_template('control_w_video.html')

@app.route('/video')
def show_video():
    return render_template('video.html')
