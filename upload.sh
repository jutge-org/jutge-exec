#!/bin/bash

echo "Current version: " `grep "version =" setup.py | awk '{print $3}'`

echo -n "New version? "
read version

perl -p -i -e "s/^version = .*/version = '$version'/" setup.py

git commit -a -m "Release $version"
git push
git tag $version -m "Release $version"
git push origin "$version"

pip3 install --upgrade sdist twine setuptools --break-system-packages
python3 setup.py sdist bdist_wheel
python3 -m twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/*
