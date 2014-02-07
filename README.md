GCorpusAnalytics
================

A python project to serialize queries on the number of items in google corpora, just books for the moment.

**WARNING: This project is still in beta phase, and sometimes produces erroneous results.**

Python version: 2.*

To read help, pass the argument help:
python GCorpusAnalytics.py help

The script takes in argument a JSON file with your request. See Request.json for an example.

The JSON file needs to contain the following parameters:

- Corpus: only “books” at the moment
- YearDebut: first year of the date interval
- YearEnd: last year of the date interval
- TimeInterval: interval in years (minimum 1 for one query per year)
- Language: only “en” at the moment
- Outfile: name of the csv file to export
- Expressions: list of expressions to query for every date interval. Keep in mind that these can include Google valid search operators.

Open a terminal in the folder where both your JSON request file and the script are located. The script runs in two phases:

1. Execute to query the results:
python GCorpusAnalytics.py Request.json execute
If the script gets blocked by Google, retry later, this time with the db file where temporary results are stored:
python GCorpusAnalytics.py Request.db execute
The script will restart to query results where it got stopped.

2. When notified “All queries executed and results retrieved”, to export in csv:
python GCorpusAnalytics.py Request.db export

For an example, see: http://www.favre-bulle.com/?p=7

Dependancies
------------

GCorpusAnalytics depends on the following python packages:
- urllib2
- datetime
- time
- csv
- time
- sys
- sqlite3
- json
- pprint
- Beautifulsoup

All but Beautifulsoup are usually included by default in any python installation. Beautifulsoup is used to parse the webpage google returns and extract the number of results.

If you have Easy install or Pip installed, just type:
easy_install beautifulsoup4
or
pip install beautifulsoup4

If not, the details of python installation can be found here:
http://docs.python.org/2/install/