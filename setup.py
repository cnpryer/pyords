from setuptools import setup

long_description = ''
with open('./README.md') as f:
    long_description = f.read()

setup(name='fyords',
    version='0.1',
    description='A library for operations research, data science, and financial engineering.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/christopherpryer/fyords',
    author='Chris Pryer',
    author_email='christophpryer@gmail.com',
    license='PUBLIC',
    packages=['fyords'],
    zip_safe=False)
