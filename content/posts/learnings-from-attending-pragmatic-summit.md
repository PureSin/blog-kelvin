+++ 
draft = true
date = 2026-02-12T21:55:57-08:00
title = "Learnings from attending Pragmatic Summit"
description = ""
slug = ""
authors = []
tags = []
categories = []
externalLink = ""
series = []
+++

I attended [https://www.pragmaticsummit.com/](https://www.pragmaticsummit.com/) this past Wed hosted by [Gergely Orosz](https://www.pragmaticengineer.com/).. As with all things tech right now, the main (and really only) topic is AI. Thankfully the attendees are all active professionals working in tech, the discussions are grounded in hands-on experience with AI tools, avoiding much of the hype. 

![Summit Agenda](/pragmatic_summit/summit_agenda.webp)

As a software engineer at Google working on the Photos mobile clients’ editing features, I’m lucky to not worry about the token budget in terms of costs and can freely use Gemini 3 models for my work. It was both scary and comforting to learn that engineers at other places are struggling with the same challenges as me right now. Mainly:


* In a world where AI writes the code, how do roles and processes on software teams change? 
* How do we best take advantage of AI? Is it purely in the model, or how much value is there in context (domain knowledge) and customization of the harness on top of the model?

I’ll share my thoughts/learnings now that I had a few days to reflect on this summit. 

*Disclaimer: I work at Google but not on any AI model or tools. These are just my personal thoughts, and I’m as likely to be wrong than to be correct.*

Instead of doing a recap on the sessions I attended, I’ll discuss popular themes presented in the talks and discussions throughout the day. The talk recordings will be shared later and I’ll watch any sessions I missed and summarize those. 


## #1: AI now writes the code



* **AI Writing Code is the Norm:** It is now clear that AI, with tools like Codex, is capable of **writing** code line-by-line, moving coding to a human language level.

And since AI doesn't get tired, can understand most common coding languages, the final step of translating detailed human intent into code is better left to AI.  I'm still telling the AI what to write, the level of specification depends on the task. 



* Routine tasks with a lot of training data/examples: more like giving a task to a teammate: please clean up this flag. AI can figure the rest out.,.
* Larger tasks that are novel are performance/security sensitive: more like a pair programming session, sitting with the AI tool and iterating.

Day to day this looks:


1. Triage my tasks, which ones are routine vs novel
2. Fire off parallel AI agents for the routine ones with clear goals and ask them to send me a diff.
3. Fire off a dedicated AI agent for 1 novel task (maybe with a UI more focused on specific files) and iterate until I’m confident the AI knows the clear goals and design, then have it auto run.
4. Review the results of agents from step 2

Which means I’m producing more diffs, which means the bottleneck moves from writing code to reviewing, deploying, evaluating product changes. AI doesn't help as much with code review, and that is the next step for AI tools to accelerate software development. (though many at the summit are pretty excited and happy with [https://graphite.com/](https://graphite.com/) for AI assisted code reviews)

![AI Cycle](/pragmatic_summit/ai_cycle.png)


## #2: Software team practices needs to adapt

Now that the coding part is taken care of by AI, which used to be a large portion of the focus time required for software development, the team overall needs to adapt. For one, coding languages and frameworks are less of a barrier because AI is really good at helping an engineer on board to new tech stacks. So there's less of a need for specialization like front end vs backend or mobile vs web. And for many simpler changes like accessibility fixes or UX polish, the PM or designer can directly make those changes instead of fighting bugs and waiting for Eng to free up (often with better results since they can best verify the change is done correctly )

And lastly, since each engineer can do more in the same span of time, the cost of being blocked has gone up. It's more and more important to gather all the requirements to allow engineers to close the loop and enable the AI to self-iterate until the goals are reached.


## #3 Mobile vs Web for User facing applications

Mobile engineering (Android, iOS) presents unique challenges for AI due to longer compile times and greater difficulty for AI to "close the loop" and self-verify its work compared to web development.

Potential Solutions:



* **Componentization:** Breaking up monolithic mobile apps into smaller, individual application feature components to allow for faster build times and shorter verification steps.
* **Cross-Platform Tools:** The rise of spec-driven development with AI could either eliminate the need for per-platform testing (by testing only the web version) or enable spec-to-implementation for each native platform, with the final direction still being uncertain. Everyone at the roundtable discussion for this topic has no idea which way it’d go. 

Everyone working on mobile agreed that AI struggles with “closing the loop” (being able to self verify) compared to Web. Most are building custom skills to assist AI. Skills are a new tool and lack a standard way to evaluate, compare, gather metrics on useful skills. The answer to: “how do you know this skill is good” is **vibes. **The most common way to distribute skills is dev to dev or team show and tells. 

## #4 Leadership, Process, and Culture

Moving past the IC role, the larger question is how does a company adapt to this new world. Even if the frontier labs immediately pause on “smarter” models and focus on inference speed/model size/harness, the existing models already will lead to dramatic changes in processes. I’d like to end with some ideas (and a quote) presented in Laura Tacho’s talk (Data vs Hype). AI is here and its coding abilities are amazing, but engineers and people do more than code or move bytes on a computer, at the end of the day the value is in solving human problems.

* **AI as an Accelerator:** AI does not change existing processes; it accelerates them. Functional companies ship faster and more quality features, but dysfunctional companies experience more bugs and production incidents at a faster rate.
* **Developer Experience (DX) Funding:** Initiatives to improve DX (faster build times, better tests, less tech debt) are now more easily funded by reframing them as "AI adoption" efforts (e.g., "faster build times for AI").

"*Organizations are constrained by human and systems-level problems. We remain skeptical of the promise of any technology to improve organizational performance without first addressing human and systems-level constraints*.

*We remain skeptical and we remain human.*"

— **Kent Beck, Laura Tacho, and Steve Yegge**
