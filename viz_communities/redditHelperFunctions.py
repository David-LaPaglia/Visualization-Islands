import requests
import json
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


import praw

'''
This script contains helper functions for working with the Reddit API.
'''

# Load Reddit API credentials
with open('reddit_login.json','r') as f:
    r_creds = json.load(f)
r = praw.Reddit(
    client_id = r_creds['client_id'],
    client_secret = r_creds['client_secret'],
    password = r_creds['password'],
    user_agent = r_creds['user_agent'],
    username = r_creds['username']
)

'''
Function to get submissions from a subreddit
Takes in a subreddit name and a limit on the number of submissions to get
a pandas dataframe with columns: title, selftext, score, created_utc.'''
def get_submissions(subreddit, limit=1000):
    subreddit = r.subreddit(subreddit)
    print(f"Searching for submissions in r/{subreddit.display_name}...")
    subreddit_submissions = subreddit.top(limit=limit)
    subreddit_submissions = [submission for submission in subreddit_submissions] # convert to list
    subreddit_submissions = pd.DataFrame([(submission.title, submission.selftext, submission.score, submission.created_utc) for submission in subreddit_submissions], columns=['title', 'selftext', 'score', 'created_utc'])
    subreddit_submissions['created_utc'] = subreddit_submissions['created_utc'].apply(lambda x: datetime.datetime.utcfromtimestamp(x)) # using lambda function to convert to datetime
    subreddit_submissions = subreddit_submissions.sort_values('created_utc', ascending=False)
    subreddit_submissions = subreddit_submissions.reset_index(drop=True)
    print(subreddit_submissions.head())
    return subreddit_submissions




'''
Function to search many subreddits for a search term
Takes in a search term and a limit on the number of submissions to get
a json file with the following structure:
title,
subreddit,
text,
comments 
'''

def search_subreddits(search_term, file_name,limit,comments_limit):
    subreddit = r.subreddit('all')
    all_data = []  # List to store data
    for submission in subreddit.search(search_term, limit=limit):  #limit is the number of submissions to get
        try:
            print(f"Title: {submission.title}")
            print(f"Subreddit: {submission.subreddit}")
            print(f"Text: {submission.selftext if submission.selftext else 'No Text'}")
            
            submission.comments.replace_more(limit=None)
            comments = submission.comments.list()
            print(f"Number of comments: {len(comments)}")
            
            submission_data = {
                'search_term': search_term,
                'title': submission.title,
                'subreddit': str(submission.subreddit),  # Convert subreddit to string
                'text': submission.selftext if submission.selftext else 'No Text',
                'comments': [comment.body for comment in comments[:comments_limit]]  #limiting to 10 comments
            }
            all_data.append(submission_data) 
            with open('./data/'+file_name, 'w', encoding='utf-8') as f: # Save data to json file each itertion to avoid losing data
                json.dump(all_data, f, indent=4)  # If i stop it at any point, I can still have the data it got so far
        except Exception as e:
            print(f"Couldn't process submission: {submission.title}")

    print("Data collection complete. Saved to "+file_name)