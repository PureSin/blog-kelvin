# My Blog: blog.kelvin.ma

Personal blog built with Hugo, focusing on tech learnings, OMSCS course summaries, book notes, and AI/finance/tech insights.

## Development Commands

### Start Development Server
```bash
# With drafts
hugo server -D

# Without drafts  
hugo server
```

### Create New Post
```bash
hugo new content posts/<post-name>.md
```

### Build Site
```bash
hugo
```

## Content Guidelines

### Tags
See [TAGS.md](TAGS.md) for the canonical list of tags and tagging guidelines. Use consistent, lowercase tags with hyphens to separate words.

### Writing Style
- Friendly, casual tone
- Focus areas: OMSCS courses, tech learnings, book notes, AI/finance/tech insights
- Markdown format with occasional images

## Project Structure

- `content/posts/` - Blog post markdown files
- `content/notes/` - Research and notes for Claude Code reference  
- `layouts/` - Custom layout overrides
- `static/` - Static assets (images, CSS, etc.)
- `themes/hugo-coder/` - Hugo Coder theme submodule
- `TAGS.md` - Tag guidelines and canonical tag list

