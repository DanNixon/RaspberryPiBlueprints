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
    MIDI_DIRECTORY='/home/dan/midi_temp',
    DEFAULT_BPM=60
))
app.config.from_envvar('BOTTLE_XYLOPHONE_SETTINGS', silent=True)


log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), None)
logging.basicConfig(level=log_level, filename=app.config['LOG_FILE'])


player = None
playback_bpm = app.config['DEFAULT_BPM']


@app.route('/')
def show_home():
    # Get a list of all MIDI files in the save directory
    midi_files = [ f for f in os.listdir(app.config['MIDI_DIRECTORY']) if f.endswith('.mid')]

    return render_template('home.html', midi_files=midi_files, tempo=playback_bpm)


@app.route('/upload_midi', methods=['POST'])
def upload_midi():
    # Get the MIDI file
    midi_file = request.files['uploaded_midi_file']

    # Check it is of the correct type (or at least has the .mid extension)
    if midi_file and midi_file.filename.endswith('.mid'):
        # Save the file to the save directory
        filename = secure_filename(midi_file.filename)
        midi_file.save(os.path.join(app.config['MIDI_DIRECTORY'], filename))
        flash('Uploaded MIDI file: %s' % filename)
    else:
        flash('MIDI file upload failed')

    return redirect(url_for('show_home'))


@app.route('/play_note/<int:midi_note>')
def play_note(midi_note):
    global player

    # Create a new player if needed
    if player is None:
        player = MIDIPlayer(app.config)

    # Use the player to play a single note
    player.play_note(int(midi_note), 50)


@app.route('/play/<path:midi_file>')
def play_midi_file(midi_file):
    global player

    # Create a new player if needed
    if player is None:
        player = MIDIPlayer(app.config)
        player.set_bpm(playback_bpm)

    # Set filename and start playing in seperate thread
    player.set_midi_file(midi_file)
    player.start()

    flash('Playing MIDI file: %s' % midi_file)
    return redirect(url_for('show_home'))


@app.route('/stop')
def stop_playback():
    global player

    # Nothing to do if there is no player
    if player is None:
        return redirect(url_for('show_home'))

    # Stop player thread
    player.stop()
    player = None

    flash('Playback stopped')
    return redirect(url_for('show_home'))


@app.route('/delete/<path:midi_file>')
def delete_midi_file(midi_file):
    # Deletes a MIDI file from the save directory
    filename = os.path.join(app.config['MIDI_DIRECTORY'], midi_file)
    os.remove(filename)

    flash('Deleted MIDI file: %s' % midi_file)
    return redirect(url_for('show_home'))


@app.route('/set_bpm')
def set_bpm():
    global playback_bpm

    playback_bpm = int(request.args.get('bpm_value'))

    if player is not None:
        player.set_bpm(playback_bpm)

    flash('BPM set to %d' % playback_bpm)
    return redirect(url_for('show_home'))
