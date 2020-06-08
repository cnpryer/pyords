pip install wheel
rm -rf build dist *.egg-info
python setup.py sdist bdist_wheel
pip install twine
python -m twine upload dist/*
