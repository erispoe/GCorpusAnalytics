import urllib2 as urllib
from bs4 import BeautifulSoup
import datetime
import csv
import time
import sys
import random
import json
import sqlite3 as lite
from pprint import pprint

def main():
    #Check if the script argument is help to display the readme file
    if sys.argv[1].lower() == 'help':
        printHelp()
    
    else:
        reqname = str(sys.argv[1]).split('.')[-2]
        
        req = ''
        if str(sys.argv[1]).split('.')[-1] == 'json':
            jsonstr = open(sys.argv[1]).read()
            req = Request(reqname, jsonstr)
        if str(sys.argv[1]).split('.')[-1] == 'db':
            req = Request(reqname)
        
        req.executeNullQueries()

class Request:
    #A request with all its parameters and the list of individual queries
    
    def __init__(self, name, jsonstr=''):
        
        self.name = name
        
        #Create a dictionnary from the JSON request, either from the json file or retrieved a previously created the database
        self.reqdic = {}
        if jsonstr != '':
            self.reqdic = json.loads(jsonstr)
        else:
            self.reqdic = json.loads(self.getJsonInDb())
        
        self.corpus = self.reqdic['Request']['Corpus'].lower()
        self.y1 = int(self.reqdic['Request']['YearDebut'])
        self.y2 = int(self.reqdic['Request']['YearEnd'])
        self.it = int(self.reqdic['Request']['TimeInterval'])
        self.lr = self.reqdic['Request']['Language'].lower()
        
        self.outfilepath = self.reqdic['Request']['Outfile']
        
        self.expressions = []
        for e in self.reqdic['Request']['Expressions']:
            self.expressions.append(e['Expression'])
        
        if jsonstr != '':
            self.createDatabase(jsonstr)
            self.createQueries()
        
    def getJsonInDb(self):
        conn = lite.connect(self.name + '.db', isolation_level=None)
        c = conn.cursor()
        sql="SELECT json FROM TheRequest WHERE Id = 1"
        c.execute(sql)
        jsonstr = str(c.fetchone()[0])
        return jsonstr
    
    def createQueries(self):
        conn = lite.connect(self.name + '.db', isolation_level=None)
        c = conn.cursor()
        for span in makeDatelist(self.y1, self.y2, self.it):
            d1 = span[0]
            d2 = span[1]
            
            YYYY1 = str(d1.timetuple()[0])
            MM1 = str(d1.timetuple()[1])
            DD1 = str(d1.timetuple()[2])
    
            YYYY2 = str(d2.timetuple()[0])
            MM2 = str(d2.timetuple()[1])
            DD2 = str(d2.timetuple()[2])
            
            for e in self.expressions:
                sql = "INSERT INTO Queries(corpus, date1, date2, expression, url, result, numbofexec) VALUES(:corpus, :date1, :date2, :expression, :url, :result, :numbofexec)"
                qdic = {'corpus' : self.corpus, 'date1' : YYYY1 + MM1 + DD1, 'date2' :  YYYY2 + MM2 + DD2, 'expression' : e, 'url' : makeURL(self.corpus, e, d1, d2), 'result' : 0 , 'numbofexec' : 0}
                c.execute(sql, qdic)
        conn.close()
                
    def readQueries(self):
        conn = lite.connect(self.name + '.db', isolation_level=None)
        c = conn.cursor()
        sql = "SELECT * FROM Queries"
        c.execute(sql)
        pprint(c.fetchall())
        conn.close()
        
    def executeNullQueries(self):
        conn = lite.connect(self.name + '.db', isolation_level=None)
        c = conn.cursor()
        i = 0
        while i == 0:
            try:
                sql='SELECT Id, url, numbofexec, date1, date2, expression FROM Queries WHERE result = 0 AND numbofexec <= 5 ORDER by RANDOM() LIMIT 1'
                c = conn.execute(sql)
                query = c.fetchone()
                #print query
                Id = query[0]
                url = query[1]
                numbofexec = int(query[2])
                result = getResults(url)
                #print result
                print str(query[3])[:4] + '-' + str(query[4])[:4], str(query[5]), result
                updateresult = "UPDATE Queries SET result = " + str(result) + ", numbofexec = " + str(numbofexec + 1) + " WHERE Id = " + str(Id)
                c = conn.execute(updateresult)
            except TypeError,e:    
                    print "All queries executed and results retrieved"
                    i = 1
            except Exception,e:
                    print "Google may have blocked your IP temporarily, retry later by passing the database file to the python script:"
                    print "python GCorpusAnalytics.py " + self.name + ".db"
                    print "The requests will restart where they stopped here."
                    i = 1
        conn.close()
        
    def runQueries(self):
        #Query all queries with a null result
        #When created, all queries have a null result, therefore all queries are processed the first time
        qwz = nullQueries(self.queries)
        if len(qwz) > 0:
            random.shuffle(qwz)
            for q in qwz:
                time.sleep(random.uniform(1, 3))
                q.makeQuery()
                
    def createDatabase(self, jsonstr):
        dbname = self.name + '.db'
        conn = lite.connect(dbname, isolation_level=None)
        c = conn.cursor()
    
        c.execute("DROP TABLE IF EXISTS Queries")
        c.execute("DROP TABLE IF EXISTS TheRequest")
        
        createTableQueries = '''CREATE TABLE Queries
                 (Id INTEGER PRIMARY KEY AUTOINCREMENT, corpus TEXT, date1 DATE, date2 DATE, expression TEXT, url TEXT, result INTEGER, numbofexec INTEGER)'''
        createTableTheRequest = "CREATE TABLE TheRequest (Id INTEGER PRIMARY KEY AUTOINCREMENT, json TEXT)"
        c.execute(createTableTheRequest)
        c.execute(createTableQueries)
        
        jsondic = {'json' : jsonstr}
        sql = "INSERT INTO TheRequest(json) VALUES(:json)"
        c.execute(sql, jsondic)
        
        conn.close()
                    
    def exportResults(self):
        print "Export of results"
        if self.outfilepath != '':
            exportToCsv(self.queries, len(self.expressions), self.outfilepath)

