#!/bin/bash

rm -rf build dist *.egg-info
python3 setup.py sdist bdist_wheel
pip3 install twine
python3 -m twine upload dist/*