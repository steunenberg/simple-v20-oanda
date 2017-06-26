from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='simplev20',
      version=version,
      description="Python wrapper for the Python wrapper for the OANDA V20 REST API",
      long_description="""\
""",
      classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry'
            'Operating System :: OS Independent',
            'Development Status :: 1 - Planning',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='OANDA FOREX wrapper REST API',
      author='Johan Steunenberg',
      author_email='kontakt@steunenberg.de',
      url='http://www.steunenberg.de',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
      test_suite="test",
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests', 'v20'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)