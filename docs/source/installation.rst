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

.. literalinclude:: ../../requirements/install/all.txt

If your platform supports these packages, SnipsKit should also be supported.

****************
Install SnipsKit
****************

.. include:: ../../README.rst
   :start-after: inclusion-marker-start-installation
   :end-before: inclusion-marker-end-installation

This will also install its dependencies:

.. literalinclude:: ../../requirements/install/all.txt

However, in many projects you don't need the complete functionality. Then you have the following options:

The hermes module
=================

If you don't need the :mod:`snipskit.mqtt` module because you're using the :mod:`snipskit.hermes` module, install the SnipsKit library like this:

.. code-block:: sh

    pip install snipskit[hermes]

This will install the complete library and the following dependencies:

.. literalinclude:: ../../requirements/install/hermes.txt

The mqtt module
===============

If you don't need the :mod:`snipskit.hermes` module because you're using the :mod:`snipskit.mqtt` module, install the SnipsKit library like this:

.. code-block:: sh

    pip install snipskit[mqtt]

This will install the complete library and the following dependencies:

.. literalinclude:: ../../requirements/install/mqtt.txt

Only the basic modules
======================

If you only need the basic modules because you don't need the :mod:`snipskit.hermes` and :mod:`snipskit.mqtt` modules, install the SnipsKit library like this:

.. code-block:: sh

    pip install snipskit

This will install the complete library and the following dependencies:

.. literalinclude:: ../../requirements/install/common.txt

********************
Virtual environments
********************

It is recommended to use a `virtual environment`_ and activate it before installing SnipsKit in order to manage your project dependencies properly. You can create a virtual environment with the name `venv` in the current directory and activate it like this:

.. code-block:: sh

    python3 -m venv venv
    source venv/bin/activate

After this, you can install SnipsKit in the virtual environment.

.. _`virtual environment`: https://docs.python.org/3/library/venv.html
