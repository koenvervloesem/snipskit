############
Installation
############

*******************
System requirements
*******************

.. include:: ../../README.rst
   :start-after: inclusion-marker-start-requirements
   :end-before: inclusion-marker-end-requirements

SnipsKit requires the following Python packages if you want to use the complete functionality:

.. literalinclude:: ../../requirements/install.txt

If your platform supports these packages, SnipsKit should also be supported.

****************
Install SnipsKit
****************

.. include:: ../../README.rst
   :start-after: inclusion-marker-start-installation
   :end-before: inclusion-marker-end-installation

This will also install its dependencies.

It is recommended to use a `virtual environment`_ and activate it before installing SnipsKit in order to manage your project dependencies properly. You can create a virtual environment with the name `venv` in the current directory and activate it like this:

.. code-block:: sh

    python3 -m venv venv
    source venv/bin/activate

After this, you can install SnipsKit in the virtual environment.

.. _`virtual environment`: https://docs.python.org/3/library/venv.html
