Widget Documentation
====================

The following configuration options apply to all widgets:

- ```core```
  - ```class```: Name of class for widget (see below)
  - ```update_time```: Time interval (in seconds) to update the widget after
  - ```title```: Title to be shown above widget
- ```ui```
  - ```width```: Width to allocate to widget
  - ```show_borders```: If borders should be shown around widget
- ```position```
  - ```type```: Type of layout to use, possible values: ```floating```, ```top```, ```left```, ```right```, ```bottom```
  - ```index```: Relative position of widget when using a layout bar (i.e. not ```floating```)
  - ```x```: Position of widget from left hand side (when using ```floating```)
  - ```y```: Position of widget from top (when using ```floating```)
- ```widget```
  - This is used for widget specific config options (see below)

Widgets
-------

The following is a list of all widgets currently added to the framework and their configuration options.

- Digital Clock
  - Class name: ```DigitalClock```
  - Must set ```core/update_time``` to ```1```
  - ```timezone```: A time zone to set the clock to (e.g. ```US/Eastern```)
- Analog Clock
  - Class name: ```AnalogClock```
  - Must set ```core/update_time``` to ```1```
  - Must set ```ui/width``` to ```200```
  - ```timezone```: A time zone to set the clock to (e.g. ```US/Eastern```)
- Text Calendar
  - Class name: ```TextCalendar```
  - Must set ```core/update_time``` to ```1```
  - ```timezone```: A time zone to set the calendar to (e.g. ```US/Eastern```)
- Weather
  - Class name: ```Weather```
  - ```location```: Location for weather status (e.g. ```London, UK```)
- RSS feed
  - Class name: ```RSSFeed```
  - ```feed_url```: URL for RSS feed
- RSS ticker
  - Class name: ```RSSTicker```
  - ```feed_url```: URL for RSS feed
  - ```text_type```: Text to be shown (either ```title``` or ```summary```)
  - ```ticker_update_time```: Time (in seconds) to change the shown text after
