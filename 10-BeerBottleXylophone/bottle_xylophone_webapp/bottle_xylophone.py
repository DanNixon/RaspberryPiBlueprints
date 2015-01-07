# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug import secure_filename


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='key',
    MIDI_DIRECTORY='/home/dan/midi_temp'
))
app.config.from_envvar('BOTTLE_XYLOPHONE_SETTINGS', silent=True)


@app.route('/')
def show_home():
    return render_template('home.html')


@app.route('/upload_midi', methods=['POST'])
def upload_midi():
    file = request.files['uploaded_midi_file']

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['MIDI_DIRECTORY'], filename))

        flash('Uploaded MIDI file: %s' % filename)
        return redirect(url_for('show_home'))
