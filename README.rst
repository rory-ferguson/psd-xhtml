photoshop_email_generator
==========

``photoshop_email_generator`` is a script to export information from a PSD file and generate html email content.

Requires
------------
Supports Python 3.6.7


Installation
------------
``photoshop_email_generator`` requires the below packages


psd-tools

.. code-block:: bash

    pip install psd-tools

psd-tools2

.. code-block:: bash

    pip install psd-tools2==1.7.30

Pillow

.. code-block:: bash

   pip install Pillow==4.1.1
   
How To
------
The email modules are located as json data inside ``modules.json``

To generate the json file use the `json_generator
<https://github.com/Constuelo/json_generator>`_.

The ``module.py`` file will parse a psds initial group layers and match the names with the ``modules.json`` keys, the html will be initially built from this.

If the text is parsed correctly, it will replace those values in the html.

.. code-block:: bash
   python module.py
