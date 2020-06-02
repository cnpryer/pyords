from setuptools import setup, find_packages
from pyords import __version__


long_description = ''
with open('./README.md') as f:
    long_description = f.read()

install_requires = []
with open('./requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='pyords',
    version=__version__,
    description='A python package for operations research and data science problems.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/christopherpryer/pyords',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points ={ 
            'console_scripts': [ 
                'pyords = pyords:cli'
            ] 
        },
    zip_safe=False)