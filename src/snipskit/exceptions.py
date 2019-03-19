"""This module contains exceptions defined for the SnipsKit library."""


class SnipsKitError(Exception):
    """Base class for exceptions raised by SnipsKit code.

    By catching this exception type, you catch all exceptions that are
    defined by the SnipsKit library."""


class AssistantConfigNotFoundError(SnipsKitError):
    """Raised when the assistant's configuration is not found in the search
    path.
    """


class SnipsConfigNotFoundError(SnipsKitError):
    """Raised when there's no snips.toml found in the search path."""
