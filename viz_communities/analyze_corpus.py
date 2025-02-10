import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_corpus_data(base_dir='text'):
    data = []
    
    # Data-related keywords to search for
    data_keywords = [
        'data', 'visualization', 'graph', 'chart', 'infographic', 
        'statistics', 'poll', 'survey', 'analysis', 'trend'
    ]
    
    # Load data from both subreddits
    for subreddit in ['democrats', 'republican']:
        subreddit_dir = os.path.join(base_dir, subreddit)
        
        for filename in os.listdir(subreddit_dir):
            if filename.endswith('.json'):
                with open(os.path.join(subreddit_dir, filename), 'r', encoding='utf-8') as f:
                    post = json.load(f)
                    
                    # Check if post contains data-related keywords
                    text_content = (post['title'] + ' ' + post['text']).lower()
                    contains_data = any(keyword in text_content for keyword in data_keywords)
                    
                    if contains_data:
                        data.append({
                            'subreddit': post['subreddit'],
                            'created_utc': datetime.fromisoformat(post['created_utc']),
                            'score': post['score'],
                            'title': post['title']
                        })
    
    return pd.DataFrame(data)

def analyze_engagement(df):
    # Basic statistics
    stats = df.groupby('subreddit').agg({
        'score': ['count', 'mean', 'median', 'std'],
        'created_utc': ['min', 'max']
    }).round(2)
    
    print("\nEngagement Statistics:")
    print(stats)
    
    # Create visualizations
    plt.figure(figsize=(15, 5))
    
    # Plot 1: Post frequency
    plt.subplot(1, 2, 1)
    sns.countplot(data=df, x='subreddit')
    plt.title('Frequency of Data-Related Posts')
    plt.ylabel('Number of Posts')
    
    # Plot 2: Engagement distribution
    plt.subplot(1, 2, 2)
    sns.boxplot(data=df, x='subreddit', y='score')
    plt.title('Distribution of Post Scores')
    plt.ylabel('Score (Upvotes)')
    
    plt.tight_layout()
    plt.savefig('engagement_analysis.png')
    plt.close()
    
    # Time series analysis
    df['month'] = df['created_utc'].dt.to_period('M')
    monthly_posts = df.groupby(['month', 'subreddit']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(15, 5))
    monthly_posts.plot(kind='line', marker='o')
    plt.title('Monthly Data-Related Posts Over Time')
    plt.xlabel('Month')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.legend(title='Subreddit')
    plt.tight_layout()
    plt.savefig('time_series_analysis.png')
    plt.close()

def main():
    print("Loading corpus data...")
    df = load_corpus_data()
    print("\nAnalyzing engagement...")
    analyze_engagement(df)
    print("\nAnalysis complete! Check engagement_analysis.png and time_series_analysis.png for visualizations.")

if __name__ == "__main__":
    main()
