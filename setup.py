import sys
from setuptools import setup, find_packages

import bandit


argv = sys.argv[1:]
TEST = len(argv) and argv[0] in ('test', 'nosetests')

setup_requires = []
test_requires = [
  'nose>=1.2.1',
  'unittest2==0.5.1',
  'mock>=0.8.0',
]
requires = []

setup(name='bandit',
      version=bandit.__version__,
      description="Bandit",
      author="George Courtsunis",
      author_email="gjcourt@gmail.com",
      packages=find_packages(),
      install_requires=requires,
      setup_requires=setup_requires,
      )

