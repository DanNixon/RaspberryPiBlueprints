Magic Mirror Web Framework
==========================

Widget Layout
-------------

The viewport is divided up into four bars two spanning the width of the viewport at the top and bottom of the viewport and two spanning the distance between the top and bottom bars at the left and right of the viewport.

Widgets can be assigned an order in a bar or given an arbitrary position anywhere on the viewport given a position relative to the top left of the viewport.

Widget Development
------------------

A widget should have:

 - A server side (Python) script file (```widgets/CLASSNAME.py```)
 - A Jinja style template file (```templates/widgets/CLASSNAME.html```)
 - A CSS file (```static/widgets/CLASSNAME/style.css```)
 - A client side (JS/jQuery) script file (```static/widgets/CLASSNAME/script.js```)

Widget classes in Python must inherit from ```AbstractWidget``` and (if needed) override the ```get_data()``` function, this is used to handle calls to the widget data webservice.

The JS code must define a class containing an ```init()``` and ```update()``` functions, ```init()``` is called when the widget content is ready and ```update()``` is called every ```n``` seconds where ```n``` is given in the deployment config file. Both functions are given the widget content div DOM as a parameter.

There is a webservice accessible at ```/widget_data/[widget ID]``` which returns the result of ```get_data()``` as a JSON formatted map.

Widget Deployment
-----------------

To add a new widget create a new config file and specify the ```core:class``` and ```position``` section properties.

Some widgets also require specific config options which should be places under the ```widget``` section
