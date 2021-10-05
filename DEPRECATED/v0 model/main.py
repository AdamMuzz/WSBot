#####################
# Trading Algorithm #
#####################

#dependencies
import datetime as dt
from psaw import PushshiftAPI
import re
import concurrent.futures
import itertools

#modules
import ticker_dict as td
import reddit_webscrape as rw

'''
today_start = dt.datetime.combine(dt.date.today(), dt.time())
after = int(today_start.timestamp()) #grab int representation of 12:00 am of today
'''

#get date of day RANGE days ago from today
RANGE = 10
today_start = dt.datetime.combine(dt.date.today(), dt.time())
delta = dt.timedelta(days=RANGE)
epoch_range = today_start - delta
epoch = int(epoch_range.timestamp())

api = PushshiftAPI()
threads = rw.grab_threads(api, 'wallstreetbets', epoch)
#grab all thread submissions from range that are pinned by mod
#   b/c we want DD discussion threads and Moves For Tom threads

dd_threads = [] #filter to only DD/MFT threads
for res in threads:
    if 'Daily' in res.title:
        dd_threads.append(res)
    elif 'Tomorrow' in res.title:
        dd_threads.append(res)

MAX_SEARCH = 10 #num of comments to pull from DD thread
comment_results = []

#'''
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_thread = {executor.submit(rw.grab_comments, api, 'wallstreetbets', thread, MAX_SEARCH) : thread for thread in dd_threads}
    for future in concurrent.futures.as_completed(future_to_thread):
        thread = future_to_thread[future]
        try:
            data = future.result()
        except Exception as exc:
            print('Generated exception: %s' % exc)
        else:
            comment_results.append(data)
comments = list(itertools.chain.from_iterable(comment_results))
'''
for thread in dd_threads:
    coms = rw.grab_comments(api, 'wallstreetbets', thread, MAX_SEARCH)
    comment_results.append(coms)
comments = list(itertools.chain.from_iterable(comment_results))
'''

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