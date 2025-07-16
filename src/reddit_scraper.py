"""
Reddit Scraper Module
Handles scraping of Reddit user data including posts and comments.
"""

import praw
import time
import logging
from typing import Dict, List, Any
from datetime import datetime

from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    MAX_POSTS, MAX_COMMENTS, REQUEST_DELAY
)


class RedditScraper:
    """Scrapes Reddit user data including posts and comments."""
    
    def __init__(self):
        """Initialize Reddit API client."""
        self.logger = logging.getLogger(__name__)
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
    
    def scrape_user_data(self, username: str) -> Dict[str, Any]:
        """
        Scrape all posts and comments for a given Reddit user.
        
        Args:
            username: Reddit username
            
        Returns:
            Dictionary containing user data with posts and comments
        """
        user_data = {
            'username': username,
            'posts': [],
            'comments': [],
            'metadata': {
                'scraped_at': datetime.now().isoformat(),
                'total_posts': 0,
                'total_comments': 0
            }
        }
        
        try:
            user = self.reddit.redditor(username)
            
            # Scrape posts
            self.logger.info(f"Scraping posts for user: {username}")
            posts = self._scrape_posts(user)
            user_data['posts'] = posts
            user_data['metadata']['total_posts'] = len(posts)
            
            # Scrape comments
            self.logger.info(f"Scraping comments for user: {username}")
            comments = self._scrape_comments(user)
            user_data['comments'] = comments
            user_data['metadata']['total_comments'] = len(comments)
            
            self.logger.info(
                f"Scraped {len(posts)} posts and {len(comments)} comments"
            )
            
        except Exception as e:
            self.logger.error(f"Error scraping user data: {str(e)}")
            raise
        
        return user_data
    
    def _scrape_posts(self, user) -> List[Dict[str, Any]]:
        """Scrape user posts."""
        posts = []
        count = 0
        
        try:
            for post in user.submissions.new(limit=MAX_POSTS):
                if count >= MAX_POSTS:
                    break
                
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'content': post.selftext,
                    'subreddit': post.subreddit.display_name,
                    'created_utc': post.created_utc,
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'is_self': post.is_self
                }
                
                posts.append(post_data)
                count += 1
                
                # Rate limiting
                time.sleep(REQUEST_DELAY)
                
        except Exception as e:
            self.logger.error(f"Error scraping posts: {str(e)}")
        
        return posts
    
    def _scrape_comments(self, user) -> List[Dict[str, Any]]:
        """Scrape user comments."""
        comments = []
        count = 0
        
        try:
            for comment in user.comments.new(limit=MAX_COMMENTS):
                if count >= MAX_COMMENTS:
                    break
                
                comment_data = {
                    'id': comment.id,
                    'body': comment.body,
                    'subreddit': comment.subreddit.display_name,
                    'created_utc': comment.created_utc,
                    'score': comment.score,
                    'parent_id': comment.parent_id,
                    'link_id': comment.link_id,
                    'is_submitter': comment.is_submitter
                }
                
                comments.append(comment_data)
                count += 1
                
                # Rate limiting
                time.sleep(REQUEST_DELAY)
                
        except Exception as e:
            self.logger.error(f"Error scraping comments: {str(e)}")
        
        return comments