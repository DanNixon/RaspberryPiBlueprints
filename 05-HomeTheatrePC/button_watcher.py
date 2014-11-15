"""
Code to watch buttons attached to GPIO pins using sysfs
and send remote control signals to XBMC using the HTTP API.
"""

import json
import signal
import time
import urllib2


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

    @param button_map Dict defining buttons
    """

    for button in button_map.values():
        gpio_export(button[0])
        active_low = button[0] == 4
        set_gpio_mode(button[0], 'in', active_low)


def poll_all_buttons(button_map):
    """
    Gets the states of each button GPIO.

    @param button_map Dict defining buttons
    @returns Dict mapping button ID to state
    """

    states = dict()

    for button_id, button in button_map.iteritems():
        states[button_id] = get_gpio(button[0])

    return states


def send_command(command):
    """
    Sends a command to XBMC instance on localhost.

    @param command Command to send
    """

    data = {'jsonrpc':'4.0', 'method': command}

    request = urllib2.Request('http://127.0.0.1:80/jsonrpc')
    request.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(request, json.dumps(data))


def stop(signal, frame):
    """
    Signal handler to stop the watcher.

    @param signal Signal received
    @param frame Unused
    """

    print 'Got signal %d, will exit.' % signal

    global RUN
    RUN = False


RUN = True

# Time between each button poll
POLL_INTERVAL = 0.1

# Dict defining buttons by BCM GPIO number and XBMC command
BUTTONS = dict()
BUTTONS['enter']  = (4,  'Input.Select')
BUTTONS['back']   = (9,  'Input.Back')
BUTTONS['up']     = (27, 'Input.Up')
BUTTONS['down']   = (22, 'Input.Down')
BUTTONS['left']   = (10, 'Input.Left')
BUTTONS['right']  = (11, 'Input.Right')


if __name__ == '__main__':
    print 'Setting up GPIO'
    signal.signal(signal.SIGINT, stop)
    setup_gpio_buttons(BUTTONS)

    print 'Running'

    # Get the initial button state
    last_button_state = poll_all_buttons(BUTTONS)

    while(RUN):
        # Get the current button state
        current_button_state = poll_all_buttons(BUTTONS)

        # Check for any pressed buttons
        for button_id in BUTTONS.keys():
            current = current_button_state[button_id]
            last = last_button_state[button_id]

            # If button was pressed
            if current and not last:
                print '%s pressed' % button_id

                # Handle it
                send_command(BUTTONS[button_id][1])

        # Set the last known state to the last poll
        last_button_state = current_button_state

        time.sleep(POLL_INTERVAL)

    print 'Exiting'
    for button in BUTTONS.values():
        gpio_unexport(button[0])
