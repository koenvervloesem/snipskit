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

However, in many projects you don't need the complete functionality. Then you have the following options to prevent pulling in unnecessary dependencies:

The hermes module
=================

If you don't need the :mod:`snipskit.mqtt` module because you're using the :mod:`snipskit.hermes` module, install the SnipsKit library like this:

.. code-block:: sh

    pip3 install snipskit[hermes]

This will install the complete library and the following dependencies:

.. literalinclude:: ../../requirements/install/hermes.txt

The mqtt module
===============

If you don't need the :mod:`snipskit.hermes` module because you're using the :mod:`snipskit.mqtt` module, install the SnipsKit library like this:

.. code-block:: sh

    pip3 install snipskit[mqtt]

This will install the complete library and the following dependencies:

.. literalinclude:: ../../requirements/install/mqtt.txt

Only the basic modules
======================

If you only need the basic modules because you don't need the :mod:`snipskit.hermes` and :mod:`snipskit.mqtt` modules, install the SnipsKit library like this:

.. code-block:: sh

    pip3 install snipskit

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

****************
Requirements.txt
****************

Because the public API of SnipsKit should not be considered stable yet, it's best to define a specific version (major.minor.patch) in the `requirements.txt` file of your project, e.g.:

.. code-block:: none

    snipskit[hermes]==0.5.3

Then you can install the specified version with:

.. code-block:: sh

    pip3 install -r requirements.txt

Alternatively, you can define a version like:

.. code-block:: none

    snipskit[hermes]~=0.5.0

This will install the latest available SnipsKit version compatible with 0.5.0, but not a higher version such as 0.6.0. Because the minor version is incremented when incompatible API changes are made, this prevents your code from breaking because of breaking changes in the SnipsKit API. Have a look at the :doc:`CHANGELOG` for the versions and their changes.
