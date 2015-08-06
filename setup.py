from setuptools import setup, find_packages

setup(
    name='av-control',
    version='0.93',
    description='User interface for controlling the A/V devices at St Aldates church',
    author='James Muscat',
    author_email='jamesremuscat@gmail.com',
    url='https://github.com/staldates/av-control',
    install_requires=['avx>=0.93', 'PySide', 'mock', 'nose', 'nose-xcover'],
    dependency_links = [
        "lib/" # find local copies of packages here
        ],
    packages=find_packages('src', exclude=["*.tests"]),
    package_dir = {'':'src'},
      )