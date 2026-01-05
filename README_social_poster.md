# Social Media Auto-Poster for Hugo Blog

Automatically post new blog entries to Twitter, Bluesky, and LinkedIn with customizable templates and URL shortening.

## Features

- 🐦 **Twitter/X integration** - Posts with API v2
- 🦋 **Bluesky integration** - Native AT Protocol support  
- 💼 **LinkedIn integration** - Professional network posting
- 📝 **Smart content generation** - Platform-specific templates and length limits
- 🔗 **URL shortening support** - Ready for integration with your preferred service
- 📊 **Post tracking** - Prevents duplicate posts with local log
- 🧪 **Dry run mode** - Preview posts before publishing
- ⚙️ **Flexible configuration** - JSON-based settings

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Access

Edit `social_config.json` with your API credentials:

#### Twitter Setup
1. Apply for Twitter Developer access at https://developer.twitter.com
2. Create a new app in your Twitter Developer dashboard
3. Generate API keys and access tokens
4. Note: Basic tier ($200/month) required for posting

#### Bluesky Setup  
1. Create an app password in Bluesky Settings → Privacy and Security → App Passwords
2. Use your Bluesky handle and app password (not your main password)

#### LinkedIn Setup
1. Create a LinkedIn app at https://www.linkedin.com/developers
2. Request "Share on LinkedIn" product access
3. Complete OAuth 2.0 flow to get access token
4. Note: Basic access has limitations

### 3. Test Configuration

```bash
# Dry run to see what would be posted
python social_poster.py --dry-run

# Test with latest post
python social_poster.py --dry-run --force
```

### 4. Post to Social Media

```bash
# Post new unpublished posts to all platforms
python social_poster.py

# Post to specific platforms only
python social_poster.py --platforms twitter bluesky

# Force post the latest article (even if already posted)
python social_poster.py --force
```

## Configuration

### API Credentials (`social_config.json`)

```json
{
  "twitter": {
    "api_key": "YOUR_TWITTER_API_KEY",
    "api_secret": "YOUR_TWITTER_API_SECRET", 
    "access_token": "YOUR_TWITTER_ACCESS_TOKEN",
    "access_token_secret": "YOUR_TWITTER_ACCESS_TOKEN_SECRET"
  },
  "bluesky": {
    "username": "your.handle.bsky.social",
    "password": "YOUR_BLUESKY_APP_PASSWORD"
  },
  "linkedin": {
    "access_token": "YOUR_LINKEDIN_ACCESS_TOKEN"
  }
}
```

### Post Templates

Customize post formats in the `templates` section:

```json
{
  "templates": {
    "twitter": {
      "format": "📝 New blog post: {title}\n\n{description}\n\n{short_url}\n\n{hashtags}"
    },
    "bluesky": {
      "format": "📝 New blog post: {title}\n\n{description}\n\n{short_url}\n\n{hashtags}"  
    },
    "linkedin": {
      "format": "📝 New blog post: {title}\n\n{description}\n\nRead more: {short_url}\n\n{hashtags}\n\n#TechBlog #SoftwareEngineering"
    }
  }
}
```

Available template variables:
- `{title}` - Blog post title
- `{description}` - Post description from frontmatter
- `{url}` - Full blog post URL
- `{short_url}` - Shortened URL (implement URL shortening service)
- `{hashtags}` - Auto-generated hashtags from post tags

## Usage Examples

```bash
# Post only new content to all platforms
python social_poster.py

# Preview what would be posted
python social_poster.py --dry-run

# Post to Twitter and Bluesky only
python social_poster.py --platforms twitter bluesky  

# Force post latest article to LinkedIn
python social_poster.py --platforms linkedin --force

# Use custom config file
python social_poster.py --config my_config.json
```

## How It Works

1. **Scans** `content/posts/` for markdown files with TOML frontmatter
2. **Parses** post metadata (title, date, description, tags)
3. **Filters** for published posts (not drafts) that haven't been shared
4. **Generates** platform-specific content using templates
5. **Posts** to selected social media platforms
6. **Tracks** posted content in `posted_posts.json` to prevent duplicates

## Platform-Specific Notes

### Twitter
- Character limit: 280
- Requires paid API access ($200/month minimum)
- Uses OAuth 2.0 authentication
- Auto-truncates content if too long

### Bluesky  
- Character limit: 300 (soft limit)
- Free API access
- Uses AT Protocol with app passwords
- Growing platform with tech-focused audience

### LinkedIn
- Character limit: 3000 (generous)
- Limited API access for basic users
- Professional audience
- Best for tech/career content

## URL Shortening

The script includes placeholder support for URL shortening. To implement:

1. Choose a service (bit.ly, tinyurl, etc.)
2. Update the `_shorten_url()` method in `social_poster.py`
3. Add API credentials to your config

## Tracking & Logs

- `posted_posts.json` - Tracks which posts have been shared
- Prevents duplicate posting
- Includes metadata like post date and platforms used
- Can be manually edited if needed

## Automation

Consider setting up automated posting with cron:

```bash
# Post new content daily at 9 AM
0 9 * * * cd /path/to/blog && python social_poster.py

# Check for new posts every 4 hours  
0 */4 * * * cd /path/to/blog && python social_poster.py
```

## Troubleshooting

### Common Issues

1. **Import errors**: Install dependencies with `pip install -r requirements.txt`
2. **Twitter 403 errors**: Check if you have paid API access
3. **LinkedIn authentication**: Ensure proper OAuth 2.0 setup
4. **Bluesky login**: Use app password, not account password
5. **No posts found**: Check that posts aren't marked as drafts

### Debug Mode

Add logging to see what's happening:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security

- Keep `social_config.json` secure and out of version control
- Use environment variables for production deployments
- Regularly rotate API keys and tokens
- Consider using `.gitignore` to exclude sensitive files

## Contributing

Feel free to extend this script with:
- Additional social media platforms
- URL shortening service integration
- Enhanced template systems
- Better error handling
- Scheduling improvements

---

Built for Hugo blogs with TOML frontmatter. Customize as needed for your specific setup!