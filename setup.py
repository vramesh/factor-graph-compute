from setuptools import setup, find_packages

setup(name='6438toypackage',
      version='0.0.1',
      description = 'toy package for 6438',

      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'sample=sample:main'
          ]
      }
)