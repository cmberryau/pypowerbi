from setuptools import setup

setup(name='pypowerbi',
      version='0.14',
      description='A python library for Microsoft\'s PowerBI',
      url='http://github.com/cmberryau/pypowerbi',
      author='Chris Berry',
      author_email='chris@chrisberry.com.au',
      license='MIT',
      packages=['pypowerbi'],
      install_requires=[
            'requests',
            'adal',
      ],
      zip_safe=False)
