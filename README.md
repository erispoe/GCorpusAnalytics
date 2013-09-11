GCorpusAnalytics
================

A python project to serialize queries on the number of items in google corpora, just books for the moment.

**WARNING: This project is still in beta phase, and sometimes produces erroneous results.**

Python version: 2.*

To read help, pass the argument help:
python GCorpusAnalytics.py help

The arguments for using this script are
python GCorpusAnalytics.py GoogleCorpus year_debut year_end time_interval expressions_file output_file

All arguments are required, apart from the output file.

GCorpusAnalytics is a python script that serializes queries to google corpora (only google books for the moment). For each interval of time_interval years between year_debut and year_end, the script will query the given google_corpus (here, books) for the number of items corresponding to each line in the passed expressions_file.

It will return a CSV output_file that can be read by any spreadsheet software (LibreOffice, Excel, Google Drive…). If you don't provide an output_file, the script will just print the results on the terminal.

For an example, see: http://www.favre-bulle.com/?p=7

Dependancies
------------

GCorpusAnalytics depends on the following python packages:
- urllib2
- datetime
- csv
- time
- sys
- Beautifulsoup

All but Beautifulsoup are usually included by default in any python installation. Beautifulsoup is used to parse the webpage google returns and extract the number of results.

If you have Easy install or Pip installed, just type:
easy_install beautifulsoup4
or
pip install beautifulsoup4

If not, the details of python installation can be found here:
http://docs.python.org/2/install/