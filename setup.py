from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup, find_packages


with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setup(
    name="snipskit",
    version=version,
    description="A library to help create apps for the voice assistant Snips",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    author="Koen Vervloesem",
    author_email="koen@vervloesem.eu",
    url="https://github.com/koenvervloesem/snipskit",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=['hermes_python>=0.3.3', 'paho-mqtt', 'toml'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries'
    ],
)
