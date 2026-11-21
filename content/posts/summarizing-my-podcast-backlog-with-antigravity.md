+++
draft = true
date = 2026-11-21T08:30:00-08:00
title = "Summarizing 75+ Hours of Podcasts with Antigravity and Gemini Neon"
description = "How I worked with Antigravity and Gemini Neon to build a free-tier audio condensation pipeline that shrank a 75-hour Pocket Casts backlog down to under 14 hours—without leaving the official app."
slug = ""
authors = []
tags = ["ai", "ai-coding", "automation", "python", "productivity", "digital-habits"]
categories = []
externalLink = ""
series = []
+++

Like my old reading backlog, my podcast backlog has a habit of growing much faster than I can listen to it. Some episodes are two or three hours long, and I don't always want to skip them entirely—I just want the core conversation without the tangents (and occasionally without the profanity, depending on who's in the car).

Back when I wrote about [AI and personal software](/posts/ai-and-personal-software/), the thesis was that AI coding tools make it cheap enough to build software tailored specifically to how you want your existing apps to behave. Recently, I worked with **Antigravity** and **Gemini Neon** to put that into practice on my Pocket Casts backlog.

The end result: a resumable, zero-cost pipeline that condensed **59 episodes (~75+ hours of audio)** down to **13 hours and 50 minutes**—saving over 60 hours of listening time—and dropped the condensed versions straight back into a playlist in the official Pocket Casts Android app.

<!-- TODO: Add a quick note on what working with Antigravity + Gemini Neon felt like on this project (e.g., how much time it took end-to-end, or a screenshot of the working playlist / pipeline output). -->

Here's how we designed and built it step by step.

## 1. Architecture: Don't Fork the App, Own the Feed

Before writing any code, we evaluated three ways to add custom AI features (topic-focused episode shortening and profanity bleeping/muting) to my Android podcast workflow:

1. **Fork the open-source Pocket Casts Android client** and build the features directly into the app.
2. **Fork AntennaPod** and add AI processing there.
3. **Keep the official Pocket Casts app untouched** and build an off-device processing pipeline that publishes the transformed episodes to a private RSS feed.

Option 3 won pretty quickly. Transcription, LLM editing, and audio re-encoding are heavy workloads that make much more sense off-device anyway. More importantly, keeping the unmodified Pocket Casts app means I keep native mobile playback, downloads, and cross-device sync for free—with zero Android fork maintenance.

## 2. Pocket Casts Account & Playlist Automation

Once we committed to the RSS pipeline approach, I still didn't want to manually wrangle 60 episode URLs or hand-rebuild a playlist. So we built a Python client using `httpx` targeting Pocket Casts' unofficial web and mobile sync APIs (`api.pocketcasts.com` and `podcast-api.pocketcasts.com`).

A few pieces made this work cleanly:

- **Auth & Queue Management:** Token-based authentication that stores only a local session token, supporting reading/editing the listening queue, inspecting subscriptions and episode durations, and archiving episodes.
- **Manual Playlist Editing via Protobuf:** Pocket Casts' manual playlists sync through a binary protobuf endpoint (`/user/sync/update`). We compiled Pocket Casts' `sync_api.proto` using `grpcio-tools` (`protoc`) so our script could read, clone, prune, and update manual playlists directly—passing `/user/last_sync_at` timestamps so edits persist cleanly across syncs.
- **Safe Cloning & Planning:** Rather than mutating my main backlog in place, we cloned it into a separate working playlist, pruned out unwanted shows and episodes, and exported a structured JSON processing plan for **60 target episodes across 6 shows**.

## 3. The Hybrid Audio Condensation Pipeline ("Original Voices + AI Bridges")

Pure text-to-speech podcast summaries always feel a little sterile—part of the reason I listen to podcasts is to hear the hosts and guests themselves. Instead of replacing an episode with an AI monologue, we built a modular, resumable Python pipeline (`Typer`, `httpx`, `ffmpeg`, `python-dotenv`) around an **"Original Voices + AI Bridges"** design: keep the best contiguous segments of original audio, and stitch across skipped sections with brief AI-narrated transitions.

