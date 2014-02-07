try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='GCorpusAnalytics',
      version='0.1.0',
      description='Serialize queries on the number of items in Google corpora',
      author='Thomas Favre-Bulle',
      author_email='thomas.favre-bulle@epfl.ch',
      url='https://github.com/Erispoe/GCorpusAnalytics',
      packages=['GCorpusAnalytics'],
      long_description=open('README.md').read(),
      package_data= {'Useragents': ['data/Useragents.txt']},
      install_requires=[
          "beautifulsoup4 >= 4.3.1",
      ],
      classifiers=[
          'Programming Language :: Python :: 2',
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering :: Information Analysis',
      ],
     )