from setuptools import setup, find_packages
import sys, os

version = '.1'

setup(name='auto-discover',
      version=version,
      description="A network discovery tool that uses nmap to identify if ssh,ping, and snmp are running on",
      long_description=('\\n'
                        'various connected devices in a network.'),
      classifiers=['Programming Language :: Python :: 2 :: Only, Topic :: System :: Systems Administration, Topic :: System :: Monitoring, '],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='nmap,portscanner,network,sysadmin',
      author='Thomas Vincent',
      author_email='thomasvincent@gmail.com',
      url='https://github.com/thomasvincent/python-auto-discover',
      license='Apache',
      packages=find_packages(exclude=['bnap', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
