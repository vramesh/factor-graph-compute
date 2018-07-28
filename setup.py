from setuptools import setup, setuptools

setup(name='hmslearn',
      version='0.0.4.1',
      description='factor graph framework for machine and reinforcement learning',
      url='https://github.com/vramesh/factor-graph-compute',
      author='Andrew Yunta Tsai, Vinayak Ramesh, Devavrat Shah, Suchan Vivatsethachai',
      author_email='andytsai14@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'numpy',
          'redis',
      ],
      zip_safe=False)