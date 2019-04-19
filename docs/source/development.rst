###########
Development
###########

You can find the SnipsKit code `on GitHub`_.

.. _`on GitHub`: https://github.com/koenvervloesem/snipskit

If you want to start developing on SnipsKit, get the code and install its (development) dependencies in a Python virtual environment:

.. code-block:: sh

    git clone https://github.com/koenvervloesem/snipskit.git
    cd snipskit
    python3 -m venv venv
    source venv/bin/activate
    pip install wheel
    pip install -r requirements/install/all.txt
    pip install -r requirements/development.txt

A good start to check whether your development environment is set up correctly is to run the unit tests:

.. code-block:: sh

    ./scripts/run_tests.sh
