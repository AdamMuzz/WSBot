#######################################
# handles retrieving reddit comments  #
#######################################

from psaw import PushshiftAPI

#grab_threads
#   grab all threads from given subreddit. [<sub> is name of subreddit as a string]
#   <API> a PushShiftAPI object to access psaw data
#   <from_when> int representation of how far back to look into subreddit's history to grab threads
#   <stickied> default true, is to grab only threads that are pinned by sub's moderator
def grab_threads(API, sub, from_when, stickied = True):
    print('Finding DD and MFT threads...')
    gen_threads = API.search_submissions(subreddit=sub, after=from_when, stickied=stickied)
    return list(gen_threads)

#grab_comments
#   grab N comments from given thread off of given sub
#   <API>
def grab_comments(API, sub, thread, lim):
    print('Grabbing ' + str(lim) + ' comments from: ' + thread.title + '...')
    gen_comments = API.search_comments(subreddit=sub, id=thread.id, limit=lim)
    return list(gen_comments)

    #print('Grabbing ' + str(MAX_SEARCH) + ' comments from: ' + dd_thread.title)
    #gen_comments = api.search_comments(subreddit='wallstreetbets', id=dd_thread.id, limit=MAX_SEARCH)
    #dd_coms = list(gen_comments) #get all comments from today's DD from WSB
    #comments.extend(dd_coms)


#test cases
if __name__ == '__main__':
    api = PushshiftAPI()
    ex_threads = grab_threads(api, 'NatureIsFuckingLit', 1554361200)
    print(ex_threads[0].title)

    print('All test cases completed successfully')