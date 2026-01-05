+++
draft = false
date = 2025-07-25T09:37:49-07:00
title = "A Month With Claude Code"
description = "My experience using Claude Code for a month: from automation scripts to larger projects, exploring the shift from writing code to directing AI development."
slug = ""
authors = []
tags = ["claude-code", "ai-coding", "development-tools", "automation", "productivity", "sabbatical"]
categories = []
externalLink = ""
series = []
+++

During the past month I've been on sabbatical and decided to use Claude Code with the $20/month Pro plan. Here's what I learned from using it across various projects.

![Daily Usage](/ccusage-daily.png)

![Project Breakdown](/ccusage-projects.png)

*Usage data via [ccusage](https://github.com/ryoppippi/ccusage) - once you're on a subscription plan, claude clit itself no longer reports costs. This tools calculates the costs based on token usage.*

## From Coder to Tech Lead

The biggest shift? I'm no longer writing code—I'm directing it. Claude Code feels like managing a capable junior developer across multiple projects, from large applications like my [activity tracker](https://github.com/PureSin/activity-tracker) to quick automation scripts.

## Two Quick Wins

I needed to automate two simple tasks:
- Monitor YouTube for expected videos
- Check websites for inventory updates

Instead of my usual Python + cron approach, Claude suggested Cloudflare Workers. Within minutes, I had TypeScript scripts using the YouTube API and web scraping libraries, complete with email notifications. Cost? About $1 each to deploy and essentially free to run daily.

## The Reality Check

It's not perfect. Both large and small projects had their share of suboptimal code and logical bugs. But here's the thing—reviewing and tweaking Claude's work is far faster than writing from scratch. I can focus on architecture and requirements while Claude handles implementation details.

The workflow works surprisingly well: I act as product manager, Claude codes, I review and refine. The asynchronous nature means I can multitask—running errands or reading while Claude works, then checking back when ready.

## Session Limits and Reliability

I encountered one reliability [issue](https://github.com/anthropics/claude-code/issues/3891) where Claude would crash, but it was quickly fixed.

Session limits are a common concern—easy to hit on the $20/month Pro plan, and even users on $100-200/month plans report reaching limits quickly with Opus. Since Pro doesn't support Opus yet, I can't compare, but friends with access say it handles complex tasks noticeably better. Overall there is a lot of discussion/advice on how to best control costs/maximize token usage for these AI coding tools.

Update: July 29th: Anthropic updated to clarify their limits for Claude Code Usage: https://news.ycombinator.com/item?id=44713757

## Overall

This is genuinely a great tool. I love the terminal-first approach, and having Claude Code (or similar AI coding tools) makes side projects much more approachable—especially those small automation tasks I'd never bothered to tackle before.

The shift from writing code to directing it feels significant. It's not just about speed; it's about lowering the barrier to turn ideas into working software. Before this required finding collaborators for the project. Now it can be all managed by 1 person with the entire vision/plan/context in their head. 

## What's next

I'll try out claude code competitors like:

- Gemini CLI: https://github.com/google-gemini/gemini-cli
- ChatGPT Codex/Sourcegraph Amp/Google Jules
- Other CLI tools that uses openRouter for the the LLM inference or uses local inference so I have more control over the inference itself. 