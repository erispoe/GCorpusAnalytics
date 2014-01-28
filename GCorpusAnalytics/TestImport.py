import GCorpusAnalytics as gca

def main():
    r = gca.Request('Request_books')
    r.executeNullQueries()
    r.exportToCsv()
    
if __name__ == '__main__':
  main()