from setuptools import setup
from fyords import __version__

long_description = ''
with open('./README.md') as f:
    long_description = f.read()

setup(name='fyords',
    version=__version__,
    description='A library for operations research, data science, and financial engineering.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/christopherpryer/fyords',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=['fyords'],
    zip_safe=False)
