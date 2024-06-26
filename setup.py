import os

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='nrewebservices',
    version='0.2.2-dev',
    packages=find_packages(),
    description='A Python 3 library for accessing the National Rail Enquiries web service APIs.',
    long_description=(read('README.rst')),
    url='https://github.com/grundleborg/nrewebservices',
    license='BSD',
    author='George Goldberg',
    author_email='george@gberg.me',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[ read('requirements.txt').split('\n') ],
)
