GCorpusAnalytics
================

A python project to serialize queries on the number of items in google corpora, just books for the moment.

**WARNING: This project is still in beta phase, and sometimes produces erroneous results.**

Python version: 2.*

To read help, pass the argument help:    
python GCorpusAnalytics.py help

## Formatting your request

The script takes in argument a JSON file with your request. See Request.json for an example.

The JSON file needs to contain the following parameters:

- Corpus: only “books” at the moment
- YearDebut: first year of the date interval
- YearEnd: last year of the date interval
- TimeInterval: interval in years (minimum 1 for one query per year)
- Language: only “en” at the moment
- Outfile: name of the csv file to export
- Expressions: list of expressions to query for every date interval. Keep in mind that these can include Google valid search operators.

## Use in command line

Open a terminal in the folder where both your JSON request file and the script are located. The script runs in two phases:

1. Execute to query the results:    
python GCorpusAnalytics.py Request.json execute    
If the script gets blocked by Google, retry later, this time with the db file where temporary results are stored:    
python GCorpusAnalytics.py Request.db execute    
The script will restart to query results where it got stopped.

2. When notified “All queries executed and results retrieved”, to export in csv:    
python GCorpusAnalytics.py Request.db exportcsv

## Use as a package

GCorpusAnalytics can be imported as a package directly in another python script. To do so, install it with pip in the console:

pip install https://github.com/Erispoe/GCorpusAnalytics/zipball/master

You can then import it in a python script and use the class Request. To create a class Request, pass it a name and a JSON string with the request. You can then execute the request or export its results in csv.

from GCorpusAnalytics import GCorpusAnalytics as gca    
r = gca.Request('Request_books',open('Request_books.json').read())    
r.execute()    
r.exportCsv()    

The script will create a database file with the same name of your request in the same directory of your python script. This database file contains all the informations to relaunch the request if it gets blocked by Google

If the script gets blocked by Google, retry later, recreating the Request by giving it only a name, and it will retrieve all request informations and already parsed results in the database file.

## See an example

For an example, see: http://www.favre-bulle.com/?p=7

