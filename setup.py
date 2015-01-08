from setuptools import setup

exec (open('delightfulsoup/version.py').read())

setup(name='delightfulsoup',
      version=__version__,
      author='Étienne Tétreault-Pinard',
      author_email='etienne.t.pinard@gmail.com',
      maintainer='Étienne Tétreault-Pinard',
      maintainer_email='etienne.t.pinard@gmail.com',
      url='https://github.com/etpinard/delightfulsoup',
      description="Python package extending BeautifulSoup's features",
      classifiers=[
          'Programming Language :: Python :: 2.7'
      ],
      license='MIT',
      packages=['delightfulsoup', 'delightfulsoup/utils'],
      zip_safe=False)
