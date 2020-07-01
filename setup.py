from setuptools import setup

setup(name='pypowerbi',
      version='0.25',
      description='A python library for Microsoft\'s PowerBI',
      url='http://github.com/cmberryau/pypowerbi',
      author='Chris Berry',
      author_email='chris@chrisberry.com.au',
      license='MIT',
      packages=['pypowerbi'],
      install_requires=[
            'requests',
            'adal',
            'future-fstrings',
      ],
      zip_safe=False)
