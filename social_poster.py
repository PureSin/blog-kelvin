#!/usr/bin/env python3
"""
Social Media Auto-Poster for Hugo Blog
Automatically posts new blog entries to Twitter, Bluesky, and LinkedIn
"""

import os
import json
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path
import yaml
import toml
from typing import Dict, List, Optional
import urllib.parse

# Platform-specific imports (install with pip install -r requirements.txt)
try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False
    
try:
    from atproto import Client as BlueskyClient
    BLUESKY_AVAILABLE = True
except ImportError:
    BLUESKY_AVAILABLE = False
    
try:
    import requests
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BlogPost:
    """Represents a blog post with metadata and content"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.title = ""
        self.date = None
        self.description = ""
        self.tags = []
        self.draft = False
        self.url = ""
        
        self._parse_frontmatter()
        
    def _parse_frontmatter(self):
        """Parse TOML frontmatter from markdown file"""
        content = self.file_path.read_text(encoding='utf-8')
        
        if content.startswith('+++'):
            # TOML frontmatter
            end_idx = content.find('+++', 3)
            if end_idx != -1:
                frontmatter = content[3:end_idx].strip()
                try:
                    data = toml.loads(frontmatter)
                    self.title = data.get('title', '')
                    self.description = data.get('description', '')
                    self.tags = data.get('tags', [])
                    self.draft = data.get('draft', False)
                    
                    # Parse date
                    date_str = data.get('date', '')
                    if date_str:
                        try:
                            self.date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        except ValueError:
                            logger.warning(f"Could not parse date: {date_str}")
                            
                    # Generate URL from filename
                    slug = self.file_path.stem
                    self.url = f"https://blog.kelvin.ma/posts/{slug}/"
                    
                except Exception as e:
                    logger.error(f"Error parsing frontmatter for {self.file_path}: {e}")

class SocialMediaPoster:
    """Main class for posting to social media platforms"""
    
    def __init__(self, config_path: str = "social_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.posted_log = Path("posted_posts.json")
        self.posted_posts = self._load_posted_log()
        
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(self.config_path):
            logger.error(f"Config file not found: {self.config_path}")
            return {}
            
        with open(self.config_path, 'r') as f:
            return json.load(f)
            
    def _load_posted_log(self) -> Dict:
        """Load log of already posted content"""
        if self.posted_log.exists():
            with open(self.posted_log, 'r') as f:
                return json.load(f)
        return {}
        
    def _save_posted_log(self):
        """Save log of posted content"""
        with open(self.posted_log, 'w') as f:
            json.dump(self.posted_posts, f, indent=2)
            
    def _shorten_url(self, url: str) -> str:
        """Generate shortened URL (placeholder - implement with your preferred service)"""
        # You can integrate with bit.ly, tinyurl, or any URL shortening service
        # For now, return the original URL
        return url
        
    def get_latest_posts(self, limit: int = 5) -> List[BlogPost]:
        """Get the latest blog posts"""
        posts_dir = Path("content/posts")
        if not posts_dir.exists():
            logger.error("Posts directory not found")
            return []
            
        posts = []
        for md_file in posts_dir.glob("*.md"):
            post = BlogPost(md_file)
            if not post.draft and post.date:  # Only published posts with dates
                posts.append(post)
                
        # Sort by date, newest first
        posts.sort(key=lambda p: p.date, reverse=True)
        return posts[:limit]
        
    def get_unposted_posts(self) -> List[BlogPost]:
        """Get posts that haven't been shared on social media yet"""
        latest_posts = self.get_latest_posts()
        unposted = []
        
        for post in latest_posts:
            post_key = post.file_path.stem
            if post_key not in self.posted_posts:
                unposted.append(post)
                
        return unposted
        
    def generate_post_content(self, post: BlogPost, platform: str) -> str:
        """Generate platform-specific post content"""
        templates = self.config.get('templates', {})
        template = templates.get(platform, {})
        
        # Default templates if not configured
        default_templates = {
            'twitter': "📝 New blog post: {title}\n\n{description}\n\n{short_url}\n\n{hashtags}",
            'bluesky': "📝 New blog post: {title}\n\n{description}\n\n{short_url}\n\n{hashtags}",
            'linkedin': "📝 New blog post: {title}\n\n{description}\n\nRead more: {short_url}\n\n{hashtags}"
        }
        
        template_str = template.get('format', default_templates.get(platform, ''))
        
        # Generate hashtags
        hashtags = ' '.join([f"#{tag.replace(' ', '').replace('-', '')}" for tag in post.tags[:3]])
        
        # Shorten URL
        short_url = self._shorten_url(post.url)
        
        content = template_str.format(
            title=post.title,
            description=post.description or "Check out my latest thoughts!",
            url=post.url,
            short_url=short_url,
            hashtags=hashtags
        )
        
        # Platform-specific length limits
        limits = {'twitter': 280, 'bluesky': 300, 'linkedin': 3000}
        limit = limits.get(platform, 280)
        
        if len(content) > limit:
            # Truncate description if needed
            excess = len(content) - limit
            if post.description and len(post.description) > excess + 10:
                truncated_desc = post.description[:len(post.description) - excess - 10] + "..."
                content = template_str.format(
                    title=post.title,
                    description=truncated_desc,
                    url=post.url,
                    short_url=short_url,
                    hashtags=hashtags
                )
                
        return content[:limit]
        
    def post_to_twitter(self, content: str) -> bool:
        """Post content to Twitter/X"""
        if not TWITTER_AVAILABLE:
            logger.error("Twitter/Tweepy not available. Install with: pip install tweepy")
            return False
            
        twitter_config = self.config.get('twitter', {})
        if not all(key in twitter_config for key in ['api_key', 'api_secret', 'access_token', 'access_token_secret']):
            logger.error("Twitter API credentials not configured")
            return False
            
        try:
            client = tweepy.Client(
                consumer_key=twitter_config['api_key'],
                consumer_secret=twitter_config['api_secret'],
                access_token=twitter_config['access_token'],
                access_token_secret=twitter_config['access_token_secret']
            )
            
            response = client.create_tweet(text=content)
            logger.info(f"Posted to Twitter: {response.data['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to post to Twitter: {e}")
            return False
            
    def post_to_bluesky(self, content: str) -> bool:
        """Post content to Bluesky"""
        if not BLUESKY_AVAILABLE:
            logger.error("Bluesky/atproto not available. Install with: pip install atproto")
            return False
            
        bluesky_config = self.config.get('bluesky', {})
        if not all(key in bluesky_config for key in ['username', 'password']):
            logger.error("Bluesky credentials not configured")
            return False
            
        try:
            client = BlueskyClient()
            client.login(bluesky_config['username'], bluesky_config['password'])
            
            post = client.send_post(content)
            logger.info(f"Posted to Bluesky: {post.uri}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to post to Bluesky: {e}")
            return False
            
    def post_to_linkedin(self, content: str) -> bool:
        """Post content to LinkedIn"""
        if not LINKEDIN_AVAILABLE:
            logger.error("Requests not available for LinkedIn posting")
            return False
            
        linkedin_config = self.config.get('linkedin', {})
        if 'access_token' not in linkedin_config:
            logger.error("LinkedIn access token not configured")
            return False
            
        try:
            headers = {
                'Authorization': f"Bearer {linkedin_config['access_token']}",
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            # Get user profile ID (you may want to cache this)
            profile_response = requests.get(
                'https://api.linkedin.com/v2/people/~',
                headers=headers
            )
            
            if profile_response.status_code != 200:
                logger.error(f"Failed to get LinkedIn profile: {profile_response.text}")
                return False
                
            profile_id = profile_response.json()['id']
            
            # Create post
            post_data = {
                "author": f"urn:li:person:{profile_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                logger.info(f"Posted to LinkedIn: {response.json()['id']}")
                return True
            else:
                logger.error(f"Failed to post to LinkedIn: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {e}")
            return False
            
    def post_to_platform(self, platform: str, post: BlogPost, dry_run: bool = False) -> bool:
        """Post to a specific platform"""
        content = self.generate_post_content(post, platform)
        
        if dry_run:
            print(f"\n--- {platform.upper()} POST (DRY RUN) ---")
            print(content)
            print(f"--- END {platform.upper()} POST ---\n")
            return True
            
        platform_methods = {
            'twitter': self.post_to_twitter,
            'bluesky': self.post_to_bluesky,
            'linkedin': self.post_to_linkedin
        }
        
        method = platform_methods.get(platform)
        if not method:
            logger.error(f"Unknown platform: {platform}")
            return False
            
        return method(content)
        
    def post_latest(self, platforms: List[str] = None, dry_run: bool = False, force: bool = False):
        """Post the latest unposted blog posts to social media"""
        if platforms is None:
            platforms = ['twitter', 'bluesky', 'linkedin']
            
        if force:
            posts_to_share = self.get_latest_posts(1)  # Just the latest post
        else:
            posts_to_share = self.get_unposted_posts()
            
        if not posts_to_share:
            logger.info("No new posts to share")
            return
            
        for post in posts_to_share:
            logger.info(f"Sharing post: {post.title}")
            
            post_key = post.file_path.stem
            success_count = 0
            
            for platform in platforms:
                if self.post_to_platform(platform, post, dry_run):
                    success_count += 1
                    
            if success_count > 0 and not dry_run:
                # Mark as posted
                self.posted_posts[post_key] = {
                    'title': post.title,
                    'posted_date': datetime.now(timezone.utc).isoformat(),
                    'platforms': platforms,
                    'url': post.url
                }
                self._save_posted_log()
                logger.info(f"Successfully posted '{post.title}' to {success_count}/{len(platforms)} platforms")

def main():
    parser = argparse.ArgumentParser(description='Social Media Auto-Poster for Hugo Blog')
    parser.add_argument('--config', default='social_config.json', help='Configuration file path')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be posted without actually posting')
    parser.add_argument('--force', action='store_true', help='Force post the latest article even if already posted')
    parser.add_argument('--platforms', nargs='+', choices=['twitter', 'bluesky', 'linkedin'], 
                       help='Specific platforms to post to')
    
    args = parser.parse_args()
    
    poster = SocialMediaPoster(args.config)
    poster.post_latest(
        platforms=args.platforms,
        dry_run=args.dry_run,
        force=args.force
    )

if __name__ == "__main__":
    main()