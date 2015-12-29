"""Setup module.
See:
https://github.com/pypa/
"""
__version__='0.2.dev2'
from setuptools import setup
from os import path

# Get the descriptions from the README file
here = path.abspath(path.dirname(__file__))
my_description='A Pure Python Telegram Bot API library'
try:
	with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
		my_long_description = f.read()
except:
	my_long_description=my_description
	
my_requirements = ['requests']
	
setup(
    name='PyTBot',
	version=__version__,
	description=my_description,
    long_description=my_long_description,
	# The project's main homepage.
    url='https://github.com/RRostami/PyTBot',
	
	classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
		'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',

        # Pick your license as you wish (should match "license" )
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.

        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
	keywords='Telegram Bot api',
	license='MIT',
	
	packages=['PyTBot'],
	install_requires=my_requirements,
	author='Ramtin Rostami',
	author_email='ramtinrostami@gmail.com'
	)