### Transcription (Cloud Speed + Local Fallback)

- Started with local `faster-whisper` (CPU `int8`) with transcript caching to disk so re-runs never redo transcription. This layer also supports word-level timestamps paired with `ffmpeg` beep/mute filters for profanity filtering.
- Added **Groq Whisper** (`whisper-large-v3-turbo`) for much faster cloud transcription. To stay under Groq's 25 MB upload limit on long episodes, `ffmpeg` compresses the audio to 16 kHz mono and chunks it into 90-minute segments.
- Whenever Groq's free-tier hourly rate limits kick in, the pipeline automatically falls back to local `faster-whisper` so batch runs don't stall.

### Clip Selection & Bridge Writing (Free-Tier LLMs)

- Transcripts are grouped into compact 60-second timestamped blocks, capped to stay within model context limits.
- Using OpenRouter's free models (`openrouter/free`) and Groq's free-tier LLMs—wrapped with retry logic and resilient JSON extraction—the pipeline selects contiguous original audio spans targeting roughly **12 minutes per episode** and writes 1–2 sentence bridge narrations summarizing what was skipped between clips.

### TTS & Audio Stitching

- Bridge narrations are synthesized with free neural TTS (`edge-tts`), with text sanitization and fallback voices in case a synthesis call hiccups.
- `ffmpeg` handles the final assembly: trimming each selected original clip with short fade-ins and fade-outs, inserting silence spacers around bridges, normalizing audio channels and sample rates, and encoding the result into compact 96 kbps speech MP3s.

## 4. Persistent Free-Tier RSS Hosting on Google Drive

With condensed MP3s in hand, we still needed a reliable way to serve them—and a private RSS feed—to Pocket Casts on Android.

We first tested a local FastAPI / Uvicorn RSS server exposed via Cloudflare Tunnel (`cloudflared`), and also evaluated static repository hosting. Both had tradeoffs (keeping a machine awake vs. repo size limits for audio files). In the end, we moved to **Google Drive** via the `gdrive` CLI for 24/7 static hosting without an always-on server.

- Each condensed MP3 is uploaded to Drive with link-sharing enabled.
- A single RSS 2.0 + iTunes XML feed is updated in place on Drive as new episodes finish processing.
- **The Android playback gotcha:** Standard Google Drive share links go through redirects and virus-scan confirmation pages that break podcast players. Switching to direct, zero-redirect URLs (`drive.usercontent.google.com` with `confirm=t`) gave Android's media player clean `HTTP 200` responses with `Accept-Ranges: bytes`, so streaming and scrubbing work reliably.

## 5. Batch Execution & Automated Playlist Swapping

With the end-to-end pieces verified, we kicked off the resumable batch run across the 60-episode plan:

- **59 unique episodes processed:** 1 duplicate dead link was skipped, and stale `404` audio URLs were automatically refreshed via Pocket Casts' metadata API.
- **~75+ hours → 13h 50m:** Over **60 hours** of runtime cut across the backlog, with raw and intermediate audio files cleaned up automatically after each episode.
- **In-place playlist swapping:** Once Pocket Casts indexed the private RSS feed, our automation matched each condensed episode and swapped it in place inside the working playlist—**50 swapped so far**, with the final **9** ready to swap as soon as Pocket Casts finishes its next feed poll.

<!-- TODO: Update final swap count once the last 9 episodes are swapped in. -->

## Reflections & What's Next

<!-- TODO: Add personal takeaways from working with Antigravity and Gemini Neon:
- How did the condensed episodes actually sound on a real commute/walk? Any quirks with pacing or AI bridge transitions?
- Where did Antigravity / Gemini Neon shine most (e.g., reverse-engineering the protobuf sync flow, debugging ffmpeg filtergraphs and Drive range requests, keeping the pipeline resumable)?
- What's next? (e.g., turning this into a recurring workflow for new episodes, tuning profanity bleeping, or experimenting with different target lengths per show.)
-->