def exportToCsv(queries, nex, outfilepath):
    #OUTDATED
    
    #Export a list of queries into to csv files, one wih the resultats, the other with the url, for controlling purposes
    #queries: the list of query objects to export to csv, sorted
    #nex: the number of expressions
    #outfilepath: the path of the csv file to export
    
    controlfilepath = outfilepath.rstrip('.csv') + '_urlcontrol.csv'
    controlfile = open(controlfilepath, 'w')
    outfile = open(outfilepath, 'w')
    
    wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    wrc = csv.writer(controlfile, quoting=csv.QUOTE_ALL)
    
    #Let's assume the queries are sorted
    #Which they should be because they are created sorted and all operations take place on another instance of the list
    
    datamodel = []
    datamodel.append('Timespan')
    
    for i in range(nex):
        datamodel.append(queries[i].expression)
        
    wr.writerow(datamodel)
    wrc.writerow(datamodel)
    
    while len(queries) > 0:
        d1 = queries[0].d1
        d2 = queries[0].d2
        resultrow = []
        urlrow = []
        strspan = str(d1.year)
        if d1.year != d2.year:
            strspan = str(d1.year) + '-' + str(d2.year)
        resultrow.append(strspan)
        urlrow.append(strspan)
        for i in range(nex):
            resultrow.append(queries[0].num)
            urlrow.append(queries[0].url)
            del queries[0]
        wr.writerow(resultrow)
        wrc.writerow(urlrow)
    

def getResults(url):
    #Query Google to return the numbers of items corresponding to the query url
    
    headers={'User-Agent':randomUserAgent(),}
    
    request=urllib.Request(url,None,headers)
    soup = BeautifulSoup(urllib.urlopen(request).read())
    
    resultStats = 0
    if noResults(soup):
        pass
    else:
        try:
            if soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[0] == 'About':
                resultStats = int(soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[1].replace(',',''))
            else:
                resultStats = int(soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[0].replace(',',''))
        except:
            pass
    
    #Sometimes the results page returns a high number of results even though it only displays a few of them
    if elementCounter(soup) < resultStats and elementCounter(soup) < 10 :
        resultStats = elementCounter(soup)
        
    return resultStats

def randomUserAgent():
    #Return a random user agent from the ones listed in the file Useragents.txt
    useragents = open('Useragents.txt').readlines()
    return str(random.choice(useragents)).rstrip('\n')

def makeSafe(expression):
    #Takes a string and returns html safe strings
    return urllib.quote(expression, safe="%/:=&?~#+!$,;'@()*[]")
    
def makeDatelist(y1, y2, it):
    #Returns a list of time spans between two dates
    ny = y1
    datelist = []
    while ny < y2:
        d1 = datetime.date(ny, 1, 1)
        d2 = datetime.date(ny+it-1, 12, 31)
        ny = ny + it
        dates = d1,d2
        datelist.append(dates)
    return datelist
    
def makeURL(corpus, expression, d1, d2):
    #Return the query URL
    
    expression = makeSafe(expression)
    
    if corpus == 'books':
        return 'http://www.google.com/search?hl=en&newwindow=1&q=' + expression + '&safe=off&tbm=bks&tbs=bkt:b%2C' + timeMapper(d1, d2)

def timeMapper(d1, d2):
    
    YYYY1 = str(d1.timetuple()[0])
    MM1 = str(d1.timetuple()[1])
    DD1 = str(d1.timetuple()[2])

    YYYY2 = str(d2.timetuple()[0])
    MM2 = str(d2.timetuple()[1])
    DD2 = str(d2.timetuple()[2])
    
    return makeSafe('cdr:1,cd_min:' + MM1 + '/' + DD1 + '/' + YYYY1 + ',cd_max:' + MM2 + '/' + DD2 + '/' + YYYY2)

def elementCounter(soup):
    #Returns the number of items in the first page of results
    return len(soup.find_all("div", {"class": "rc"}))
    
def noResults(soup):
    #Returns True is the page contains a no results alter
    r = False
    try:
        if str(soup.find("div", {"id": "topstuff"}).find_all("div", {"class": "med"})[0].find_all("img")[0]['src']) == '/images/yellow-alert2x.png':
            r = True
    except:
        pass
    return r
    
def printHelp():
    #Prints the README.md file as help
    helptext = open('README.md').read()
    print helptext

if __name__ == '__main__':
    main()