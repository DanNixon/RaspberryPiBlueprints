import logging, time
from threading import Thread


class MIDIPlayer(Thread):

    logger = logging.getLogger(__name__)


    def __init__(self, configuration):
        Thread.__init__(self)
        self._servos = self._define_servos(configuration)
        self._init_servos()

        self._midi_file = None


    def set_midi_file(self, midi_file):
        """
        Sets the MIDI file to be played.

        @param midi_file MIDI filename
        """

        self._midi_file = midi_file


    def run(self):
        """
        """

        pass


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
        @param note_on True for hit position, Flase or retract position
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
