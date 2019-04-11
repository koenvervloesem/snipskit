#########
Changelog
#########

All notable changes to the SnipsKit project are documented in this file.

The format is based on `Keep a Changelog`_, and this project adheres to the `Semantic Versioning`_ specification with major, minor and patch version.

Given a version number MAJOR.MINOR.PATCH, this project increments the:

- MAJOR version when incompatible API changes are made;
- MINOR version when functionality is added in a backwards-compatible manner;
- PATCH version when backwards-compatible bug fixes are made.

.. warning:: Note that major version zero (0.y.z) is for initial development. Anything may change at any time. The public API should not be considered stable. Before SnipsKit reaches version 1.0.0, the API does not adhere to the above specification, but the minor version is incremented when incompatible API changes are made.

.. _`Keep a Changelog`: https://keepachangelog.com/en/1.0.0/

.. _`Semantic Versioning`: https://semver.org

*************
`Unreleased`_
*************

Added
=====

Changed
=======

Deprecated
==========

Removed
=======

Fixed
=====

Security
========

.. _`Unreleased`: https://github.com/koenvervloesem/snipskit/compare/0.5.4...HEAD

*********************
`0.5.4`_ - 2019-04-11
*********************

Added
=====

- New function :func:`.snipskit.tools.latest_snips_version` that returns the latest version of the Snips platform, as published in the `release notes`_.
- Documented the use of :attr:`.SnipsAppMixin.assistant` to get access to the assistant's configuration outside of an app.

.. _`release notes`: https://docs.snips.ai/additional-resources/release-notes

Fixed
=====

- Removed '/usr/local/etc/assistant/assistant.json' as a default path for :class:`.AssistantConfig`. This was added erroneously in version 0.5.3.

.. _`0.5.4`: https://github.com/koenvervloesem/snipskit/compare/0.5.3...0.5.4

*********************
`0.5.3`_ - 2019-04-11
*********************

Added
=====

- New module :mod:`snipskit.services` with functions to check the versions of Snips services, whether a Snips service is installed or running and what the model version of Snips NLU is.

.. _`0.5.3`: https://github.com/koenvervloesem/snipskit/compare/0.5.2...0.5.3

Fixed
=====

- Added '/usr/local/etc/assistant/assistant.json' as a default path for :class:`.AssistantConfig`. This was meant to fix a bug reported in `issue #4`_.

.. _`issue #4`: https://github.com/koenvervloesem/snipskit/issues/4

*********************
`0.5.2`_ - 2019-04-09
*********************

Added
=====

- New module :mod:`snipskit.mqtt.dialogue` with helper functions :func:`snipskit.mqtt.dialogue.continue_session` and :func:`snipskit.mqtt.dialogue.end_session` to continue and end a session.

.. _`0.5.2`: https://github.com/koenvervloesem/snipskit/compare/0.5.1...0.5.2

*********************
`0.5.1`_ - 2019-04-09
*********************

Fixed
=====

- Example code in documentation fixed to use the new callback signature for methods of :class:`.MQTTSnipsComponent`.
- PyPi package was built incorrectly.

.. _`0.5.1`: https://github.com/koenvervloesem/snipskit/compare/0.5.0...0.5.1

*********************
`0.5.0`_ - 2019-04-08
*********************

Added
=====

- Example code and documentation about accessing the app's configuration, the assistant's configuration and the configuration of Snips.
- Method :meth:`.MQTTSnipsComponent.publish` to publish a payload, optionally encoded as JSON.

Changed
=======

- Breaking change: The callback signature for methods of :class:`.MQTTSnipsComponent` has changed to (self, topic, payload).
- Breaking change: the decorator :func:`.snipskit.mqtt.decorators.topic` now has an optional argument 'json_decode' to decode a JSON payload to a dict, which is True by default.

.. _`0.5.0`: https://github.com/koenvervloesem/snipskit/compare/0.4.0...0.5.0

*********************
`0.4.0`_ - 2019-03-25
*********************

Added
=====

- Support for Python 3.7.
- Extra documentation about installation and usage.

Changed
=======

- Breaking change: Moved all Hermes Python-related classes to :mod:`snipskit.hermes` submodules and all MQTT-related classes to :mod:`snipskit.mqtt` submodules.
- Breaking change: Class :class:`.SnipsConfig` uses the new class :class:`.MQTTConfig` for its MQTT connection settings so it doesn't depend on Hermes Python.
- Breaking change: Use `pip install snipskit[hermes]` to install the Hermes Python dependency, and `pip install snipskit[mqtt]` to install the Paho MQTT dependency. This way you can use the :mod:`snipskit.hermes` module without pulling in the Paho MQTT dependency, or the :mod:`snipskit.mqtt` module without pulling in the Hermes Python dependency. 

.. _`0.4.0`: https://github.com/koenvervloesem/snipskit/compare/0.3.0...0.4.0

*********************
`0.3.0`_ - 2019-03-22
*********************

Added
=====

- Extra documentation about installation and usage.
- Example code in directory `examples`.
- Script `scripts/check_examples.sh` to check example code with pylint.

Changed
=======

- Breaking change: Refactored :class:`.SnipsAppMixin`. Drop :meth:`.SnipsAppMixin.get_assistant` method, add constructor.

.. _`0.3.0`: https://github.com/koenvervloesem/snipskit/compare/0.2.0...0.3.0

*********************
`0.2.0`_ - 2019-03-17
*********************

Added
=====

- Changelog.
- Examples in documentation.

Changed
=======

- Breaking change: Divided :mod:`snipskit.decorators` module into two submodules: :mod:`snipskit.decorators.hermes` and :mod:`snipskit.decorators.mqtt`.

Fixed
=====

- Cleaned up API documentation.

.. _`0.2.0`: https://github.com/koenvervloesem/snipskit/releases/tag/0.2.0

******************
0.1.0 - 2019-03-16
******************

Added
=====

- This is the first version with a 'semi-stable' API.
