# -*- coding: utf-8 -*-

import os, logging
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug import secure_filename
from player import MIDIPlayer


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='key',
    LOG_LEVEL='DEBUG',
    LOG_FILE='midi_bottles.log',
    MIDI_DIRECTORY='/home/dan/midi_temp'
))
app.config.from_envvar('BOTTLE_XYLOPHONE_SETTINGS', silent=True)


log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), None)
logging.basicConfig(level=log_level, filename=app.config['LOG_FILE'])


player = MIDIPlayer(app.config)


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


@app.route('/play_note/<midi_note>')
def play_note(midi_note):
    player.play_note(int(midi_note), 50)
    flash('Playing MIDI note: %s' % midi_note)
    return redirect(url_for('show_home'))


@app.route('/play/<midi_file>')
def play_midi_file(midi_file):
    # TODO
    flash('Playing MIDI file: %s' % midi_file)
    return redirect(url_for('show_home'))


@app.route('/stop')
def stop_playback():
    # TODO
    flash('Playback stopped')
    return redirect(url_for('show_home'))
