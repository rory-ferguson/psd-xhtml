photoshop_email_generator
==========

``photoshop_email_generator`` exports layer and text information from a photoshop file to generate html email content.

This library is complemented by an automated image extractor `photoshop_email_image_exporter
<https://github.com/Constuelo/photoshop_email_image_exporter>`_.


Requires
------------
Supports Python 3.6.7


Installation
------------
``photoshop_email_generator`` requires the below packages

`psd-tools2
<https://github.com/kyamagu/psd-tools2>`_

.. code-block:: bash

    pip install psd-tools2==1.8.5



Example Directory
-----------------
Move the ``modules.json`` from ``examples/`` into the parent directory.

Use the ``examples/`` to test with.


How To
------
The email modules are located as json data inside ``modules.json``

To generate the json file use the `json_generator
<https://github.com/Constuelo/json_generator>`_.

The ``module.py`` file will parse a psds initial group layers and match the names with the ``modules.json`` key/values, the html will be initially built from this.

If the psd text is parsed correctly, it will replace those values in the html.

.. code-block:: bash
   python module.py
   

Notes for work
--------------
Remove <br class="d_h" /> in modules.json

Replace &nbsp;&gt; with ' >' in modules.json
