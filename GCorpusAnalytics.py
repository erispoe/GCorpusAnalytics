import urllib2 as urllib
from bs4 import BeautifulSoup
import datetime
import csv
import time
import sys
import random

def main():
    if sys.argv[1].lower() == 'help':
        printHelp()
    else:
        corpus = str(sys.argv[1]).lower()
        y1 = int(sys.argv[2])
        y2 = int(sys.argv[3])
        it = int(sys.argv[4])
    
        #Creates the list of expressions to query from the expression file
        expressionsfile = open(sys.argv[5])
        expressions = []
        for line in expressionsfile:
            expressions.append(str(line).rstrip('\n'))

        outfilepath = ''
        try:
            outfilepath = sys.argv[6]
        except:
            pass
        
        queries = []
        
        #Create the list of datespans and one query object per datespan per expression
        for span in makeDatelist(y1, y2, it):
            d1 = span[0]
            d2 = span[1]
            for e in expressions:
                queries.append(Query(corpus, d1, d2, e))
        
        #Query all queries with a null result
        #When created, all queries have a null result, therefore all queries are processed the first time
        #Sometime a query gets an erroneous null result (0), processing three times the list of null queries reduces the risk of false null results
        for i in range(3):
            qwz = queriesWithZero(queries)
            if len(qwz) > 0:
                random.shuffle(qwz)
                for q in qwz:
                    time.sleep(random.uniform(1, 3))
                    q.makeQuery()
                    
        if outfilepath != '':
            exportToCsv(queries, len(expressions), outfilepath)
                
class Query:
    
    def __init__(self, corpus, d1, d2, expression):
        self.corpus = corpus
        self.d1 = d1
        self.d2 = d2
        self.expression = expression
        self.url = makeURL(self.corpus, self.expression, self.d1, self.d2)
        self.num = 0
    
    def printArgs(self):
        print self.corpus, self.d1, self.d2, self.expression, self.num
        
    def makeQuery(self):
        self.num = getResults(self.url)
        print self.d1.year, self.d2.year, self.expression, self.num
        
    def getNum(self):
        return self.num

def queriesWithZero(queries):
    #Returns a list of queries with a resultStats of zero
    qwz = []
    for q in queries:
        if q.getNum() == 0:
            qwz.append(q)
    return qwz

def exportToCsv(queries, nex, outfilepath):
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
    
def makeURL(corpus, expression, date1, date2):
    #Return the query URL
    
    expression = makeSafe(expression)
    
    YYYY1 = str(date1.timetuple()[0])
    MM1 = str(date1.timetuple()[1])
    DD1 = str(date1.timetuple()[2])
    
    YYYY2 = str(date2.timetuple()[0])
    MM2 = str(date2.timetuple()[1])
    DD2 = str(date2.timetuple()[2])
    
    if corpus == 'books':
        return 'http://www.google.com/search?hl=en&newwindow=1&q=' + expression + '&safe=off&tbm=bks&tbs=bkt:b%2Ccdr%3A1%2Ccd_min%3A' + MM1 +'%2F' + DD1 + '%2F' + YYYY1 + '%2Ccd_max%3A' + MM2 + '%2F' + DD2 + '%2F' + YYYY2

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