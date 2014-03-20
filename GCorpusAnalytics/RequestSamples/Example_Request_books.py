from GCorpusAnalytics import GCorpusAnalytics as gca

def main():
	r = gca.Request('Request_books', open('Request_books.json').read())
	r.execute()
	r.exportCsv()

if __name__ == '__main__':
    main()