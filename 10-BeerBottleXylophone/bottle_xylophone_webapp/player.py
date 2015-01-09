import logging, time, os, midi
from threading import Thread, Event


class MIDIPlayer(Thread):
    """
    Class to handle playing MIDI files on a seperate thread.
    """

    logger = logging.getLogger(__name__)


    def __init__(self, configuration):
        Thread.__init__(self)
        self._stop = Event()

        self._servos = self._define_servos(configuration)
        self._init_servos()

        self._midi_file = None
        self._midi_file_dir = configuration['MIDI_DIRECTORY']

        self.set_bpm(120)


    def set_midi_file(self, midi_file):
        """
        Sets the MIDI file to be played.

        @param midi_file MIDI filename
        """

        self._midi_file = os.path.join(self._midi_file_dir, midi_file)

        if not os.path.exists(self._midi_file):
            raise RuntimeError('MIDI file not found')


    def set_bpm(self, bpm):
        """
        Sets the tempo of the playback.

        @param bpm Tempo as beats per minute
        """

        self._tempo = 60 * 1000000 / bpm
        self.logger.info('Set tempo %f for BPM %f' % (self._tempo, bpm))


    def run(self):
        """
        Plays the set MIDI file
        """

        # Read the MIDI file
        pattern = midi.read_midifile(self._midi_file)

        # Get thr resolution of the MIDI file
        self._resolution = pattern.resolution
        self.logger.info('MIDI file resolution: %d' % self._resolution)

        # Calculate the tick duration
        tick_to_seconds = self._tempo / (self._resolution * 1000000.0)
        self.logger.info('Tick time: %f seconds' % tick_to_seconds)

        for event in pattern[1]:
            # Delay for the required amont of time
            delay_seconds = event.tick * tick_to_seconds
            self.logger.debug('Delay before event process: %ds' % delay_seconds)
            time.sleep(delay_seconds)

            # Check if we should stop playback
            if self._stop.isSet():
                return

            # Process a note on message
            if isinstance(event, midi.NoteOnEvent):
                midi_note = event.data[0]
                velocity = event.data[1]
                is_on = velocity > 0
                self._set_note(midi_note, is_on)

            # Process a note off message
            elif isinstance(event, midi.NoteOffEvent):
                midi_note = event.data[0]
                self._set_note(midi_note, False)

        self.logger.info('End of MIDI file')


    def stop(self):
        """
        Stops playback of the MIDI file.
        """

        self._stop.set()


    def play_note(self, midi_note, duration):
        """
        Playes a note for a given time duration.

        @param midi_note MIDI note to play
        @param duration Duration to keep servo in hit position for (in ms)
        """

        self.logger.info('Playing MIDI note %d for %dms' % (midi_note, duration))
        self._set_note(midi_note, True)
        time.sleep(duration / 1000.0)
        self._set_note(midi_note, False)


    def _set_note(self, midi_note, note_on):
        """
        Sets the servo for a not into either the hit or reract position.

        @param midi_note MIDI note to actuate
        @param note_on True for hit position, False for retract position
        """

        servo = self._servos.get(midi_note, None)

        if servo is None:
            self.logger.warning('No servo for MIDI note %d' % midi_note)
            return

        if note_on:
            position = servo['hit_pos']
        else:
            position = servo['retract_pos']

        self._output_servo(servo['gpio'], position)


    def _define_servos(self, configuration):
        """
        Gets all the configured servos form the configuraion file.

        @param configuration Config to get servo data from
        @return Map of MIDI note to servo information
        """

        default_hit = configuration['DEFAULT_HIT']
        self.logger.info('Default hit position: %d' % (default_hit))

        default_retract = configuration['DEFAULT_RETRACT']
        self.logger.info('Default retract position: %d' % (default_retract))

        servos = dict()
        for k, v in configuration.items():
            if k.startswith('MIDI_GPIO_'):
                servo = {'gpio':v}
                servo['midi_note'] = int(k.split('_')[-1:][0])
                servo['hit_pos'] = configuration.get('MIDI_HIT_%d' % servo['midi_note'], default_hit)
                servo['retract_pos'] = configuration.get('MIDI_RETRACT_%d' % servo['midi_note'], default_retract)

                self.logger.info('Parsed servo: %s' % (str(servo)))
                servos[servo['midi_note']] = servo

        return servos


    def _init_servos(self):
        """
        Initilise the servos and set them to theirretracted positions.
        """

        for servo in self._servos.values():
            gpio = servo['gpio']
            # TODO: Init servo
            self._output_servo(gpio, servo['retract_pos'])


    def _output_servo(self, gpio, position):
        """
        Sets a servo to a given posiion.

        @param gpio GPIO to output on
        @param position Timing value denoting position
        """

        self.logger.debug('Setting servo on GPIO %d to %d' % (gpio, position))
        # TODO: Servo output
