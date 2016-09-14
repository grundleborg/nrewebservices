------------------------------
NREWebServices Releasing Guide
------------------------------

Follow the steps in this guide to roll a new release of NRE Web Services.

#. Check the `CHANGELOG <https://github.com/grundleborg/nrewebservices/blob/master/CHANGELOG.rst>`_
   and make sure all changes since the last release are included.
#. Check the current development version is consistent with semantic versioning and the changes
   since the last release. If not, use bumpversion with the appropriate parameter below to set the
   development version below, e.g. to bump the minor release number:
   ::

        bumpversion minor --no-tag

#. Check the tests pass:
   ::

        py.test

#. Bump the version and make the release tag:
   ::

        bumpversion release


#. Check the version bumping commit and tag all look OK.
#. Remove any previous build artifacts:
   ::
   
        python setup.py clean

#. Build the release:
   ::
   
        python setup.py sdist bdist_wheel

#. Upload the release to PyPI:
   ::
   
        twine upload dist/nrewebservices

#. Bump the version for the next development version:
   ::
   
        bumpversion patch --no-tag

#. Check the version bumping commit looks OK and no tag was created.
#. Push the master branch and release tag to github:
   ::
   
        git push origin master --tags


