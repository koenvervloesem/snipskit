import os
import sys

try:
    # This environment variable is used by Travis CI to define which
    # dependencies are installed. Pytest uses it to define which modules
    # are checked.
    requirements = os.environ['SNIPSKIT_REQUIREMENTS']

    if requirements == 'common':
        collect_ignore = ['mqtt', 'hermes']
    elif requirements == 'mqtt':
        collect_ignore = ['hermes']
    elif requirements == 'hermes':
        collect_ignore = ['mqtt']
    elif requirements == 'all':
    # Run all the tests
        pass
    else:
        sys.exit('Unkown value for SNIPSKIT_REQUIREMENTS environment variable: {}'.format(requirements))
except KeyError:
    # Run all the tests
    pass
