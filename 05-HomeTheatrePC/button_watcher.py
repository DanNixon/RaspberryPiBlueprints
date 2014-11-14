"""
Code to watch buttons attached to GPIO pins using sysfs
abd send remote control signals to XBMC using the HTTP API.
"""

def gpio_export(gpio):
    """
    Exports a GPIO ready to be used.

    @param gpio BCM GPIO number
    """

    with open('/sys/class/gpio/export', 'w') as file:
        file.write(str(gpio))


def gpio_unexport(gpio):
    """
    Unexports a GPIO after use.

    @param gpio BCM GPIO number
    """

    with open('/sys/class/gpio/unexport', 'w') as file:
        file.write(str(gpio))


def set_gpio_mode(gpio, mode, active_low=False):
    """
    Sets the IO mode of a GPIO.

    @param gpio BCM GPIO number
    @param mode IO mode ('in' or 'out')
    @param active_low If the input should be considered active when low
    """

    with open('/sys/class/gpio/gpio%d/direction' % gpio, 'w') as file:
        file.write(str(mode))
    if mode == 'in':
        with open('/sys/class/gpio/gpio%d/active_low' % gpio, 'w') as file:
            if active_low:
                file.write('1')
            else:
                file.write('0')


def get_gpio(gpio):
    """
    Gets the state of a GPIO.

    @param gpio BCM GPIO number
    @returns True for high, False for low
    """

    with open('/sys/class/gpio/gpio%d/value' % gpio, 'r') as file:
        state = file.read()
	return '1' in state


def setup_gpio_buttons(button_map):
    """
    Exports each button GPIO and sets it as an input.

    @param button_map Dict mapping button ID to BCM GPIO number
    """

    for gpio in button_map.values():
        gpio_export(gpio)
        active_low = gpio == 4
        set_gpio_mode(gpio, 'in', active_low)


def poll_all_buttons(button_map):
    """
    Gets the states of each button GPIO.

    @param button_map Dict mapping button ID to BCM GPIO number
    @returns Dict mapping button ID to state
    """

    states = dict()

    for button_id, gpio in button_map.iteritems():
        states[button_id] = get_gpio(gpio)

    return states


import signal
import time

RUN = True

# Time between each button poll
POLL_INTERVAL = 1.0

# DIct mapping button ID to BCM GPIO number
BUTTONS = dict()
BUTTONS['enter'] = 4
BUTTONS['back'] = 9
BUTTONS['up'] = 27
BUTTONS['down'] = 22
BUTTONS['left'] = 10
BUTTONS['right'] = 11


def stop(signal, frame):
    global RUN
    RUN = False


if __name__ == '__main__':
    print 'Setting up GPIO'
    signal.signal(signal.SIGINT, stop)
    setup_gpio_buttons(BUTTONS)

    print 'Running'
    while(RUN):
        print poll_all_buttons(BUTTONS)
        time.sleep(POLL_INTERVAL)

    print 'Exiting'
    for gpio in BUTTONS.values():
        gpio_unexport(gpio)
