@echo off

call pip install wheel
rm -rf build dist *.egg-info
call python setup.py sdist bdist_wheel

call pip install twine
call python -m twine upload dist/* --verbose
