###########
Development
###########

You can find the SnipsKit code `on GitHub`_.

.. _`on GitHub`: https://github.com/koenvervloesem/snipskit

***********************************
Set up your development environment
***********************************

If you want to start developing on SnipsKit, get the code and install its (development) dependencies in a Python virtual environment:

.. code-block:: sh

    git clone https://github.com/koenvervloesem/snipskit.git
    cd snipskit
    python3 -m venv venv
    source venv/bin/activate
    pip install wheel
    pip install -r requirements/install/all.txt
    pip install -r requirements/development.txt

******************
Run the unit tests
******************

A good start to check whether your development environment is set up correctly is to run the unit tests:

.. code-block:: sh

    ./scripts/run_tests.sh

It's good practice to run the unit tests before and after you work on something.

*********************
Development practices
*********************

- Before starting significant work, please propose it and discuss it first on the `issue tracker`_ on GitHub. Other people may have suggestions, will want to collaborate and will wish to review your code.
- Please work on one piece of conceptual work at a time. Keep each narrative of work in a different branch.
- As much as possible, have each commit solve one problem.
- A commit must not leave the project in a non-functional state.
- Run the unit tests before you create a commit.
- Treat code, tests and documentation as one.

.. _`issue tracker`: https://github.com/koenvervloesem/snipskit/issues

*****************
Things to work on
*****************

Have a look at the issues in the `issue tracker`_, especially the following categories:

- `help wanted`_: Issues that could use some extra help.
- `good first issue`_: Issues that are good for newcomers to the project.

.. _`help wanted`: https://github.com/koenvervloesem/snipskit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22

.. _`good first issue`: https://github.com/koenvervloesem/snipskit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22

************************
License of contributions
************************

By submitting patches to this project, you agree to allow them to be redistributed under the project's :doc:`LICENSE` according to the normal forms and usages of the open-source community.

It is your responsibility to make sure you have all the necessary rights to contribute to the project.
