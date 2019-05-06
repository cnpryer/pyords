from setuptools import setup

long_description = ''
with open('./README.md') as f:
    long_description = f.read()

setup(name='pryords',
    version='0.1',
    description='A library for operations research and data science.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/christopherpryer/pryords',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=['pryords'],
    zip_safe=False)
