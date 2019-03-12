"""This module contains exceptions defined for the snipskit library.

Classes:
    :class:`SnipsKitError`: The base class for exceptions in snipskit.

    :class:`AssistantConfigNotFoundError`: Raised when the assistant's
        configuration file is not found.

    :class:`SnipsConfigNotFoundError`: Raised when there's no snips.toml found.
"""


class SnipsKitError(Exception):
    """Base class for exceptions raised by snipskit code."""
    pass


class AssistantConfigNotFoundError(SnipsKitError):
    """Raised when the assistant's configuration is not found in the search
    path.
    """
    pass


class SnipsConfigNotFoundError(SnipsKitError):
    """Raised when there's no snips.toml found in the search path."""
    pass
