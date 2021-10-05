#####################
# Trading Algorithm #
#####################

#dependencies
import datetime as dt
from psaw import PushshiftAPI
import re

#modules
import ticker_dict as td
import reddit_webscrape as rw

today_start = dt.datetime.combine(dt.date.today(), dt.time())
after = int(today_start.timestamp()) #grab int representation of 12:00 am of today

api = PushshiftAPI()
threads = rw.grab_threads(api, 'wallstreetbets', after)
#grab all thread submissions from today that are pinned by mod
#   b/c we want DD discussion thread and Moves For Tom thread

dd_thread = False
tom_thread = False
for res in threads:
    if 'Daily' in res.title:
        print(res.title)
        dd_thread = res #grab DD thread from pinned threads
    elif 'Tomorrow' in res.title:
        tom_thread = res

MAX_SEARCH = 500 #num of comments to pull from DD thread
comments = []

if dd_thread:
    dd_coms = rw.grab_comments(api, 'wallstreetbets', dd_thread, MAX_SEARCH)
    comments.extend(dd_coms)
    #get comments
if tom_thread:
    print('Grabbing ' + str(MAX_SEARCH) + ' comments from: ' + tom_thread.title)
    gen_comments = api.search_comments(subreddit='wallstreetbets', id=tom_thread.id, limit=MAX_SEARCH)
    tom_coms = list(gen_comments) #get all comments from today's DD from WSB
    comments.extend(tom_coms)

TD = td.ticker_dict()
tickers = {}

for comment in comments:
    s = comment.body.split() #split string into sep words
    for word in s:
        if word.isupper(): #if word is all caps it might be a ticker
            word = re.sub(r'\W+', '', word) #remove non alpha chars
            if TD.get(word): #make sure word is an actual ticker
                if tickers.get(word): #add to dict
                    tickers[word] += 1
                else:
                    tickers[word] = 1

#sort dict to grab most frequently talked abt ticks
sorted_tickers = dict(sorted(tickers.items(), key=lambda item: item[1], reverse=True))

MAX_TICKS = 10
top = []
for idx, ticker in enumerate(sorted_tickers): #grab 10 most talked abt ticks
    if (idx < MAX_TICKS):
        top.append(ticker)

print(top)
