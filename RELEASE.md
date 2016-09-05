NREWebService Releasing Guide
=============================

Follow the steps in this guide to roll a release of NRE Web Services.

1. Check the CHANGELOG.md file and make sure all changes since the last release are included.
2. Check the current development version is consistent with semantic versioning and the changes
   since the last release.
3. Check the tests pass by running ```py.test```.
4. Bump the version and make the release tag: ```bumpversion release```.
5. Check the version bumping commit and tag all look OK.
6. Remove any previous build artifacts: ```python setup.py clean```.
6. Build the release: ```python setup.py sdist bdist_wheel```.
7. Upload the release to PyPI: ```twine upload dist/nrewebservices*```.
8. Bump the version for the next development version: ```bumpversion patch --no-tag```.
9. Check the version bumping commit looks OK and no tag was created.
10. Push the master branch and release tag to github: ```git push origin master --tags```.


