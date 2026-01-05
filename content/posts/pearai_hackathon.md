+++ 
date = 2024-05-17T15:45:17-07:00
title = "PearVC/OpenAI Hackathon: hacking in the AI era"
description = "A short recap of a 1 day hackathon"
slug = ""
authors = []
tags = ["ai", "hackathons"]
categories = []
externalLink = ""
series = []
+++

# Intro/Background

A few weeks back I attended the PearVC X OpenAI hackathon in SF. 

![Event Info](/pear_info.avif)

It's the first in-person external hackathon I attended in years, and the first in the "AI" era. Want to write done some thoughts on how "hacking" a product has been impacted by AI.

# The Hackathon

![Pear VC SF Hacker Space](/pear.jpg)

The event took place in PearVC's incubator space in Mission Bay. Had a nice view of the city on a beautiful day. Attendees grouped up in the morning with a brief intro by PearVC partners and a few companies they funded that are offering tools/APIs for the hackathon. Members of OpenAI's DevRel team was also there to help answer questions on usage and setup on slack and in person. 

It was a simple, 1 day (9am - 6pm) hackathon. No 48 hour, overnight intense session (which is great for me, I didn't event stay for the entire day, left around 1:30 after getting my hack working). Since I was planning to head out early, I opted to solo hack on this as to not be unfair to any teammates.

# The Idea: Screen assistant.

Do you ever do stuff around the house while something plays on the laptop? For example, cooking in the kitchen while sports is playing OR folding laundry while watching a show with your kid? Then once in a while, something comes on the screen you don't want to hear/see, you need to stop what you're doing and skip the video or dim the screen/lower the audio. 

I do this a lot, some examples are:
- Watching basketball while cooking, want to lower the volume when ads are playing but my hands are busy/wet.
- Folding laundry with my kid, and want to skip some part of a show

It would be great if my computer understands the kind of content I'm interested in and which portions of that content I'm not (ads during sports, scary parts for kids shows). Well now that we have LLMs, it should! Let's build it.

# The implementation 

![High level Diagram of Design](/pear_hack_diagram.png)

The Github repo is here: https://github.com/PureSin/Pearhack. 

It's a simple python script built using a mix of Python libs and OpenAI APIs:

- Audio Capture: pyaudio (for mic input to get the audio)
- Speech-to-text: OpenAI's whisper API 
- Classifiying text into interest value in [0,1] range: a custom LLM on OpenAI
- Computer Control: `control_device` script to control the mac's screen brightness and audio levels.

The first part for audio capture using pyaudio was fast to get it to capture on input channels (the default laptop mic). I did want the option for audio capture to be purely from the output audio stream of the video being watched as well. Sadly I coulnd't get that working after trying different options with pyaudio (and simliar python libraries). If you know how to do so, please let me know.

Once I had the audio (captured in 10s chunks as wav files). Doing speech-to-text using Whipser was quick and simple. I save the text in a txt file mostly for recording keeping (so I can use it as training examples for the classifier in the next step).

For the classifier, I created a custom prompt on OpenAI and tried different prompts. After some basic exampls for NBA games (in game commentry vs text from ads breaks), the prompt was generally working (few-shot learning). 

Lastly, control the audio level and screen brightness was done using OS X script commands. 

Overall, the entire system came together in 2.5 hours to have a first working version: [Example Video Link](https://photos.app.goo.gl/sKzNEWegaUPkNoNB8)

# Learnings

- Anything is possible!

With LLMs, you can probably get something to work. Does it work well (what is the precision/recall) and across all possible settings? That's hard to say. 

- Ability to quickly, confidently tune a model for an acceptable level of performance is critical.

Building from the last learning, some basic "promot engineering" ability is important. Knowing "how" to ask the LLM and also having a good evaluation pipeline to know which prompts are actually better is the only want to make forward progress. This means knowledge of working with data, setting up evaluation sets and a few/single score to gauge improvements. 

- Still need the ability to design and code a system. 

Coding assistants are helpful, but they can't fully build a system, searching useful libraries, understand how to structure the pieces together yet. Maybe that'll change in the next 2-3 years. Until then, knowing how to build a product (the product description, UX, engineering) is still a critical skill. 
