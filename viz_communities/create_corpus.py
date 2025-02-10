import os
import json
from redditHelperFunctions import get_submissions
import datetime

def save_to_corpus(submissions, subreddit_name, base_dir='text'):
    # Create subreddit directory if it doesn't exist
    subreddit_dir = os.path.join(base_dir, subreddit_name)
    os.makedirs(subreddit_dir, exist_ok=True)
    
    # Save each submission as a separate JSON file
    for idx, row in submissions.iterrows():
        # Create a clean filename using timestamp
        timestamp = row['created_utc'].strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{idx}.json"
        filepath = os.path.join(subreddit_dir, filename)
        
        # Prepare post data
        post_data = {
            'title': row['title'],
            'text': row['selftext'],
            'score': int(row['score']),
            'created_utc': row['created_utc'].isoformat(),
            'subreddit': subreddit_name
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, ensure_ascii=False, indent=2)

def main():
    # Get submissions from both subreddits
    print("Fetching submissions from r/democrats...")
    dem_submissions = get_submissions('democrats', limit=1000)
    
    print("Fetching submissions from r/republican...")
    rep_submissions = get_submissions('republican', limit=1000)
    
    # Save submissions to corpus
    print("Saving Democratic submissions to corpus...")
    save_to_corpus(dem_submissions, 'democrats')
    
    print("Saving Republican submissions to corpus...")
    save_to_corpus(rep_submissions, 'republican')
    
    print("Corpus creation complete!")

if __name__ == "__main__":
    main()
