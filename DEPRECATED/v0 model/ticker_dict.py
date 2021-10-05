#Creates dictionary of ticker symbols from tickers.txt
#   allows O(1) search-up to see if a ticker is valid (ie see if its in dict)

def ticker_dict():
    file_path = "tickers.txt" #path to text file containing ticker files
    tickers = {} #dictionary to hold dicts

    with open(file_path, 'r') as data: #go thru each line in tickers.txt
        for line in data:
            ticker = line.split('\t', 1)[0] #get ticker
            tickers[ticker.upper()] = True #add to dict w/ true data

    return tickers #return filled up dict



#test cases
if __name__ == '__main__':
    test_dict = ticker_dict()
    assert test_dict['AAPL']
    assert test_dict.get('z') == None
    print('All test cases completed successfully')
