+++ 
draft = false
date = 2025-07-07T20:38:56-07:00
title = "An Ode to Pocket: Analysis of Exported Logs"
description = "Analyzing 5 years of Pocket usage data reveals fascinating patterns in digital reading habits"
slug = ""
authors = []
tags = ["data-analysis", "pocket", "reading", "hacker-news", "python", "visualization", "digital-habits", "tech"]
categories = []
externalLink = ""
series = []
+++

Pocket is a service for saving links for later reading. It shuts down [tomorrow, July 8th RIP](https://support.mozilla.org/en-US/kb/future-of-pocket). Inspired by [noperator's post](https://noperator.dev/posts/o3-pocket-profile/), I decided to use Claude Code to analyze my exports as well. 

First some basic facts about my Pocket archive: 1,530 articles saved between January 2020 and May 2025. That's about 306 articles per year, or roughly 6 articles per week. Not too shabby when I feel like I'm always behind on my reading backlog.

![Pocket Analysis Charts](/pocket_analysis.png)

## The Hacker News Addiction

I have a serious Hacker News problem. 659 articles (43% of my entire archive) came from news.ycombinator.com. That's nearly half my digital reading diet from a single source. 

The next biggest sources were Substack (45 articles) and various email newsletters (36 articles). This tells a story: I'm either browsing Hacker News directly or getting curated content delivered to my inbox. Not much serendipitous discovery happening here.

It's worth noting that Hacker News is over-represented in this data because Pocket doesn't capture my other reading habits - I consume news through dedicated apps and read most email newsletters directly in my inbox. So while HN dominates my *saved* content, it's not actually half my total reading diet.

## What I'm Actually Reading

Looking at the most common words in article titles reveals my interests:

- "comments" appears 396 times – that's a lot of Hacker News comment threads -> I often prefer to save the HN thread over the actual link so I can read the discussions.
- "android" shows up 27 times – reflects my job as an Android dev working on Google Photos.
- "models" appears 19 times – the AI/ML trend is visible
- "learning" and "open" both appear 18 times – education and open source matter

Looking at this data, I see someone deeply embedded in the tech world, particularly interested in software development, AI/ML, and mobile development. The prevalence of "comments" suggests I'm not just reading articles but diving into discussions.

## Goodbye, Pocket

As Pocket shuts down tomorrow, this analysis feels like a fitting farewell. The service helped me build a habit of saving interesting content, even if I probably only read a fraction of what I saved. 

The data shows a clear evolution in my reading habits over 5+ years, with increasing engagement and more focused interests. Whether I'll maintain this level of curation with whatever replaces Pocket remains to be seen.

Thanks for the memories, Pocket. And thanks for the data – it's been illuminating to see my digital reading habits laid bare in charts and numbers.

With the Pocket shutdown, I migrated to a new setup: [Instapaper](https://instapaper.com/) for saving then sending most text heavy content to my kindle via http://ktool.io/ with feedly for RSS tracking.

---

*Analysis performed via Claude CLI using Python with pandas, matplotlib, and seaborn. The full breakdown covered 1,530 articles with 16 invalid entries removed during processing.* 

