@echo off

rm -rf build dist *.egg-info
call python setup.py sdist bdist_wheel
call python -m twine upload dist/* --verbose