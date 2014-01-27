from distutils.core import setup

setup(name='GCorpusAnalytics',
      version='0.1.0',
      description='Serialize queries on the number of items in Google corpora',
      author='Thomas Favre-Bulle',
      author_email='thomas.favre-bulle@epfl.ch',
      url='https://github.com/Erispoe/GCorpusAnalytics',
      packages=['GCorpusAnalytics'],
      long_description=open('README.md').read(),
      #install_requires=[
      #    "urllib2 >= 2.7",
      #    "bs4 >= 4.3.1",
      #    "csv >= 1.0",
      #    "json >= 2.0.9",
      #],
     )