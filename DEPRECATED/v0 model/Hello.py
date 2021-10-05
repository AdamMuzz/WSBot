'''
msg = "Hello World!"
print(msg)

tickers = ['TSLA', 'TSLA', 'AMD', 'amd']

dict1 = {}

for tick in tickers:
    if tick.isupper():
        print(tick)
        if dict1.get(tick):
            dict1[tick] += 1
        else:
            dict1[tick] = 1

print(dict1)
'''

'''
import requests
import datetime as dt
today_start = dt.datetime.combine(dt.date.today(), dt.time())
delta = dt.timedelta(days=5)
epoch_range = today_start - delta
epoch_range = int(epoch_range.timestamp())
print(epoch_range)
'''

from concurrent.futures import ThreadPoolExecutor
def foo(bar):
    print(bar)
    return 'foo'

glob = []
with ThreadPoolExecutor(5) as executor:
    for _ in range(5):
        future = executor.submit(foo, 'rab')
        glob.append(future.result())
print(glob)
