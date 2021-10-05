import requests
import csv
import sched, time

###############
# GLOBAL VARS #
###############

watchlist = set() #tracks all tickers being watched
owned = set() #tracks all tickers with currently opened positions
s = sched.scheduler(time.time, time.sleep) #global scheduler to handle bots



##########################
# Data Retrieval Section #
##########################
#'''
#open and clear tickers.txt file
open('tickers.txt', 'w').write('')
watchlist = open('tickers.txt', 'ab')

#grab ticker info from each url and append it to tickers.txt
urls = ['https://yolostocks.live/downloads/wallstreetbets.csv',
		'https://yolostocks.live/downloads/stocks.csv',
		'https://yolostocks.live/downloads/pennystocks.csv',
		'https://yolostocks.live/downloads/options.csv']

for url in urls:
	r = requests.get(url, allow_redirects=True)
	watchlist.write(r.content)
#'''


###########################
# Data Processing Section #
###########################
'''
# grab only ticker symbols from file, add to array
#	acts as intial populater of watchlist on startup
with open('tickers.txt', 'r') as tickers:
	reader = csv.reader(tickers)
	next(reader, None)
	for row in reader:
		watchlist.add(row[0])
'''


#######################
# Trading Bot Section #
#######################

#create scheduler to handle processes

'''	WATCHLIST UPDATER BOT
calls data section to update ticker array
runs every 30 mins
'''
def watchlist_updater():
	print('updating watchlist')

	watchlist.clear() #empty list

	with open('tickers.txt', 'r') as tickers: #repopulate list
		reader = csv.reader(tickers)
		next(reader, None)
		for row in reader:
			watchlist.add(row[0])
	
	delay = 1800 - ((time.time() - start_time) % 1800)
	s.enterabs(time.time() + delay, 10, watchlist_updater) #reschedule itself to run in 30 mins

'''INCOMPLETE PAST THIS'''

'''
goes thru ticker array to watch each stock
for every stock:
	checks its volume compared to avg vol
	checks price changes
if a stock is high volume and trending up: set a buy order
runs every 30 seconds
'''
def watchlist_bot():
	print('watchlist')
	next = 2 - ((time.time() - start_time) % 2)
	s.enterabs(time.time() + next, 1, watchlist_bot)

'''
goes thru every owned stock
for every stock:
	checks something
if stock is sell: set a sell order
runs every 30 seconds
'''

'''
handles buy/sell orders
'''

'''
start_time = time.time()
s.enterabs(time.time(), 1, watchlist_bot)
s.run()
'''