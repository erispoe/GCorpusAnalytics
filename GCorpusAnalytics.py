import urllib2 as urllib
from bs4 import BeautifulSoup
import datetime
import csv
import time
import sys

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
        except Exception, e:
            print 'Oups, there seems to be a problem somewhere:'
            print e
            print 'Here is how to use the script:'
            printHelp()

def GBooksQuery(y1, y2, it, expressions, outfile=''):
    #Parameters:
    #y1: start year
    #y2: end year
    #it: interval of queries, in years
    #expressions: a list of string of expression to find in google books
    #outfile: file where the resuts are to be exported

    wr = 0
    
    if outfile != '':
        outfile = open(outfile, 'wb')
        wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
    
    results = []
    datamodel = [] 
    datamodel.append('Timespan')
    datamodel = datamodel + expressions
    results.append(datamodel)
    printRow(datamodel)
    
    if wr != 0:
        wr.writerow(datamodel)
        
    expressions = makeSafe(expressions)
    
    for span in makeDatelist(y1, y2, it):
        d1 = span[0]
        d2 = span[1]
        
        strspan = str(d1.year)
        if d1.year != d2.year:
            strspan = str(d1.year) + '-' + str(d2.year)
        result = [strspan]
        for e in expressions:    
            num = resultStatsBooks(e, d1, d2)
            result.append(num)
            time.sleep(2)
        results.append(result)
        printRow(result)
        
        if wr != 0:
            wr.writerow(result)
            
    return results

def makeSafe(expressions):
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
    expression = urllib.quote(expression, safe="%/:=&?~#+!$,;'@()*[]")
    
    user_agent = 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36'
    headers={'User-Agent':user_agent,}
    
    YYYY1 = str(date1.timetuple()[0])
    MM1 = str(date1.timetuple()[1])
    DD1 = str(date1.timetuple()[2])
    
    YYYY2 = str(date2.timetuple()[0])
    MM2 = str(date2.timetuple()[1])
    DD2 = str(date2.timetuple()[2])
    
    url = 'http://www.google.com/search?hl=en&newwindow=1&q=' + expression + '&safe=off&tbm=bks&tbs=bkt:b%2Ccdr%3A1%2Ccd_min%3A' + MM1 +'%2F' + DD1 + '%2F' + YYYY1 + '%2Ccd_max%3A' + MM2 + '%2F' + DD2 + '%2F' + YYYY2
    
    #print url
    
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
    
    return resultStats
    
def printRow(list):
    st = ''
    for i in list:
        st = st + str(i) + ', '
    st = st[:-2]
    print st
    
def printHelp():
    
    helptext = open('README.md').read()
    print helptext
    
if __name__ == '__main__':
    main()