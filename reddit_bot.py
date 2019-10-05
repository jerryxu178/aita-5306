import praw
import config
from praw.models import MoreComments
from operator import itemgetter
import csv

def scraper_login():
# log into the reddit account with credentials from config.py
    r = praw.Reddit(username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = "aita scraper v1.0")
    return r

def run_scraper(r):
# run the bot on subreddit designated in config.py
    post = r.submission(id = 'd7yuot') #NOTE: edit submission id here
    submission_info = []
    for top_level_comment in post.comments:
        if isinstance(top_level_comment, MoreComments): #ignore MoreComments
            continue
        #print "start"
        #print "score: " + str(top_level_comment.score)
        #print "minutes elapsed: " + str((top_level_comment.created_utc-s1.created_utc)/60)
        #print "number of replies: " + str(len(top_level_comment.replies))
        #print "number of words: " + str(len(top_level_comment.body.split(" ")))
        #print "end
        
        submission_info.append([top_level_comment.score
        , str(round(((top_level_comment.created_utc-post.created_utc)/60),1))
        , str(len(top_level_comment.replies))
        , str(len(top_level_comment.body.split(" ")))
        ])
    submission_info = sorted(submission_info, key=itemgetter(0))[::-1]
    counter = 1
    for elt in submission_info:
        elt.append("R" + str(counter))
        counter += 1
    submission_info = submission_info[:10]
        
    with open('data.csv',mode='w') as data:
        data_writer = csv.writer(data, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
        
        for elt in submission_info:
            data_writer.writerow(elt)  
        
        


r = scraper_login()
run_scraper(r)