# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_pbs', 'python_pbs.extensions.pbs']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=69.0.3,<70.0.0']

setup_kwargs = {
    'name': 'python-pbs',
    'version': '0.1.0',
    'description': 'Modern Python wrapper around OpenPBS',
    'long_description': '# python-pbs\nModern python wrapper for OpenPBS\n',
    'author': 'Dax Harris',
    'author_email': 'dharr@lle.rochester.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}
from make import *
build(setup_kwargs)

setup(**setup_kwargs)
