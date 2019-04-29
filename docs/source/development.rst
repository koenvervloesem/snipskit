###########
Development
###########

You can find the SnipsKit code `on GitHub`_.

.. _`on GitHub`: https://github.com/koenvervloesem/snipskit

***********************************
Set up your development environment
***********************************

If you want to start developing on SnipsKit, `fork`_ the repository, clone your fork and install the project's (development) dependencies in a Python virtual environment:

.. code-block:: sh

    git clone https://github.com/<your_username>/snipskit.git
    cd snipskit
    python3 -m venv venv
    source venv/bin/activate
    pip install wheel
    pip install -r requirements/install/all.txt
    pip install -r requirements/development.txt

.. _`fork`: https://help.github.com/en/articles/fork-a-repo

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
- Create a `pull request`_ from your fork.
- Investigate the output of the Continuous Integration checks and fix any errors you have introduced (you can find badges with an overview of these checks `on GitHub`_):

  - The Travis CI `build status`_ should be "passing".
  - The Code Climate `maintainability`_ should not decrease.
  - The Code Climate `test coverage`_ should not decrease.
  - The Codacy `code quality`_ should not decrease.
  - The `documentation`_ on Read The Docs should be "passing".

.. _`issue tracker`: https://github.com/koenvervloesem/snipskit/issues

.. _`pull request`: https://help.github.com/en/articles/creating-a-pull-request-from-a-fork

.. _`build status`: https://travis-ci.com/koenvervloesem/snipskit

.. _`maintainability`: https://codeclimate.com/github/koenvervloesem/snipskit/maintainability

.. _`test coverage`: https://codeclimate.com/github/koenvervloesem/snipskit/test_coverage

.. _`code quality`: https://www.codacy.com/app/koenvervloesem/snipskit

.. _`documentation`: https://snipskit.readthedocs.io/en/latest/?badge=latest

*****************
Things to work on
*****************

Have a look at the issues in the `issue tracker`_, especially the following categories:

- `help wanted`_: Issues that could use some extra help.
- `good first issue`_: Issues that are good for newcomers to the project.

.. _`help wanted`: https://github.com/koenvervloesem/snipskit/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22

.. _`good first issue`: https://github.com/koenvervloesem/snipskit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22

You can also look at the `maintainability`_ issues on Code Climate and the `code quality`_ issues on Codacy. However, note that not all these issues are relevant.

************************
License of contributions
************************

By submitting patches to this project, you agree to allow them to be redistributed under the project's :doc:`LICENSE` according to the normal forms and usages of the open-source community.

It is your responsibility to make sure you have all the necessary rights to contribute to the project.
