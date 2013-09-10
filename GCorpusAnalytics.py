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
        try:
            corpus = str(sys.argv[1]).lower()
            y1 = int(sys.argv[2])
            y2 = int(sys.argv[3])
            it = int(sys.argv[4])
    
            expressionsfile = open(sys.argv[5])
            expressions = []
            for line in expressionsfile:
                expressions.append(str(line).rstrip('\n'))
    
            outfile = ''
            try:
                outfile = sys.argv[6]
            except:
                pass
    
            if corpus == 'books':
                results = GBooksQuery(y1, y2, it, expressions, outfile)
            else:
                print """At the moment, the google corpora supported are:
- books"""
        except Exception, e:
            print "Oups, there seems to be a problem somewhere: '" , e , "'"
            try:
                if e.code == 503:
                    print 'Google temporarily blocked your queries, try again in a little while.'
            except:
                pass
            print "To get help on how to use the script, type 'python GCorpusAnalytics.py help'"

def GBooksQuery(y1, y2, it, expressions, outfile=''):
    #Parameters:
    #y1: start year
    #y2: end year
    #it: interval of queries, in years
    #expressions: a list of string of expression to find in google books
    #outfile: file where the resuts are to be exported

    wr = 0
    wrc = 0
    
    if outfile != '':
        controlfile = open(outfile.rstrip('\n') + '_urlcontrol.csv', 'wb')
        outfile = open(outfile, 'wb')
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        wrc = csv.writer(controlfile, quoting=csv.QUOTE_ALL)
    
    results = []
    datamodel = [] 
    datamodel.append('Timespan')
    datamodel = datamodel + expressions
    results.append(datamodel)
    printRow(datamodel)
    
    if wr != 0:
        wr.writerow(datamodel)
        wrc.writerow(datamodel)
        
    expressions = makeSafe(expressions)
    
    for span in makeDatelist(y1, y2, it):
        d1 = span[0]
        d2 = span[1]
        
        strspan = str(d1.year)
        if d1.year != d2.year:
            strspan = str(d1.year) + '-' + str(d2.year)
        result = [strspan]
        urls = [strspan]
        for e in expressions:    
            num, url = resultStatsBooks(e, d1, d2)
            result.append(num)
            urls.append(url)
            time.sleep(random.uniform(1, 3))
        results.append(result)
        printRow(result)
        
        if wr != 0:
            wr.writerow(result)
            wrc.writerow(urls)
            
    return results

def makeSafe(expressions):
    #Takes a list of strings and returns alist of html safe strings
    safeexpr = []
    for e in expressions:
        e = urllib.quote(e, safe="%/:=&?~#+!$,;'@()*[]")
        safeexpr.append(e)
    return safeexpr

def makeDatelist(y1, y2, it):
    
    ny = y1
    datelist = []
    while ny < y2:
        d1 = datetime.date(ny, 1, 1)
        d2 = datetime.date(ny+it-1, 12, 31)
        ny = ny + it
        dates = d1,d2
        datelist.append(dates)
    return datelist
    

def resultStatsBooks(expression, date1, date2):
    #Query Google Books to return the numbers of items corresponding to the expression between the dates date1 and date2
    
    headers={'User-Agent':randomUserAgent(),}
    
    YYYY1 = str(date1.timetuple()[0])
    MM1 = str(date1.timetuple()[1])
    DD1 = str(date1.timetuple()[2])
    
    YYYY2 = str(date2.timetuple()[0])
    MM2 = str(date2.timetuple()[1])
    DD2 = str(date2.timetuple()[2])
    
    url = 'http://www.google.com/search?hl=en&newwindow=1&q=' + expression + '&safe=off&tbm=bks&tbs=bkt:b%2Ccdr%3A1%2Ccd_min%3A' + MM1 +'%2F' + DD1 + '%2F' + YYYY1 + '%2Ccd_max%3A' + MM2 + '%2F' + DD2 + '%2F' + YYYY2
    
    request=urllib.Request(url,None,headers)
    soup = BeautifulSoup(urllib.urlopen(request).read())
    
    resultStats = 0
    try:
        if soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[0] == 'About':
            resultStats = int(soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[1].replace(',',''))
        else:
            resultStats = int(soup.find("div", {"id": "resultStats"}).contents[0].split(' ')[0].replace(',',''))
    except:
        pass
        
    if len(soup.find("div", {"id": "topstuff"}).contents) > 0:
        resultStats = 0
    
    return resultStats, url
    
def printRow(list):
    #Takes a list and prints it on a line, elements separated by commas
    st = ''
    for i in list:
        st = st + str(i) + ', '
    st = st[:-2]
    print st
    
def printHelp():
    #Prints the README.md file as help
    helptext = open('README.md').read()
    print helptext
    
def randomUserAgent():
    #Return a random user agent from the ones listed in the file Useragents.txt
    useragents = open('Useragents.txt').readlines()
    return str(random.choice(useragents)).rstrip('\n')
    
if __name__ == '__main__':
    main()