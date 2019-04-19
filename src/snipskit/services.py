"""This module contains some functions related to Snips services."""

from psutil import process_iter, NoSuchProcess
import re
from subprocess import check_output

SNIPS_SERVICES = ['snips-analytics', 'snips-asr', 'snips-asr-google',
                  'snips-audio-server', 'snips-dialogue', 'snips-hotword',
                  'snips-injection', 'snips-nlu', 'snips-skill-server',
                  'snips-tts']
VERSION_FLAG = '--version'


def _state(state_function):
    """Return a dict with the state of all Snips Services.

    Args:
        state_function: A function that returns a state for a Snips service.

    Returns:
        dict: A dict with all Snips services as keys and their state as value.
    """
    states = [state_function(service) for service in SNIPS_SERVICES]
    return dict(zip(SNIPS_SERVICES, states))


def _version_output(service):
    """Return the output of the command `service` with the argument
    '--version'.

    Args:
        service (str): The service to check the version of.

    Returns:
        str: The output of the command `service` with the argument
        '--version', or an empty string if the command is not installed.

    Example:

        >>> _version_output('snips-nlu')
        'snips-nlu 1.1.2 (0.62.3) [model_version: 0.19.0]'
    """
    try:
        version_output = check_output([service,
                                       VERSION_FLAG]).decode('utf-8').strip()

    except FileNotFoundError:
        version_output = ''

    return version_output


def is_installed(service):
    """Check whether the Snips service `service` is installed.

    Args:
        service (str): The Snips service to check.

    Returns:
        bool: True if the service is installed; False otherwise.

    Example:

        >>> is_installed('snips-nlu')
        True
    """
    return bool(_version_output(service))


def is_running(service):
    """Check whether the Snips service `service` is running.

    Args:
        service (str): The Snips service to check.

    Returns:
        bool: True if the service is running; False otherwise.

    Example:

        >>> is_running('snips-nlu')
        True
    """
    service_found = False
    for process in process_iter():
        try:
            if service == process.name():
                service_found = True
                break
        except NoSuchProcess:  # Happens when the process no longer exists.
            pass

    return service_found


def model_version():
    """Return the model version of Snips NLU.

    Returns:
        str: The model version of Snips NLU, or an empty string if snips-nlu
        is not installed.

    Example:

        >>> model_version()
        '0.19.0'
    """
    version_output = _version_output('snips-nlu')
    try:
        model_version = re.search(r'\[model_version: (.*)\]',
                                  version_output).group(1)
    except (AttributeError, IndexError):
        model_version = ''

    return model_version


def installed():
    """Return a dict with the installation state of all Snips services.

    Returns:
        dict: A dict with all Snips services as keys and their installation
        state (True or False) as value.
    """
    return _state(is_installed)


def running():
    """Return a dict with the running state of all Snips services.

    Returns:
        dict: A dict with all Snips services as keys and their running state
        (True or False) as value.
    """
    return _state(is_running)


def versions():
    """Return a dict with the version numbers of all Snips services.

    Returns:
        dict: A dict with all Snips services as keys and their version numbers
        as value. Services that are not installed have an empty string as their
        value.
    """
    return _state(version)


def version(service=None):
    """Return the version number of a Snips service or the Snips platform.

    If the `service` argument is empty, this returns the minimum value of the
    version numbers of all installed Snips services.

    Args:
        service (str, optional): The Snips service to check.

    Returns:
        str: The version number of the Snips service or an empty string if the
        service is not installed. If no `service` argument is given: the
        version of the Snips platform or an empty string if no Snips services
        are installed.

    Examples:

        >>> version()
        '1.1.2'
        >>> version('snips-nlu')
        '1.1.2'
    """
    if service:
        try:
            return _version_output(service).split()[1]
        except IndexError:
            # The version output is empty, so the service is not installed.
            return ''
    else:
        # Filter the empty versions and then compute the minimum value.
        return min([version for version in versions().values() if version])
