from datetime import datetime, date, time
import praw
from praw.models import MoreComments
from psaw import PushshiftAPI
import re

#Global Constants
trash_words = {'I', 'A', 'DFV', 'THE', 'DD', 'WSB'}

today_start = datetime.combine(date.today(), time())
after = int(today_start.timestamp()) #grab int representation of 12:00 am of today

api = PushshiftAPI()
gen_threads = api.search_submissions(subreddit='wallstreetbets', after=after, stickied=True)
results = list(gen_threads)
#grab all submissions from today that are pinned by mod
#   b/c we want DD discussion thread
dd_thread = 0

for res in results:
    if 'Daily' in res.title:
        dd_thread = res #grab DD thread from pinned threads


MAX_SEARCH = 100 #num of comments to pull from DD thread
gen_comments = api.search_comments(subreddit='wallstreetbets', id=dd_thread.id, limit=MAX_SEARCH)
comments = list(gen_comments)
tickers = {}

for comment in comments:
    s = comment.body.split() #split string into sep words
    for word in s:
        if word.isupper() and word not in trash_words : #if word is all caps it might be a ticker
            word = re.sub(r'\W+', '', word) #remove non alpha chars
            if len(word) <= 5: #make sure it has tick length
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

