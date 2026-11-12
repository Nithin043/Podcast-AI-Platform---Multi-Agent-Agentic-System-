# 🎙️ PodcastAI Platform
## Production Reference Document — v3.0 SaaS Edition
### NCI H9IAPA: Intelligent Agents & Process Automation

> **A fully autonomous, multi-tenant SaaS platform where YouTubers register, connect their publishing accounts, configure content preferences and repeatable task templates, and let an AI-powered multi-agent pipeline automatically detect new uploads, generate repurposed content, and distribute it across every platform — with zero manual effort.**

---

## 📑 Table of Contents

1. [Product Vision](#1-product-vision)
2. [System Architecture](#2-system-architecture)
3. [BPMN Process Design](#3-bpmn-process-design)
4. [Database Design](#4-database-design)
5. [Full Project Structure](#5-full-project-structure)
6. [Complete Tech Stack](#6-complete-tech-stack)
7. [Installation & Setup](#7-installation--setup)
8. [Module Reference](#8-module-reference)
9. [Full Code — Auth System](#9-full-code--auth-system)
   - [auth/models.py](#91-authmodelspy)
   - [auth/register.py](#92-authregisterpy)
   - [auth/login.py](#93-authloginpy)
   - [auth/middleware.py](#94-authmiddlewarepy)
10. [Full Code — Database](#10-full-code--database)
    - [database/db.py](#101-databasedbpy)
    - [database/models.py](#102-databasemodelspy)
11. [Full Code — RPA Bot](#11-full-code--rpa-bot)
    - [rpa_bot/fetch_transcript.py](#111-rpa_botfetch_transcriptpy)
    - [rpa_bot/organise_files.py](#112-rpa_botorganise_filespy)
    - [rpa_bot/log_to_csv.py](#113-rpa_botlog_to_csvpy)
12. [Full Code — Multi-Agent System](#12-full-code--multi-agent-system)
    - [ai_agent/orchestrator.py](#121-ai_agentorchestratorpy)
    - [ai_agent/research_agent.py](#122-ai_agentresearch_agentpy)
    - [ai_agent/writer_agent.py](#123-ai_agentwriter_agentpy)
    - [ai_agent/editor_agent.py](#124-ai_agenteditor_agentpy)
    - [ai_agent/seo_agent.py](#125-ai_agentseo_agentpy)
13. [Full Code — RAG Knowledge Base](#13-full-code--rag-knowledge-base)
    - [ai_agent/rag/embeddings.py](#131-ai_agentragembeddingspy)
    - [ai_agent/rag/vector_store.py](#132-ai_agentragvector_storepy)
    - [ai_agent/rag/retriever.py](#133-ai_agentragretrieverpy)
14. [Full Code — Scheduler](#14-full-code--scheduler)
    - [scheduler/channel_watcher.py](#141-schedulerchannel_watcherpy)
    - [scheduler/job_scheduler.py](#142-schedulerjob_schedulerpy)
    - [scheduler/task_runner.py](#143-schedulertask_runnerpy)
15. [Full Code — Publishers](#15-full-code--publishers)
    - [publisher/wordpress.py](#151-publisherwordpresspy)
    - [publisher/twitter.py](#152-publishertwitterpy)
    - [publisher/mailchimp.py](#153-publishermailchimpy)
16. [Full Code — Preferences Engine](#16-full-code--preferences-engine)
    - [preferences/engine.py](#161-preferencesenginery)
17. [Full Code — Analytics](#17-full-code--analytics)
    - [analytics/dashboard.py](#171-analyticsdashboardpy)
18. [Full Code — Streamlit Pages](#18-full-code--streamlit-pages)
    - [pages/login.py](#181-pagesloginpy)
    - [pages/register.py](#182-pagesregisterpy)
    - [pages/dashboard.py](#183-pagesdashboardpy)
    - [pages/preferences.py](#184-pagespreferencepy)
    - [pages/templates.py](#185-pagestemplatepy)
    - [pages/publishers.py](#186-pagespublisherspy)
    - [pages/episodes.py](#187-pagesepisodespy)
    - [pages/analytics.py](#188-pagesanalyticspy)
19. [Full Code — Entry Points](#19-full-code--entry-points)
    - [app.py](#191-apppy)
    - [main.py](#192-mainpy)
    - [requirements.txt](#193-requirementstxt)
20. [Automation Potential Analysis](#20-automation-potential-analysis)
21. [Multi-Agent Flow Explained](#21-multi-agent-flow-explained)
22. [RAG System Explained](#22-rag-system-explained)
23. [Human-in-the-Loop Design](#23-human-in-the-loop-design)
24. [Security Architecture](#24-security-architecture)
25. [Challenges & Mitigations](#25-challenges--mitigations)
26. [Academic References](#26-academic-references)

---

## 1. Product Vision

### What This Platform Is

PodcastAI is a **multi-tenant SaaS automation platform** purpose-built for YouTube content creators. A creator registers once, connects their YouTube channel and publishing accounts, defines their content preferences and repeatable task templates, and the platform takes over completely — detecting new uploads, generating repurposed content via a multi-agent AI pipeline, and distributing it across every configured platform on a custom schedule.

### The Problem It Solves

| Pain Point | Manual Effort | PodcastAI Solution |
|-----------|--------------|-------------------|
| Transcript extraction | 15–30 min per episode | Automated on upload detection |
| Blog writing | 1–2 hours per episode | AI-generated in 2–4 minutes |
| Social media posts | 30–45 min per episode | Auto-posted on schedule |
| Newsletter writing | 20–30 min per episode | Auto-sent to subscribers |
| File organisation | 10–15 min per episode | RPA bot handles instantly |
| **Total per episode** | **3–5 hours** | **~0 minutes of creator time** |

For a creator publishing weekly, this saves **150–260 hours per year**.

### Who It Is Built For

- Independent podcast creators on YouTube
- Media companies managing multiple shows
- Marketing teams repurposing video content
- News organisations distributing content at scale

### Real-World Comparable Products

| Product | Monthly Price | PodcastAI Advantage |
|---------|--------------|-------------------|
| Buffer | $18/month | Adds AI generation |
| Hootsuite | $99/month | Adds AI + RAG memory |
| Lately.ai | $49/month | Free, local, private |
| Descript | $24/month | Full pipeline automation |

---

## 2. System Architecture

```
╔═════════════════════════════════════════════════════════════════════╗
║                      PODCASTAI PLATFORM                            ║
╠═════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  ┌──────────────────────────────────────────────────────────────┐  ║
║  │               STREAMLIT FRONTEND (8 Pages)                   │  ║
║  │  Login | Register | Dashboard | Preferences | Templates      │  ║
║  │  Publishers | Episodes | Analytics                           │  ║
║  └────────────────────────┬─────────────────────────────────────┘  ║
║                           │                                         ║
║  ┌────────────────────────▼─────────────────────────────────────┐  ║
║  │                    AUTH LAYER (JWT)                          │  ║
║  │  register.py | login.py | middleware.py                      │  ║
║  │  bcrypt passwords | JWT session tokens | per-user isolation  │  ║
║  └────────────────────────┬─────────────────────────────────────┘  ║
║                           │                                         ║
║  ┌────────────────────────▼─────────────────────────────────────┐  ║
║  │                   DATABASE LAYER (SQLite)                    │  ║
║  │  Users | Preferences | Templates | Episodes                  │  ║
║  │  ConnectedPlatforms | RunLog | ScheduledJobs                 │  ║
║  └────────┬──────────────┬──────────────────┬───────────────────┘  ║
║           │              │                  │                       ║
║  ┌────────▼───┐  ┌───────▼──────┐  ┌───────▼──────────────────┐  ║
║  │ SCHEDULER  │  │  PREFERENCES │  │     PIPELINE ENGINE      │  ║
║  │            │  │   ENGINE     │  │                          │  ║
║  │ Channel    │  │              │  │  ┌──────────────────────┐ │  ║
║  │ Watcher    │  │ Per-user     │  │  │     RPA BOT          │ │  ║
║  │ (RSS Poll) │  │ tone, style, │  │  │ fetch → organise     │ │  ║
║  │            │  │ niche, prefs │  │  │ → log               │ │  ║
║  │ Job        │  │              │  │  └──────────┬───────────┘ │  ║
║  │ Scheduler  │  │ Injected     │  │             │             │  ║
║  │ (APSched)  │  │ into every   │  │  ┌──────────▼───────────┐ │  ║
║  │            │  │ agent prompt │  │  │    RAG LAYER         │ │  ║
║  │ Task       │  │              │  │  │ embed → store        │ │  ║
║  │ Runner     │  └──────────────┘  │  │ → retrieve          │ │  ║
║  └────────────┘                    │  └──────────┬───────────┘ │  ║
║                                    │             │             │  ║
║                                    │  ┌──────────▼───────────┐ │  ║
║                                    │  │  MULTI-AGENT SYSTEM  │ │  ║
║                                    │  │ Orchestrator         │ │  ║
║                                    │  │ → Research Agent     │ │  ║
║                                    │  │ → Writer Agent       │ │  ║
║                                    │  │ → Editor Agent       │ │  ║
║                                    │  │ → SEO Agent          │ │  ║
║                                    │  └──────────┬───────────┘ │  ║
║                                    └─────────────┼─────────────┘  ║
║                                                  │                 ║
║  ┌───────────────────────────────────────────────▼──────────────┐  ║
║  │                    PUBLISHER LAYER                           │  ║
║  │  WordPress | Twitter/X | LinkedIn | Mailchimp                │  ║
║  │  Per-user credentials | Schedule-aware | Status logging      │  ║
║  └──────────────────────────────────────────────────────────────┘  ║
║                                                                     ║
╚═════════════════════════════════════════════════════════════════════╝
```

---

## 3. BPMN Process Design

### As-Is Process (Manual — Current State)

```
[START]
   │
   ▼
[Creator publishes podcast episode on YouTube]
   │
   ▼
[Creator manually opens YouTube Studio]
   │
   ▼
[Copies video transcript manually]
── Time: 15–30 min
   │
   ▼
[Opens Google Docs or Word]
   │
   ▼
[Reads through full transcript to understand themes]
── Time: 30–60 min
   │
   ▼
<DECISION: Is this episode worth repurposing?>
   │ YES                                 │ NO
   ▼                                     ▼
[Manually writes blog post]           [PROCESS ENDS — opportunity lost]
── Time: 1–2 hours
   │
   ▼
[Manually writes Twitter thread]
── Time: 15–20 min
   │
   ▼
[Manually writes LinkedIn post]
── Time: 15–20 min
   │
   ▼
[Manually writes newsletter]
── Time: 20–30 min
   │
   ▼
[Logs into WordPress, pastes blog, formats, publishes]
── Time: 15–20 min
   │
   ▼
[Logs into Twitter, posts thread manually]
── Time: 5–10 min
   │
   ▼
[Logs into Mailchimp, pastes newsletter, sends]
── Time: 15–20 min
   │
   ▼
[Saves all files to a local folder — inconsistently]
   │
   ▼
[END]

─────────────────────────────────────────────────
Total Time Per Episode:  3–5 hours
Consistency:             LOW — varies by creator mood/energy
Scalability:             NONE — breaks at 2+ episodes per week
Error Risk:              HIGH — missed platforms, wrong tone
Audit Trail:             NONE — no logging
─────────────────────────────────────────────────
```

---

### To-Be Process (Fully Automated — Future State)

```
[START]
   │
   ▼
[Creator registers on PodcastAI platform]
   │
   ▼
[Onboarding Flow — one time only]
  ├── Connect YouTube channel ID
  ├── Connect WordPress / Twitter / Mailchimp
  ├── Set content preferences (tone, niche, length)
  └── Create repeatable task templates
   │
   ▼
══════════════════ SCHEDULER (Runs continuously) ══════════════
   │
   ▼
[channel_watcher.py polls YouTube RSS every 30 minutes]
   │
   ▼
<DECISION: New video ID found not in Episodes table?>
   │ YES                              │ NO
   ▼                                  ▼
[Trigger task_runner.py           [Sleep → next poll cycle]
 for this user + video]
   │
   ▼
══════════════════ RPA BOT ════════════════════════════════════
   │
   ▼
[fetch_transcript.py: extract video ID, download transcript]
   │
   ▼
<DECISION: English transcript available?>
   │ YES                              │ NO
   ▼                                  ▼
[Fetch metadata via yt-dlp]       [Log failure → notify creator
   │                                via dashboard warning badge]
   ▼                                  │
[organise_files.py: auto-name,        ▼
 create dated folders, move]       [EPISODE ENDS]
   │
   ▼
[log_to_csv.py: append RPA run to per-user run log]
   │
   ▼
══════════════════ RAG LAYER ══════════════════════════════════
   │
   ▼
[embeddings.py: chunk transcript into 500-word segments]
   │
   ▼
[vector_store.py: embed + store in user-isolated ChromaDB]
   │
   ▼
[retriever.py: query for similar past episode content]
   │
   ▼
<DECISION: Relevant past context found?>
   │ YES                              │ NO
   ▼                                  ▼
[Pass context to Orchestrator]    [Continue without context]
   │                                  │
   └──────────────┬───────────────────┘
                  ▼
══════════════════ PREFERENCES ENGINE ════════════════════════
                  │
                  ▼
[preferences/engine.py: load user preferences]
  ├── tone: "formal" / "casual" / "fun"
  ├── length: "short" / "medium" / "long"
  ├── niche_tags: ["tech", "AI", "science"]
  ├── style_sample: "Here is a blog I love..."
  └── active_platforms: ["wordpress", "twitter", "mailchimp"]
                  │
                  ▼
[Inject preferences into every agent system prompt]
                  │
                  ▼
══════════════════ MULTI-AGENT SYSTEM ════════════════════════
                  │
                  ▼
         [ORCHESTRATOR AGENT]
         Plans + coordinates all agents
                  │
         ┌────────┼──────────────┐
         ▼        ▼              ▼
  [RESEARCH]  [WRITER]       assembled
  Extract 5   Blog post      by orchestrator
  topics +    Social posts       │
  web search  Newsletter         ▼
         │        │          [EDITOR]
         └────────┘          Polish + refine
                  │              │
                  ▼              ▼
                         [SEO AGENT]
                         Keywords, meta,
                         slug, H1/H2 structure
                  │
                  ▼
══════════════════ HUMAN-IN-THE-LOOP ═════════════════════════
                  │
                  ▼
[Creator reviews output in dashboard — optional]
                  │
<DECISION: Feedback given?>
   │ YES                              │ NO (auto-approved)
   ▼                                  ▼
[Regenerate with feedback]        [Proceed to publishing]
[Version history tracked]
   │
   ▼
[Creator accepts version]
                  │
                  ▼
══════════════════ PUBLISHER LAYER ═══════════════════════════
                  │
         ┌────────┼──────────────────┐
         ▼        ▼                  ▼
  [WORDPRESS]  [TWITTER]        [MAILCHIMP]
  REST API     API v2           API v3
  POST blog    POST thread      Send newsletter
  Draft or     Immediately      Per schedule
  Publish      or scheduled     (e.g. Tues 8am)
         │        │                  │
         └────────┴──────────────────┘
                  │
                  ▼
[Update Episodes table: publish_status per platform]
                  │
                  ▼
[Update per-user analytics dashboard]
                  │
                  ▼
[END — total elapsed time: 2–5 minutes]

─────────────────────────────────────────────────
Total Creator Time Per Episode:  ~0 minutes
Consistency:                     HIGH — preferences applied always
Scalability:                     UNLIMITED — 1 or 100 episodes/week
Error Risk:                      LOW — logged, retried, alerted
Audit Trail:                     FULL — every action logged
─────────────────────────────────────────────────
```

---

## 4. Database Design

```
╔══════════════════════════════════════════════════════════════╗
║                    DATABASE SCHEMA                           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  users                         preferences                   ║
║  ─────────────────────         ──────────────────────────    ║
║  id          UUID PK           user_id        FK → users     ║
║  username    VARCHAR UNIQUE    blog_tone      VARCHAR        ║
║  email       VARCHAR UNIQUE    blog_length    VARCHAR        ║
║  password_hash VARCHAR         target_audience VARCHAR       ║
║  youtube_channel_id VARCHAR    niche_tags     JSON           ║
║  created_at  DATETIME          style_sample   TEXT           ║
║  is_active   BOOLEAN           updated_at     DATETIME       ║
║                                                              ║
║  connected_platforms           templates                     ║
║  ─────────────────────         ──────────────────────────    ║
║  id          UUID PK           id             UUID PK        ║
║  user_id     FK → users        user_id        FK → users     ║
║  platform    VARCHAR           name           VARCHAR        ║
║  access_token VARCHAR ENC      trigger_type   VARCHAR        ║
║  refresh_token VARCHAR ENC     schedule_cron  VARCHAR        ║
║  platform_url VARCHAR          tasks          JSON           ║
║  is_active   BOOLEAN           is_active      BOOLEAN        ║
║  connected_at DATETIME         created_at     DATETIME       ║
║                                                              ║
║  episodes                      run_log                       ║
║  ─────────────────────         ──────────────────────────    ║
║  id          UUID PK           id             UUID PK        ║
║  user_id     FK → users        user_id        FK → users     ║
║  video_id    VARCHAR UNIQUE    episode_id     FK → episodes  ║
║  title       VARCHAR           run_id         VARCHAR        ║
║  channel     VARCHAR           status         VARCHAR        ║
║  upload_date VARCHAR           blog_generated BOOLEAN        ║
║  transcript_path VARCHAR       social_generated BOOLEAN      ║
║  blog_path   VARCHAR           newsletter_generated BOOLEAN  ║
║  social_path VARCHAR           rag_context_used BOOLEAN      ║
║  newsletter_path VARCHAR       feedback_iterations INT       ║
║  word_count  INTEGER           publish_status JSON           ║
║  publish_status JSON           created_at     DATETIME       ║
║  processed_at DATETIME                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 5. Full Project Structure

```
podcastai/
│
├── auth/
│   ├── __init__.py
│   ├── models.py                  # Pydantic models for auth
│   ├── register.py                # User registration logic
│   ├── login.py                   # Login + JWT token issue
│   └── middleware.py              # JWT validation guard
│
├── database/
│   ├── __init__.py
│   ├── db.py                      # SQLite engine + session factory
│   └── models.py                  # SQLAlchemy table definitions
│
├── rpa_bot/
│   ├── __init__.py
│   ├── fetch_transcript.py        # Download transcript + metadata
│   ├── organise_files.py          # Sort files into dated folders
│   └── log_to_csv.py              # Append run entry to CSV
│
├── ai_agent/
│   ├── __init__.py
│   ├── orchestrator.py            # Coordinate all agents
│   ├── research_agent.py          # Topic extraction + web search
│   ├── writer_agent.py            # Blog, social, newsletter
│   ├── editor_agent.py            # Polish and refine content
│   ├── seo_agent.py               # SEO optimisation
│   └── rag/
│       ├── __init__.py
│       ├── embeddings.py          # Chunk + embed text
│       ├── vector_store.py        # ChromaDB per-user store
│       └── retriever.py           # Query past episode context
│
├── scheduler/
│   ├── __init__.py
│   ├── channel_watcher.py         # Poll YouTube RSS for new videos
│   ├── job_scheduler.py           # APScheduler — per-user jobs
│   └── task_runner.py             # Execute template task sequences
│
├── publisher/
│   ├── __init__.py
│   ├── wordpress.py               # WordPress REST API publisher
│   ├── twitter.py                 # Twitter API v2 publisher
│   └── mailchimp.py               # Mailchimp API v3 publisher
│
├── preferences/
│   ├── __init__.py
│   └── engine.py                  # Load + inject user preferences
│
├── analytics/
│   ├── __init__.py
│   └── dashboard.py               # Per-user metrics + chart data
│
├── pages/
│   ├── login.py                   # Streamlit login page
│   ├── register.py                # Streamlit register page
│   ├── dashboard.py               # Main creator dashboard
│   ├── preferences.py             # Content preferences settings
│   ├── templates.py               # Repeatable task template builder
│   ├── publishers.py              # Connect publishing platforms
│   ├── episodes.py                # Episode history + status
│   └── analytics.py              # Analytics dashboard page
│
├── outputs/
│   ├── {user_id}/
│   │   ├── transcripts/
│   │   ├── blogs/
│   │   ├── social_posts/
│   │   └── newsletters/
│
├── knowledge_base/
│   └── {user_id}/                 # Per-user ChromaDB store
│
├── logs/
│   └── {user_id}_run_log.csv      # Per-user audit log
│
├── app.py                         # Streamlit entry point
├── main.py                        # Headless CLI runner
├── config.py                      # Global config + constants
└── requirements.txt               # All dependencies
```

---

## 6. Complete Tech Stack

| Layer | Technology | Purpose | Cost |
|-------|-----------|---------|------|
| Frontend | Streamlit | 8-page web UI | Free |
| Auth | JWT + bcrypt | Secure sessions + password hashing | Free |
| Database | SQLite → PostgreSQL | User data, preferences, episodes | Free |
| ORM | SQLAlchemy | Database models + queries | Free |
| Transcript | youtube-transcript-api | Download YouTube captions | Free |
| Metadata | yt-dlp | Video info without download | Free |
| File ops | os, shutil, pathlib | Organise output files | Built-in |
| Logging | pandas, csv | Persistent run audit log | Free |
| Web Search | duckduckgo-search | Research Agent queries | Free |
| LLM Runtime | Ollama | Serve local LLMs | Free |
| LLM Model | Mistral-7B-Instruct | All text generation | Free |
| Embeddings | nomic-embed-text (Ollama) | Vector generation for RAG | Free |
| Vector DB | ChromaDB | Per-user knowledge base | Free |
| Scheduler | APScheduler | Per-user cron jobs | Free |
| RSS Polling | feedparser | YouTube channel RSS feed | Free |
| Encryption | cryptography (Fernet) | Encrypt stored API keys | Free |
| Blog Publisher | WordPress REST API | Auto-publish blog posts | Free |
| Social Publisher | Twitter API v2 | Auto-post threads | Free tier |
| Email Publisher | Mailchimp API v3 | Send newsletters | Free tier |
| Analytics | Plotly | Interactive charts | Free |
| Word Cloud | wordcloud + matplotlib | Topic visualisation | Free |
| **Total Cost** | | | **£0** |

---

## 7. Installation & Setup

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 8 GB | 16 GB |
| Disk | 15 GB | 30 GB |
| OS | Windows/macOS/Linux | macOS/Linux |

### Step 1 — Create Project

```bash
mkdir podcastai
cd podcastai
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Install Ollama + Models

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Pull required models
ollama pull mistral           # 4GB — main LLM
ollama pull nomic-embed-text  # 274MB — embeddings

# Verify
ollama list
```

### Step 4 — Initialise Database

```bash
python -c "from database.db import init_db; init_db()"
```

### Step 5 — Create Directory Structure

```bash
mkdir -p outputs logs knowledge_base pages analytics \
         rpa_bot ai_agent/rag scheduler publisher preferences \
         auth database
touch auth/__init__.py database/__init__.py rpa_bot/__init__.py \
      ai_agent/__init__.py ai_agent/rag/__init__.py \
      scheduler/__init__.py publisher/__init__.py \
      preferences/__init__.py analytics/__init__.py
```

### Step 6 — Configure API Credentials

Each user enters their own credentials in the platform UI.
For testing, create a `.env` file:

```bash
# .env (for local testing only — never commit this)
SECRET_KEY=your-jwt-secret-key-min-32-chars
ENCRYPTION_KEY=your-fernet-key-generated-below
```

Generate an encryption key:

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### Step 7 — Run the Platform

```bash
# Full Streamlit UI
streamlit run app.py

# Headless CLI (single video)
python main.py --url "https://youtube.com/watch?v=VIDEO_ID" --user-id "USER_UUID"

# Start scheduler daemon (watches all active users)
python -c "from scheduler.job_scheduler import start_all_schedulers; start_all_schedulers()"
```

---

## 8. Module Reference

### Auth Modules

| Module | Function | Input | Output |
|--------|----------|-------|--------|
| `register.py` | `register_user(username, email, password, channel_id)` | User fields | `{success, user_id, message}` |
| `login.py` | `login_user(email, password)` | Credentials | `{success, token, user_id}` |
| `middleware.py` | `validate_token(token)` | JWT string | User dict or None |
| `middleware.py` | `get_current_user(token)` | JWT string | User ORM object |

### Scheduler Modules

| Module | Function | Input | Output |
|--------|----------|-------|--------|
| `channel_watcher.py` | `check_for_new_videos(user)` | User ORM object | List of new video IDs |
| `job_scheduler.py` | `schedule_user(user_id)` | User UUID | None |
| `job_scheduler.py` | `start_all_schedulers()` | None | None |
| `task_runner.py` | `run_for_user(user_id, video_url)` | User ID + URL | Results dict |

### Publisher Modules

| Module | Function | Input | Output |
|--------|----------|-------|--------|
| `wordpress.py` | `publish_post(blog, metadata, credentials)` | Content + creds | `{success, post_url}` |
| `twitter.py` | `post_thread(tweets, credentials)` | Tweet list + creds | `{success, tweet_ids}` |
| `mailchimp.py` | `send_campaign(newsletter, metadata, credentials)` | Content + creds | `{success, campaign_id}` |

---

## 9. Full Code — Auth System

### 9.1 `auth/models.py`

```python
"""
auth/models.py
--------------
Pydantic models for auth request/response validation.
Used by register.py and login.py for input sanitisation.
"""

from pydantic import BaseModel, EmailStr, validator
import re


class RegisterRequest(BaseModel):
    username:           str
    email:              EmailStr
    password:           str
    youtube_channel_id: str

    @validator("username")
    def username_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', v):
            raise ValueError("Username must be 3-30 chars, alphanumeric or underscore")
        return v.lower()

    @validator("password")
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    success:  bool
    token:    str = ""
    user_id:  str = ""
    username: str = ""
    message:  str = ""
```

---

### 9.2 `auth/register.py`

```python
"""
auth/register.py
----------------
User registration logic.
Hashes password with bcrypt, creates user record in SQLite.
Returns success flag and new user_id.
"""

import bcrypt
import uuid
from datetime import datetime
from database.db import get_session
from database.models import User


def hash_password(password: str) -> str:
    """Hash a plain-text password with bcrypt (12 rounds)."""
    salt   = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def register_user(
    username: str,
    email: str,
    password: str,
    youtube_channel_id: str,
) -> dict:
    """
    Register a new user.

    Steps:
      1. Check username and email are not already taken
      2. Hash password with bcrypt
      3. Create User record in database
      4. Return success with new user_id

    Returns:
        dict: {success, user_id, message}
    """
    session = get_session()
    try:
        # Check for existing username
        existing_username = session.query(User).filter_by(
            username=username.lower()
        ).first()
        if existing_username:
            return {"success": False, "user_id": "", "message": "Username already taken"}

        # Check for existing email
        existing_email = session.query(User).filter_by(email=email.lower()).first()
        if existing_email:
            return {"success": False, "user_id": "", "message": "Email already registered"}

        # Create new user
        new_user = User(
            id=str(uuid.uuid4()),
            username=username.lower(),
            email=email.lower(),
            password_hash=hash_password(password),
            youtube_channel_id=youtube_channel_id.strip(),
            created_at=datetime.utcnow(),
            is_active=True,
        )

        session.add(new_user)
        session.commit()

        print(f"[Auth] ✅ New user registered: {username} ({new_user.id})")
        return {
            "success": True,
            "user_id": new_user.id,
            "message": "Registration successful",
        }

    except Exception as e:
        session.rollback()
        print(f"[Auth] ❌ Registration error: {e}")
        return {"success": False, "user_id": "", "message": f"Registration failed: {e}"}
    finally:
        session.close()
```

---

### 9.3 `auth/login.py`

```python
"""
auth/login.py
-------------
Login logic with JWT token generation.
Verifies bcrypt password hash and issues a signed JWT.
"""

import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from database.db import get_session
from database.models import User


SECRET_KEY    = os.getenv("SECRET_KEY", "change-this-in-production-min-32-chars")
TOKEN_EXPIRY  = timedelta(hours=24)
ALGORITHM     = "HS256"


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_token(user_id: str, username: str) -> str:
    """Create a signed JWT token with 24-hour expiry."""
    payload = {
        "user_id":  user_id,
        "username": username,
        "exp":      datetime.utcnow() + TOKEN_EXPIRY,
        "iat":      datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def login_user(email: str, password: str) -> dict:
    """
    Authenticate a user by email and password.

    Steps:
      1. Look up user by email
      2. Verify bcrypt password hash
      3. Issue JWT token

    Returns:
        dict: {success, token, user_id, username, message}
    """
    session = get_session()
    try:
        user = session.query(User).filter_by(email=email.lower()).first()

        if not user:
            return {"success": False, "token": "", "message": "Email not found"}

        if not user.is_active:
            return {"success": False, "token": "", "message": "Account is inactive"}

        if not verify_password(password, user.password_hash):
            return {"success": False, "token": "", "message": "Incorrect password"}

        token = create_token(user.id, user.username)

        print(f"[Auth] ✅ Login: {user.username}")
        return {
            "success":  True,
            "token":    token,
            "user_id":  user.id,
            "username": user.username,
            "message":  "Login successful",
        }

    except Exception as e:
        print(f"[Auth] ❌ Login error: {e}")
        return {"success": False, "token": "", "message": f"Login failed: {e}"}
    finally:
        session.close()
```

---

### 9.4 `auth/middleware.py`

```python
"""
auth/middleware.py
------------------
JWT validation middleware.
Used to protect all authenticated routes and Streamlit pages.
"""

import jwt
import os
from datetime import datetime
from database.db import get_session
from database.models import User


SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production-min-32-chars")
ALGORITHM  = "HS256"


def validate_token(token: str) -> dict | None:
    """
    Decode and validate a JWT token.
    Returns payload dict if valid, None if expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Check expiry
        if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user(token: str):
    """
    Validate token and return the full User ORM object.
    Returns None if token is invalid or user not found.
    """
    payload = validate_token(token)
    if not payload:
        return None

    session = get_session()
    try:
        user = session.query(User).filter_by(id=payload["user_id"]).first()
        return user
    finally:
        session.close()


def require_auth(session_state) -> bool:
    """
    Streamlit page guard. Call at the top of every protected page.
    Returns True if authenticated, False if not (redirects to login).
    """
    token = session_state.get("token", "")
    if not token or not validate_token(token):
        session_state["authenticated"] = False
        return False
    session_state["authenticated"] = True
    return True
```

---

## 10. Full Code — Database

### 10.1 `database/db.py`

```python
"""
database/db.py
--------------
SQLite database engine and session factory.
Uses SQLAlchemy ORM. Initialises all tables on first run.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///podcastai.db")

engine         = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal   = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base           = declarative_base()


def get_session():
    """Return a new database session."""
    return SessionLocal()


def init_db():
    """Create all tables if they do not exist."""
    from database import models  # noqa — import to register models
    Base.metadata.create_all(bind=engine)
    print("[DB] ✅ Database initialised")
```

---

### 10.2 `database/models.py`

```python
"""
database/models.py
------------------
SQLAlchemy ORM table definitions.
All tables are user-scoped for full multi-tenant isolation.
"""

from sqlalchemy import (
    Column, String, Boolean, Integer,
    DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id                   = Column(String, primary_key=True)
    username             = Column(String, unique=True, nullable=False)
    email                = Column(String, unique=True, nullable=False)
    password_hash        = Column(String, nullable=False)
    youtube_channel_id   = Column(String, nullable=False)
    created_at           = Column(DateTime, default=datetime.utcnow)
    is_active            = Column(Boolean, default=True)

    preferences          = relationship("Preferences",     back_populates="user", uselist=False)
    connected_platforms  = relationship("ConnectedPlatform", back_populates="user")
    templates            = relationship("Template",        back_populates="user")
    episodes             = relationship("Episode",         back_populates="user")


class Preferences(Base):
    __tablename__ = "preferences"

    id               = Column(String, primary_key=True)
    user_id          = Column(String, ForeignKey("users.id"), unique=True)
    blog_tone        = Column(String, default="professional")
    blog_length      = Column(String, default="medium")
    target_audience  = Column(String, default="general")
    niche_tags       = Column(JSON,   default=list)
    style_sample     = Column(Text,   default="")
    updated_at       = Column(DateTime, default=datetime.utcnow)

    user             = relationship("User", back_populates="preferences")


class ConnectedPlatform(Base):
    __tablename__ = "connected_platforms"

    id             = Column(String, primary_key=True)
    user_id        = Column(String, ForeignKey("users.id"))
    platform       = Column(String, nullable=False)   # wordpress|twitter|mailchimp
    access_token   = Column(Text,   default="")       # AES encrypted
    refresh_token  = Column(Text,   default="")       # AES encrypted
    platform_url   = Column(String, default="")       # For WordPress site URL
    is_active      = Column(Boolean, default=True)
    connected_at   = Column(DateTime, default=datetime.utcnow)

    user           = relationship("User", back_populates="connected_platforms")


class Template(Base):
    __tablename__ = "templates"

    id            = Column(String, primary_key=True)
    user_id       = Column(String, ForeignKey("users.id"))
    name          = Column(String, nullable=False)
    trigger_type  = Column(String, default="new_upload")  # new_upload|scheduled
    schedule_cron = Column(String, default="")            # cron expression
    tasks         = Column(JSON,   default=dict)          # {blog, twitter, mailchimp, delays}
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime, default=datetime.utcnow)

    user          = relationship("User", back_populates="templates")


class Episode(Base):
    __tablename__ = "episodes"

    id                = Column(String, primary_key=True)
    user_id           = Column(String, ForeignKey("users.id"))
    video_id          = Column(String, nullable=False)
    title             = Column(String, default="")
    channel           = Column(String, default="")
    upload_date       = Column(String, default="")
    transcript_path   = Column(String, default="")
    blog_path         = Column(String, default="")
    social_path       = Column(String, default="")
    newsletter_path   = Column(String, default="")
    word_count        = Column(Integer, default=0)
    publish_status    = Column(JSON, default=dict)   # {wordpress: True, twitter: False}
    processed_at      = Column(DateTime, default=datetime.utcnow)

    user              = relationship("User", back_populates="episodes")


class RunLog(Base):
    __tablename__ = "run_log"

    id                    = Column(String, primary_key=True)
    user_id               = Column(String, ForeignKey("users.id"))
    episode_id            = Column(String, ForeignKey("episodes.id"), nullable=True)
    run_id                = Column(String, default="")
    status                = Column(String, default="SUCCESS")
    blog_generated        = Column(Boolean, default=False)
    social_generated      = Column(Boolean, default=False)
    newsletter_generated  = Column(Boolean, default=False)
    rag_context_used      = Column(Boolean, default=False)
    feedback_iterations   = Column(Integer, default=0)
    publish_status        = Column(JSON,    default=dict)
    created_at            = Column(DateTime, default=datetime.utcnow)
```

---

## 11. Full Code — RPA Bot

### 11.1 `rpa_bot/fetch_transcript.py`

```python
"""
fetch_transcript.py
-------------------
RPA Bot — Step 1
Downloads transcript and metadata from YouTube.
User-scoped: saves to outputs/{user_id}/transcripts/
"""

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import yt_dlp, os, re
from datetime import datetime


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/")
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/shorts/")[1]
    raise ValueError(f"Cannot extract video ID from: {url}")


def sanitise_filename(title: str) -> str:
    title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")
    return title[:80].strip("_")


def fetch_metadata(url: str) -> dict:
    ydl_opts = {"quiet": True, "skip_download": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    raw_date = info.get("upload_date", "unknown")
    formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}" if raw_date != "unknown" else "unknown"
    return {
        "title":        info.get("title", "Unknown Title"),
        "channel":      info.get("uploader", "Unknown Channel"),
        "upload_date":  formatted_date,
        "duration_sec": info.get("duration", 0),
        "duration_min": round(info.get("duration", 0) / 60, 2),
        "url":          url,
        "video_id":     info.get("id", extract_video_id(url)),
        "fetched_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def fetch_transcript(video_id: str) -> str:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    try:
        transcript = transcript_list.find_manually_created_transcript(["en"])
    except Exception:
        transcript = transcript_list.find_generated_transcript(["en"])
    entries   = transcript.fetch()
    full_text = " ".join(
        entry.get("text", "") if isinstance(entry, dict) else str(entry)
        for entry in entries
    )
    return re.sub(r'\s+', ' ', full_text).strip()


def save_transcript(transcript: str, metadata: dict, user_id: str) -> str:
    output_dir = os.path.join("outputs", user_id, "transcripts")
    os.makedirs(output_dir, exist_ok=True)
    safe     = sanitise_filename(metadata["title"])
    date_str = metadata["upload_date"].replace("-", "")
    filepath = os.path.join(output_dir, f"{date_str}_{safe}.txt")
    content  = (
        f"TITLE:      {metadata['title']}\n"
        f"CHANNEL:    {metadata['channel']}\n"
        f"DATE:       {metadata['upload_date']}\n"
        f"DURATION:   {metadata['duration_min']} minutes\n"
        f"URL:        {metadata['url']}\n"
        f"FETCHED AT: {metadata['fetched_at']}\n"
        f"{'─' * 60}\n\n{transcript}\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def run(url: str, user_id: str) -> dict:
    """Master fetch function scoped to a specific user."""
    print(f"\n[RPA] Fetching transcript for user {user_id[:8]}...")
    metadata        = fetch_metadata(url)
    transcript      = fetch_transcript(metadata["video_id"])
    transcript_path = save_transcript(transcript, metadata, user_id)
    print(f"[RPA] ✅ Saved → {transcript_path}")
    return {"metadata": metadata, "transcript": transcript, "transcript_path": transcript_path}
```

---

### 11.2 `rpa_bot/organise_files.py`

```python
"""
organise_files.py
-----------------
RPA Bot — Step 2
Moves files into user-scoped YYYY/MM folder structure.
"""

import os, shutil
from datetime import datetime


def run(filepath: str, metadata: dict, user_id: str) -> str:
    upload_date = metadata.get("upload_date", "")
    try:
        dt    = datetime.strptime(upload_date, "%Y-%m-%d")
        year  = dt.strftime("%Y")
        month = dt.strftime("%m_%B")
    except (ValueError, TypeError):
        year  = datetime.now().strftime("%Y")
        month = datetime.now().strftime("%m_%B")

    dest_dir = os.path.join("outputs", user_id, "transcripts", year, month)
    os.makedirs(dest_dir, exist_ok=True)

    filename     = os.path.basename(filepath)
    new_filepath = os.path.join(dest_dir, filename)

    if os.path.exists(new_filepath):
        base, ext    = os.path.splitext(filename)
        ts           = datetime.now().strftime("%H%M%S")
        new_filepath = os.path.join(dest_dir, f"{base}_{ts}{ext}")

    shutil.move(filepath, new_filepath)
    print(f"[RPA] ✅ Organised → {new_filepath}")
    return new_filepath
```

---

### 11.3 `rpa_bot/log_to_csv.py`

```python
"""
log_to_csv.py
-------------
RPA Bot — Step 3
Per-user CSV audit logging.
Each user has their own run_log CSV in logs/{user_id}_run_log.csv
"""

import csv, os
from datetime import datetime

HEADERS = [
    "run_id", "timestamp", "video_title", "channel",
    "upload_date", "duration_min", "url", "video_id",
    "transcript_path", "word_count", "blog_generated",
    "social_generated", "newsletter_generated",
    "rag_context_used", "feedback_iterations", "status",
]


def get_log_path(user_id: str) -> str:
    os.makedirs("logs", exist_ok=True)
    return f"logs/{user_id}_run_log.csv"


def ensure_log(log_path: str) -> None:
    if not os.path.exists(log_path):
        with open(log_path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=HEADERS).writeheader()


def run(
    user_id: str,
    metadata: dict,
    transcript_path: str,
    transcript: str,
    blog_generated: bool = False,
    social_generated: bool = False,
    newsletter_generated: bool = False,
    rag_context_used: bool = False,
    feedback_iterations: int = 0,
    status: str = "SUCCESS",
) -> str:
    """Append run entry to user-specific CSV. Returns run_id."""
    log_path = get_log_path(user_id)
    ensure_log(log_path)

    run_id = f"RUN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    row    = {
        "run_id":               run_id,
        "timestamp":            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "video_title":          metadata.get("title", ""),
        "channel":              metadata.get("channel", ""),
        "upload_date":          metadata.get("upload_date", ""),
        "duration_min":         metadata.get("duration_min", 0),
        "url":                  metadata.get("url", ""),
        "video_id":             metadata.get("video_id", ""),
        "transcript_path":      transcript_path,
        "word_count":           len(transcript.split()) if transcript else 0,
        "blog_generated":       blog_generated,
        "social_generated":     social_generated,
        "newsletter_generated": newsletter_generated,
        "rag_context_used":     rag_context_used,
        "feedback_iterations":  feedback_iterations,
        "status":               status,
    }
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS).writerow(row)
    return run_id


def read_log(user_id: str) -> list:
    log_path = get_log_path(user_id)
    if not os.path.exists(log_path):
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```

---

## 12. Full Code — Multi-Agent System

### 12.1 `ai_agent/orchestrator.py`

```python
"""
orchestrator.py
---------------
AI Agent — Orchestrator
Coordinates all specialist agents.
Accepts user preferences to personalise every output.
"""

from ai_agent import research_agent, writer_agent, editor_agent, seo_agent
import os, re


def run(
    transcript: str,
    metadata: dict,
    user_id: str,
    preferences: dict,
    rag_context: str = "",
    feedback: str = "",
    previous_blog: str = "",
) -> dict:
    """
    Orchestrate full multi-agent pipeline for a specific user.

    Args:
        transcript:    Full podcast transcript
        metadata:      Video metadata dict
        user_id:       Owner user UUID (for scoped file saving)
        preferences:   User preference dict (tone, niche, length, etc.)
        rag_context:   Retrieved past episode context
        feedback:      Human feedback for regeneration
        previous_blog: Previous version for feedback loop

    Returns:
        Full results dict with all content and file paths
    """
    print(f"\n[Orchestrator] Starting pipeline for user {user_id[:8]}")
    results = {}

    # Step 1 — Research
    research_result     = research_agent.run(transcript, metadata)
    results["topics"]   = research_result.get("topics", [])
    results["research"] = research_result.get("research", [])

    # Step 2 — Write (with preferences injected)
    writer_result = writer_agent.run(
        transcript=transcript, topics=results["topics"],
        research=results["research"], metadata=metadata,
        preferences=preferences, rag_context=rag_context,
        feedback=feedback, previous_blog=previous_blog,
    )
    results.update(writer_result)

    # Step 3 — Edit
    results["blog"]       = editor_agent.run(results.get("blog", ""), "blog")
    results["newsletter"] = editor_agent.run(results.get("newsletter", ""), "newsletter")

    # Step 4 — SEO
    seo_result              = seo_agent.run(results["blog"], results["topics"])
    results["blog"]         = seo_result.get("optimised_content", results["blog"])
    results["meta_description"] = seo_result.get("meta_description", "")
    results["keywords"]     = seo_result.get("keywords", [])
    results["url_slug"]     = seo_result.get("url_slug", "")

    # Save all outputs (user-scoped)
    results.update(_save_outputs(results, metadata, user_id))

    print(f"[Orchestrator] ✅ Complete for user {user_id[:8]}")
    return results


def _save_outputs(results: dict, metadata: dict, user_id: str) -> dict:
    """Save all content to user-scoped output folders."""
    paths = {}

    def safe_name(suffix, ext):
        title = metadata.get("title", "output")
        s     = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "_")[:60]
        d     = metadata.get("upload_date", "unknown").replace("-", "")
        return f"{d}_{s}_{suffix}.{ext}"

    for content_key, folder, suffix, ext in [
        ("blog",       "blogs",        "blog",       "md"),
        ("newsletter", "newsletters",  "newsletter", "txt"),
    ]:
        if results.get(content_key):
            path = os.path.join("outputs", user_id, folder, safe_name(suffix, ext))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(results[content_key])
            paths[f"{content_key}_path"] = path

    if results.get("social_posts"):
        path  = os.path.join("outputs", user_id, "social_posts", safe_name("social", "txt"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        posts = results["social_posts"]
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                f"TWITTER\n{'─'*40}\n{posts.get('twitter','')}\n\n"
                f"LINKEDIN\n{'─'*40}\n{posts.get('linkedin','')}\n\n"
                f"INSTAGRAM\n{'─'*40}\n{posts.get('instagram','')}\n"
            )
        paths["social_path"] = path

    return paths
```

---

### 12.2 `ai_agent/research_agent.py`

```python
"""
research_agent.py
-----------------
AI Agent — Research Specialist
Extracts topics from transcript, searches DuckDuckGo for each,
and summarises results for the Writer Agent.
"""

import ollama, json, re
from duckduckgo_search import DDGS

MODEL = "mistral"

TOPIC_PROMPT = """
Extract exactly 5 key topics from this podcast transcript.
Respond ONLY with a valid JSON array. No preamble. No markdown.

[{"topic": "Name", "description": "One sentence", "search_query": "short query"}, ...]
"""

SUMMARISE_PROMPT = """
You are a research assistant. Summarise this web snippet in 2-3 sentences.
Focus only on facts, statistics, and expert opinions. No fluff.
"""


def extract_topics(transcript: str) -> list:
    excerpt  = " ".join(transcript.split()[:3000])
    response = ollama.chat(model=MODEL, messages=[
        {"role": "system", "content": TOPIC_PROMPT},
        {"role": "user",   "content": f"TRANSCRIPT:\n{excerpt}"},
    ])
    raw = re.sub(r"```json|```", "", response["message"]["content"]).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [{"topic": "Main Topic", "description": raw[:100], "search_query": "podcast"}]


def search_web(query: str) -> list:
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception:
        return []


def summarise(snippet: str) -> str:
    if not snippet:
        return ""
    try:
        response = ollama.chat(model=MODEL, messages=[
            {"role": "system", "content": SUMMARISE_PROMPT},
            {"role": "user",   "content": snippet[:800]},
        ])
        return response["message"]["content"].strip()
    except Exception:
        return snippet[:200]


def run(transcript: str, metadata: dict) -> dict:
    topics   = extract_topics(transcript)
    research = []
    for topic in topics:
        results  = search_web(topic.get("search_query", topic["topic"]))
        sources  = [{"title": r.get("title",""), "summary": summarise(r.get("body","")), "url": r.get("href","")} for r in results]
        research.append({"topic": topic["topic"], "sources": sources})
        print(f"[Research] ✅ {topic['topic']} — {len(sources)} sources")
    return {"topics": topics, "research": research}
```

---

### 12.3 `ai_agent/writer_agent.py`

```python
"""
writer_agent.py
---------------
AI Agent — Writer Specialist
Generates blog, social posts, and newsletter.
Injects user preferences into every system prompt.
"""

import ollama, json, re


MODEL = "mistral"


def _build_preference_context(preferences: dict) -> str:
    """Format user preferences into a natural language instruction block."""
    if not preferences:
        return ""
    tone     = preferences.get("blog_tone", "professional")
    length   = preferences.get("blog_length", "medium")
    audience = preferences.get("target_audience", "general")
    niche    = ", ".join(preferences.get("niche_tags", []))
    sample   = preferences.get("style_sample", "")

    ctx = (
        f"\nUSER PREFERENCES (apply these strictly):\n"
        f"- Tone: {tone}\n"
        f"- Length: {length}\n"
        f"- Target Audience: {audience}\n"
    )
    if niche:
        ctx += f"- Content Niche: {niche}\n"
    if sample:
        ctx += f"- Style to emulate:\n{sample[:500]}\n"
    return ctx


def generate_blog(transcript, topics, research, metadata, preferences, rag_context, feedback, previous_blog) -> str:
    pref_ctx     = _build_preference_context(preferences)
    topic_names  = ", ".join(t.get("topic", "") for t in topics)
    research_ctx = "\n".join(f"- {s['summary']}" for item in research for s in item.get("sources", [])[:2])
    excerpt      = " ".join(transcript.split()[:2000])
    feedback_sec = f"\n\nPREVIOUS VERSION:\n{previous_blog[:1000]}\n\nFEEDBACK: {feedback}\nRewrite incorporating this." if feedback and previous_blog else ""
    rag_sec      = f"\n\nRELEVANT PAST EPISODES:\n{rag_context}" if rag_context else ""

    system = f"""You are a professional blog writer.{pref_ctx}
Write a structured blog post in markdown with: H1 title, intro, 3-4 H2 sections, conclusion, CTA."""

    user = f"PODCAST: {metadata.get('title','')}\nTOPICS: {topic_names}\nRESEARCH:\n{research_ctx}{rag_sec}\nTRANSCRIPT:\n{excerpt}{feedback_sec}"

    r = ollama.chat(model=MODEL, messages=[{"role":"system","content":system},{"role":"user","content":user}])
    return r["message"]["content"].strip()


def generate_social(transcript, topics, metadata, preferences) -> dict:
    pref_ctx    = _build_preference_context(preferences)
    topic_names = ", ".join(t.get("topic","") for t in topics)
    excerpt     = " ".join(transcript.split()[:800])

    system = f"""You are a social media expert.{pref_ctx}
Respond ONLY with valid JSON: {{"twitter":"...","linkedin":"...","instagram":"..."}}"""

    user = f"PODCAST: {metadata.get('title','')}\nTOPICS: {topic_names}\nTRANSCRIPT:\n{excerpt}"
    r    = ollama.chat(model=MODEL, messages=[{"role":"system","content":system},{"role":"user","content":user}])
    raw  = re.sub(r"```json|```","",r["message"]["content"]).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"twitter": raw, "linkedin": raw, "instagram": raw}


def generate_newsletter(transcript, topics, metadata, preferences, rag_context) -> str:
    pref_ctx    = _build_preference_context(preferences)
    topic_names = ", ".join(t.get("topic","") for t in topics)
    excerpt     = " ".join(transcript.split()[:1000])
    rag_sec     = f"\nPAST CONTEXT:\n{rag_context}" if rag_context else ""

    system = f"""You are a newsletter writer.{pref_ctx}
Write exactly 150-200 words in flowing prose. No bullet points. Second person voice."""

    user = f"PODCAST: {metadata.get('title','')}\nTOPICS: {topic_names}{rag_sec}\nTRANSCRIPT:\n{excerpt}"
    r    = ollama.chat(model=MODEL, messages=[{"role":"system","content":system},{"role":"user","content":user}])
    return r["message"]["content"].strip()


def run(transcript, topics, research, metadata, preferences, rag_context="", feedback="", previous_blog="") -> dict:
    print("[Writer] ✍️ Generating all content...")
    return {
        "blog":         generate_blog(transcript, topics, research, metadata, preferences, rag_context, feedback, previous_blog),
        "social_posts": generate_social(transcript, topics, metadata, preferences),
        "newsletter":   generate_newsletter(transcript, topics, metadata, preferences, rag_context),
    }
```

---

### 12.4 `ai_agent/editor_agent.py`

```python
"""
editor_agent.py
---------------
AI Agent — Editor Specialist
Polishes grammar, flow, tone consistency, and readability.
"""

import ollama

MODEL = "mistral"

PROMPTS = {
    "blog": "You are a senior editor. Fix grammar, improve flow, strengthen hooks and CTAs. Return only the improved markdown.",
    "newsletter": "You are a newsletter editor. Fix grammar, ensure 150-200 words, smooth prose. Return only the improved text.",
}


def run(content: str, content_type: str = "blog") -> str:
    if not content or len(content.strip()) < 50:
        return content
    system = PROMPTS.get(content_type, PROMPTS["blog"])
    r      = ollama.chat(model=MODEL, messages=[
        {"role": "system", "content": system},
        {"role": "user",   "content": content},
    ])
    return r["message"]["content"].strip()
```

---

### 12.5 `ai_agent/seo_agent.py`

```python
"""
seo_agent.py
------------
AI Agent — SEO Specialist
Optimises blog post for search: keywords, meta, slug, H1/H2 structure.
"""

import ollama, json, re

MODEL = "mistral"

SYSTEM = """
You are an SEO expert. Optimise the blog post and return ONLY valid JSON:
{
  "optimised_content": "full markdown blog",
  "meta_description": "150-160 char meta description",
  "url_slug": "clean-url-slug",
  "keywords": ["kw1","kw2","kw3","kw4","kw5"],
  "internal_links": ["anchor1","anchor2","anchor3"]
}
"""


def run(blog: str, topics: list) -> dict:
    topic_names = ", ".join(t.get("topic","") for t in topics)
    r   = ollama.chat(model=MODEL, messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": f"KEYWORDS: {topic_names}\n\nBLOG:\n{blog}"},
    ])
    raw = re.sub(r"```json|```","",r["message"]["content"]).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"optimised_content": blog, "meta_description": "", "url_slug": "episode", "keywords": [], "internal_links": []}
```

---

## 13. Full Code — RAG Knowledge Base

### 13.1 `ai_agent/rag/embeddings.py`

```python
"""
embeddings.py — Chunk and embed transcript text using nomic-embed-text via Ollama.
"""

import ollama

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50
EMBED_MODEL   = "nomic-embed-text"


def chunk_text(text: str) -> list:
    words, chunks, start = text.split(), [], 0
    while start < len(words):
        end = min(start + CHUNK_SIZE, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words): break
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def embed_text(text: str) -> list:
    try:
        return ollama.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]
    except Exception:
        return []


def embed_chunks(chunks: list) -> list:
    return [embed_text(c) for c in chunks]
```

---

### 13.2 `ai_agent/rag/vector_store.py`

```python
"""
vector_store.py — Per-user ChromaDB persistent vector store.
Each user has an isolated collection: f"user_{user_id}"
"""

import chromadb
from ai_agent.rag.embeddings import chunk_text, embed_chunks
from datetime import datetime


def get_collection(user_id: str):
    client = chromadb.PersistentClient(path=f"knowledge_base/{user_id}")
    return client.get_or_create_collection(name=f"user_{user_id[:8]}", metadata={"hnsw:space": "cosine"})


def store_episode(transcript: str, metadata: dict, user_id: str) -> int:
    collection = get_collection(user_id)
    chunks     = chunk_text(transcript)
    embeddings = embed_chunks(chunks)
    video_id   = metadata.get("video_id", datetime.now().strftime("%Y%m%d%H%M%S"))

    valid = [(f"{video_id}_chunk_{i}", chunks[i], embeddings[i],
              {"video_id": video_id, "title": metadata.get("title",""), "chunk_index": i})
             for i in range(len(chunks)) if embeddings[i]]

    if valid:
        ids, docs, embs, metas = zip(*valid)
        collection.add(ids=list(ids), documents=list(docs), embeddings=list(embs), metadatas=list(metas))
    return len(valid)


def get_stats(user_id: str) -> dict:
    try:
        return {"total_chunks": get_collection(user_id).count(), "status": "connected"}
    except Exception as e:
        return {"total_chunks": 0, "status": f"error: {e}"}
```

---

### 13.3 `ai_agent/rag/retriever.py`

```python
"""
retriever.py — Query user-scoped ChromaDB for relevant past episode content.
"""

import chromadb
from ai_agent.rag.embeddings import embed_text


def run(topics: list, user_id: str, current_video_id: str = "") -> str:
    try:
        client     = chromadb.PersistentClient(path=f"knowledge_base/{user_id}")
        collection = client.get_or_create_collection(name=f"user_{user_id[:8]}")
        if collection.count() == 0:
            return ""
    except Exception:
        return ""

    contexts, seen = [], set()
    for topic in topics[:3]:
        query_emb = embed_text(f"{topic.get('topic','')} {topic.get('description','')}")
        if not query_emb: continue
        try:
            results = collection.query(query_embeddings=[query_emb], n_results=min(5, collection.count()),
                                       include=["documents","metadatas","distances"])
            for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
                if meta.get("video_id") == current_video_id: continue
                key = f"{meta.get('video_id')}_{meta.get('chunk_index')}"
                if key in seen or dist > 0.4: continue
                seen.add(key)
                contexts.append(f"[From '{meta.get('title','Past Episode')}']:\n{doc}")
        except Exception:
            continue

    return "\n\n".join(contexts[:4])
```

---

## 14. Full Code — Scheduler

### 14.1 `scheduler/channel_watcher.py`

```python
"""
channel_watcher.py
------------------
Polls YouTube RSS feed for each active user's channel.
YouTube exposes a public RSS feed per channel — no API key needed.
RSS URL: https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
"""

import feedparser
import os
from database.db import get_session
from database.models import User, Episode


RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def get_latest_videos(channel_id: str, max_results: int = 5) -> list:
    """
    Fetch latest video entries from YouTube RSS feed.
    Returns list of dicts: {video_id, title, url, published}
    """
    url  = RSS_URL.format(channel_id=channel_id)
    feed = feedparser.parse(url)

    videos = []
    for entry in feed.entries[:max_results]:
        video_id = entry.get("yt_videoid", "")
        if video_id:
            videos.append({
                "video_id":  video_id,
                "title":     entry.get("title", ""),
                "url":       f"https://www.youtube.com/watch?v={video_id}",
                "published": entry.get("published", ""),
            })
    return videos


def check_for_new_videos(user) -> list:
    """
    Check if there are any new videos for a user that have not
    yet been processed. Returns list of new video dicts.
    """
    if not user.youtube_channel_id:
        return []

    try:
        latest   = get_latest_videos(user.youtube_channel_id)
        session  = get_session()

        new_videos = []
        for video in latest:
            # Check if this video_id has already been processed for this user
            existing = session.query(Episode).filter_by(
                user_id=user.id,
                video_id=video["video_id"]
            ).first()
            if not existing:
                new_videos.append(video)

        session.close()
        if new_videos:
            print(f"[Watcher] ✅ {len(new_videos)} new video(s) for {user.username}")
        return new_videos

    except Exception as e:
        print(f"[Watcher] ⚠️ Error checking {user.username}: {e}")
        return []


def check_all_users() -> dict:
    """
    Check all active users for new videos.
    Returns dict: {user_id: [new_video_dicts]}
    """
    session  = get_session()
    users    = session.query(User).filter_by(is_active=True).all()
    session.close()

    results = {}
    for user in users:
        new_videos = check_for_new_videos(user)
        if new_videos:
            results[user.id] = new_videos

    return results
```

---

### 14.2 `scheduler/job_scheduler.py`

```python
"""
job_scheduler.py
----------------
APScheduler-based per-user job scheduler.
Each user gets their own polling job based on their template settings.
Default: check for new videos every 30 minutes.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from scheduler.channel_watcher import check_for_new_videos
from scheduler.task_runner import run_for_user
from database.db import get_session
from database.models import User, Template
import atexit

scheduler = BackgroundScheduler()


def _poll_user(user_id: str) -> None:
    """Job function: check user for new videos and trigger pipeline."""
    session = get_session()
    try:
        user = session.query(User).filter_by(id=user_id, is_active=True).first()
        if not user:
            return

        new_videos = check_for_new_videos(user)
        for video in new_videos:
            print(f"[Scheduler] New video for {user.username}: {video['title'][:50]}")
            run_for_user(user_id=user_id, video_url=video["url"])

    except Exception as e:
        print(f"[Scheduler] ❌ Poll error for {user_id[:8]}: {e}")
    finally:
        session.close()


def schedule_user(user_id: str, interval_minutes: int = 30) -> None:
    """Add or replace a polling job for a specific user."""
    job_id = f"poll_user_{user_id}"

    # Remove existing job if present
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        func=_poll_user,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id=job_id,
        args=[user_id],
        name=f"Channel watcher — {user_id[:8]}",
        replace_existing=True,
        misfire_grace_time=60,
    )
    print(f"[Scheduler] ✅ Scheduled user {user_id[:8]} every {interval_minutes} min")


def start_all_schedulers() -> None:
    """Start polling jobs for all active users."""
    if not scheduler.running:
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
        print("[Scheduler] ✅ Scheduler started")

    session = get_session()
    users   = session.query(User).filter_by(is_active=True).all()
    session.close()

    for user in users:
        schedule_user(user.id)

    print(f"[Scheduler] ✅ {len(users)} user job(s) active")


def stop_user_scheduler(user_id: str) -> None:
    """Remove a user's polling job."""
    job_id = f"poll_user_{user_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        print(f"[Scheduler] ⏹ Stopped scheduler for {user_id[:8]}")
```

---

### 14.3 `scheduler/task_runner.py`

```python
"""
task_runner.py
--------------
Executes the full pipeline for a user + video combination.
Loads user preferences, runs RPA + RAG + agents + publishers.
Logs everything to DB and CSV.
"""

import uuid
from datetime import datetime
from database.db import get_session
from database.models import User, Preferences, ConnectedPlatform, Episode, RunLog
from rpa_bot import fetch_transcript, organise_files, log_to_csv
from ai_agent import orchestrator
from ai_agent.rag import vector_store, retriever
from preferences.engine import load_preferences
from publisher import wordpress, twitter, mailchimp


def run_for_user(user_id: str, video_url: str) -> dict:
    """
    Full end-to-end pipeline runner for a user + video URL.
    Called by the scheduler when a new video is detected,
    or manually from the CLI / Streamlit UI.
    """
    session = get_session()
    user    = session.query(User).filter_by(id=user_id).first()
    prefs   = load_preferences(user_id)
    session.close()

    if not user:
        print(f"[TaskRunner] ❌ User {user_id[:8]} not found")
        return {}

    print(f"\n[TaskRunner] 🚀 Running pipeline for {user.username}")
    results = {}

    # ── Phase 1: RPA Bot ─────────────────────────────────────────
    try:
        fetch_res  = fetch_transcript.run(video_url, user_id)
        metadata   = fetch_res["metadata"]
        transcript = fetch_res["transcript"]
        t_path     = fetch_res["transcript_path"]
        t_path     = organise_files.run(t_path, metadata, user_id)
        log_to_csv.run(user_id, metadata, t_path, transcript)
        results.update(fetch_res)
        results["transcript_path"] = t_path
    except Exception as e:
        print(f"[TaskRunner] ❌ RPA failed: {e}")
        return {}

    # ── Phase 2: RAG ─────────────────────────────────────────────
    rag_context = ""
    try:
        vector_store.store_episode(transcript, metadata, user_id)
        placeholder = [{"topic": metadata["title"], "description": ""}]
        rag_context = retriever.run(placeholder, user_id, metadata.get("video_id",""))
    except Exception as e:
        print(f"[TaskRunner] ⚠️ RAG skipped: {e}")

    # ── Phase 3: Multi-Agent ─────────────────────────────────────
    try:
        agent_results = orchestrator.run(
            transcript=transcript, metadata=metadata,
            user_id=user_id, preferences=prefs,
            rag_context=rag_context,
        )
        results.update(agent_results)
    except Exception as e:
        print(f"[TaskRunner] ❌ Agent pipeline failed: {e}")
        return {}

    # ── Phase 4: Publish ─────────────────────────────────────────
    publish_status = {}
    platforms      = _get_active_platforms(user_id)

    for platform_record in platforms:
        platform = platform_record.platform
        try:
            if platform == "wordpress" and results.get("blog"):
                r = wordpress.publish_post(results["blog"], metadata, platform_record)
                publish_status["wordpress"] = r.get("success", False)

            elif platform == "twitter" and results.get("social_posts"):
                r = twitter.post_thread(results["social_posts"].get("twitter",""), platform_record)
                publish_status["twitter"] = r.get("success", False)

            elif platform == "mailchimp" and results.get("newsletter"):
                r = mailchimp.send_campaign(results["newsletter"], metadata, platform_record)
                publish_status["mailchimp"] = r.get("success", False)

        except Exception as e:
            print(f"[TaskRunner] ⚠️ Publish to {platform} failed: {e}")
            publish_status[platform] = False

    # ── Phase 5: Save to DB ──────────────────────────────────────
    _save_episode(user_id, metadata, results, publish_status)
    log_to_csv.run(
        user_id=user_id, metadata=metadata,
        transcript_path=t_path, transcript=transcript,
        blog_generated=bool(results.get("blog")),
        social_generated=bool(results.get("social_posts")),
        newsletter_generated=bool(results.get("newsletter")),
        rag_context_used=bool(rag_context),
        status="SUCCESS",
    )

    results["publish_status"] = publish_status
    print(f"[TaskRunner] ✅ Complete for {user.username} | Published: {publish_status}")
    return results


def _get_active_platforms(user_id: str) -> list:
    session   = get_session()
    platforms = session.query(ConnectedPlatform).filter_by(user_id=user_id, is_active=True).all()
    session.close()
    return platforms


def _save_episode(user_id: str, metadata: dict, results: dict, publish_status: dict) -> None:
    session = get_session()
    try:
        episode = Episode(
            id=str(uuid.uuid4()),
            user_id=user_id,
            video_id=metadata.get("video_id",""),
            title=metadata.get("title",""),
            channel=metadata.get("channel",""),
            upload_date=metadata.get("upload_date",""),
            transcript_path=results.get("transcript_path",""),
            blog_path=results.get("blog_path",""),
            social_path=results.get("social_path",""),
            newsletter_path=results.get("newsletter_path",""),
            word_count=len(results.get("transcript","").split()),
            publish_status=publish_status,
            processed_at=datetime.utcnow(),
        )
        session.add(episode)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[TaskRunner] ⚠️ Episode save failed: {e}")
    finally:
        session.close()
```

---

## 15. Full Code — Publishers

### 15.1 `publisher/wordpress.py`

```python
"""
publisher/wordpress.py
----------------------
Publishes blog posts to a WordPress site via the REST API.
Requires: site URL + Application Password (WordPress admin).
"""

import requests
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("ENCRYPTION_KEY", "").encode()


def decrypt(token: str) -> str:
    """Decrypt a stored encrypted token."""
    if not token or not FERNET_KEY:
        return token
    try:
        return Fernet(FERNET_KEY).decrypt(token.encode()).decode()
    except Exception:
        return token


def publish_post(blog: str, metadata: dict, platform_record) -> dict:
    """
    Publish a blog post to WordPress via REST API.

    WordPress REST API endpoint: POST /wp-json/wp/v2/posts
    Auth: Basic auth with username:application_password (base64)

    Args:
        blog:            Markdown blog content
        metadata:        Video metadata dict (for title, date)
        platform_record: ConnectedPlatform ORM object

    Returns:
        dict: {success, post_url, post_id, message}
    """
    site_url = platform_record.platform_url.rstrip("/")
    username = decrypt(platform_record.access_token)
    app_pass = decrypt(platform_record.refresh_token)

    endpoint = f"{site_url}/wp-json/wp/v2/posts"

    payload = {
        "title":   metadata.get("title", "New Episode"),
        "content": blog,
        "status":  "publish",
        "slug":    metadata.get("video_id", "episode"),
    }

    try:
        response = requests.post(
            endpoint,
            json=payload,
            auth=(username, app_pass),
            timeout=30,
        )

        if response.status_code in (200, 201):
            data = response.json()
            print(f"[WordPress] ✅ Published: {data.get('link','')}")
            return {
                "success":  True,
                "post_url": data.get("link", ""),
                "post_id":  data.get("id", ""),
                "message":  "Published successfully",
            }
        else:
            print(f"[WordPress] ❌ Failed: {response.status_code} — {response.text[:100]}")
            return {"success": False, "post_url": "", "post_id": "", "message": response.text[:200]}

    except requests.RequestException as e:
        print(f"[WordPress] ❌ Request error: {e}")
        return {"success": False, "post_url": "", "post_id": "", "message": str(e)}
```

---

### 15.2 `publisher/twitter.py`

```python
"""
publisher/twitter.py
--------------------
Posts a Twitter/X thread via Twitter API v2.
Requires: Bearer Token + OAuth 2.0 credentials.
Uses tweepy for clean API v2 access.
"""

import tweepy
from cryptography.fernet import Fernet
import os, time

FERNET_KEY = os.getenv("ENCRYPTION_KEY", "").encode()


def decrypt(token: str) -> str:
    if not token or not FERNET_KEY:
        return token
    try:
        return Fernet(FERNET_KEY).decrypt(token.encode()).decode()
    except Exception:
        return token


def parse_thread(thread_text: str) -> list:
    """
    Split a thread string into individual tweets.
    Tweets are separated by double newlines.
    Truncates each tweet to 280 characters.
    """
    tweets = [t.strip() for t in thread_text.split("\n\n") if t.strip()]
    return [t[:280] for t in tweets]


def post_thread(thread_text: str, platform_record) -> dict:
    """
    Post a Twitter thread via API v2.

    Posts each tweet as a reply to the previous one
    to form a proper thread.

    Returns:
        dict: {success, tweet_ids, first_tweet_url}
    """
    bearer_token   = decrypt(platform_record.access_token)
    consumer_key   = os.getenv("TWITTER_CONSUMER_KEY", "")
    consumer_secret= os.getenv("TWITTER_CONSUMER_SECRET", "")
    access_token   = os.getenv("TWITTER_ACCESS_TOKEN", "")
    access_secret  = os.getenv("TWITTER_ACCESS_SECRET", "")

    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )

        tweets    = parse_thread(thread_text)
        tweet_ids = []
        reply_to  = None

        for i, tweet in enumerate(tweets):
            if reply_to:
                response = client.create_tweet(text=tweet, in_reply_to_tweet_id=reply_to)
            else:
                response = client.create_tweet(text=tweet)

            tweet_id = response.data["id"]
            tweet_ids.append(tweet_id)
            reply_to = tweet_id
            time.sleep(1)  # rate limit buffer

        first_url = f"https://twitter.com/i/web/status/{tweet_ids[0]}" if tweet_ids else ""
        print(f"[Twitter] ✅ Posted {len(tweet_ids)}-tweet thread")
        return {"success": True, "tweet_ids": tweet_ids, "first_tweet_url": first_url}

    except Exception as e:
        print(f"[Twitter] ❌ Error: {e}")
        return {"success": False, "tweet_ids": [], "first_tweet_url": "", "message": str(e)}
```

---

### 15.3 `publisher/mailchimp.py`

```python
"""
publisher/mailchimp.py
----------------------
Sends newsletter via Mailchimp Marketing API v3.
Creates a campaign, sets content, and sends immediately or schedules.
"""

import requests
import json
from cryptography.fernet import Fernet
import os

FERNET_KEY = os.getenv("ENCRYPTION_KEY", "").encode()


def decrypt(token: str) -> str:
    if not token or not FERNET_KEY:
        return token
    try:
        return Fernet(FERNET_KEY).decrypt(token.encode()).decode()
    except Exception:
        return token


def send_campaign(newsletter: str, metadata: dict, platform_record) -> dict:
    """
    Create and send a Mailchimp campaign.

    Steps:
      1. Create campaign object
      2. Set HTML content
      3. Send immediately

    Requires platform_record.access_token = Mailchimp API key
    Requires platform_record.platform_url = Mailchimp list/audience ID

    Returns:
        dict: {success, campaign_id, message}
    """
    api_key   = decrypt(platform_record.access_token)
    list_id   = platform_record.platform_url

    if not api_key or not list_id:
        return {"success": False, "campaign_id": "", "message": "Missing API key or list ID"}

    # Mailchimp data centre is in the API key suffix (e.g. us1, us6)
    dc       = api_key.split("-")[-1]
    base_url = f"https://{dc}.api.mailchimp.com/3.0"
    headers  = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # 1. Create campaign
    campaign_data = {
        "type": "regular",
        "recipients": {"list_id": list_id},
        "settings": {
            "subject_line": f"🎙️ New Episode: {metadata.get('title', 'New Podcast')}",
            "from_name":    "PodcastAI",
            "reply_to":     "noreply@podcastai.com",
        },
    }

    try:
        r = requests.post(f"{base_url}/campaigns", headers=headers, json=campaign_data, timeout=15)
        if r.status_code != 200:
            return {"success": False, "campaign_id": "", "message": r.text[:200]}

        campaign_id = r.json()["id"]

        # 2. Set content
        html_body = f"<html><body><p>{newsletter.replace(chr(10), '<br>')}</p></body></html>"
        requests.put(
            f"{base_url}/campaigns/{campaign_id}/content",
            headers=headers,
            json={"html": html_body},
            timeout=15,
        )

        # 3. Send
        send_r = requests.post(f"{base_url}/campaigns/{campaign_id}/actions/send",
                               headers=headers, timeout=15)

        if send_r.status_code == 204:
            print(f"[Mailchimp] ✅ Campaign sent: {campaign_id}")
            return {"success": True, "campaign_id": campaign_id, "message": "Campaign sent"}
        else:
            return {"success": False, "campaign_id": campaign_id, "message": send_r.text[:200]}

    except requests.RequestException as e:
        return {"success": False, "campaign_id": "", "message": str(e)}
```

---

## 16. Full Code — Preferences Engine

### 16.1 `preferences/engine.py`

```python
"""
preferences/engine.py
---------------------
Loads per-user preferences from the database and formats them
for injection into every AI agent system prompt.
Defaults are applied if no preferences have been set.
"""

from database.db import get_session
from database.models import Preferences


DEFAULTS = {
    "blog_tone":       "professional",
    "blog_length":     "medium",
    "target_audience": "general",
    "niche_tags":      [],
    "style_sample":    "",
}


def load_preferences(user_id: str) -> dict:
    """
    Load user preferences from database.
    Falls back to defaults if not configured.
    Returns a flat dict ready for agent injection.
    """
    session = get_session()
    try:
        prefs = session.query(Preferences).filter_by(user_id=user_id).first()
        if not prefs:
            return DEFAULTS.copy()

        return {
            "blog_tone":       prefs.blog_tone       or DEFAULTS["blog_tone"],
            "blog_length":     prefs.blog_length      or DEFAULTS["blog_length"],
            "target_audience": prefs.target_audience  or DEFAULTS["target_audience"],
            "niche_tags":      prefs.niche_tags        or [],
            "style_sample":    prefs.style_sample      or "",
        }
    finally:
        session.close()


def save_preferences(user_id: str, data: dict) -> bool:
    """Save or update user preferences. Returns True on success."""
    import uuid
    from datetime import datetime

    session = get_session()
    try:
        prefs = session.query(Preferences).filter_by(user_id=user_id).first()
        if prefs:
            prefs.blog_tone       = data.get("blog_tone", DEFAULTS["blog_tone"])
            prefs.blog_length     = data.get("blog_length", DEFAULTS["blog_length"])
            prefs.target_audience = data.get("target_audience", DEFAULTS["target_audience"])
            prefs.niche_tags      = data.get("niche_tags", [])
            prefs.style_sample    = data.get("style_sample", "")
            prefs.updated_at      = datetime.utcnow()
        else:
            prefs = Preferences(
                id=str(uuid.uuid4()), user_id=user_id,
                blog_tone=data.get("blog_tone", DEFAULTS["blog_tone"]),
                blog_length=data.get("blog_length", DEFAULTS["blog_length"]),
                target_audience=data.get("target_audience", DEFAULTS["target_audience"]),
                niche_tags=data.get("niche_tags", []),
                style_sample=data.get("style_sample", ""),
                updated_at=datetime.utcnow(),
            )
            session.add(prefs)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"[Preferences] ❌ Save error: {e}")
        return False
    finally:
        session.close()
```

---

## 17. Full Code — Analytics

### 17.1 `analytics/dashboard.py`

```python
"""
analytics/dashboard.py
----------------------
Per-user analytics computed from run log CSV.
All functions are user-scoped for multi-tenant isolation.
"""

import pandas as pd
import plotly.express as px
from rpa_bot.log_to_csv import read_log
from collections import Counter
import re


def load_dataframe(user_id: str) -> pd.DataFrame:
    records = read_log(user_id)
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    df["timestamp"]  = pd.to_datetime(df["timestamp"], errors="coerce")
    df["word_count"] = pd.to_numeric(df["word_count"], errors="coerce").fillna(0).astype(int)
    for col in ["blog_generated","social_generated","newsletter_generated","rag_context_used"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().isin(["true","1","yes"])
    return df


def compute_metrics(user_id: str) -> dict:
    df = load_dataframe(user_id)
    if df.empty:
        return {"total_runs":0,"success_rate":0,"avg_words":0,"total_blogs":0,"rag_rate":0}
    success = (df["status"].str.upper() == "SUCCESS").sum()
    return {
        "total_runs":   len(df),
        "success_rate": round(success / len(df) * 100, 1),
        "avg_words":    int(df["word_count"].mean()),
        "total_blogs":  int(df.get("blog_generated", pd.Series([False]*len(df))).sum()),
        "rag_rate":     round(df.get("rag_context_used", pd.Series([False]*len(df))).sum() / len(df) * 100, 1),
    }


def chart_runs_over_time(user_id: str):
    df = load_dataframe(user_id)
    if df.empty: return None
    daily = df.set_index("timestamp").resample("D").size().reset_index()
    daily.columns = ["date","runs"]
    fig = px.line(daily, x="date", y="runs", title="📈 Runs Over Time", line_shape="spline")
    fig.update_traces(line_color="#6366f1", line_width=3)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def chart_word_counts(user_id: str):
    df = load_dataframe(user_id)
    if df.empty: return None
    recent = df.tail(10).copy()
    recent["label"] = recent["video_title"].str[:25]
    fig = px.bar(recent, x="label", y="word_count", title="📝 Transcript Word Counts",
                 color="word_count", color_continuous_scale="Viridis")
    fig.update_layout(xaxis_tickangle=-45, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def chart_success_pie(user_id: str):
    df = load_dataframe(user_id)
    if df.empty: return None
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status","count"]
    return px.pie(counts, names="status", values="count", title="✅ Success Rate",
                  color_discrete_map={"SUCCESS":"#22c55e","FAILED":"#ef4444"}, hole=0.4)


def get_top_words(user_id: str) -> dict:
    df = load_dataframe(user_id)
    if df.empty: return {}
    STOP = {"the","a","an","and","or","but","in","on","at","to","for","of","with","by","is","are","was"}
    words = []
    for title in df["video_title"].dropna():
        words.extend([w for w in re.findall(r'\b[a-zA-Z]{3,}\b', title.lower()) if w not in STOP])
    return dict(Counter(words).most_common(40))
```

---

## 18. Full Code — Streamlit Pages

### 18.1 `pages/login.py`

```python
"""pages/login.py — Streamlit login page."""

import streamlit as st
from auth.login import login_user
from scheduler.job_scheduler import schedule_user, scheduler


def show():
    st.title("🔐 Login to PodcastAI")
    st.caption("Your autonomous content repurposing platform")
    st.divider()

    with st.form("login_form"):
        email    = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

    if submitted:
        if not email or not password:
            st.warning("Please fill in all fields.")
            return
        with st.spinner("Authenticating..."):
            result = login_user(email, password)

        if result["success"]:
            st.session_state["token"]          = result["token"]
            st.session_state["user_id"]        = result["user_id"]
            st.session_state["username"]       = result["username"]
            st.session_state["authenticated"]  = True

            # Start scheduler for this user
            if not scheduler.running:
                scheduler.start()
            schedule_user(result["user_id"])

            st.success(f"Welcome back, {result['username']}! 🎙️")
            st.rerun()
        else:
            st.error(f"❌ {result['message']}")

    st.divider()
    st.caption("Don't have an account?")
    if st.button("Create Account →"):
        st.session_state["page"] = "register"
        st.rerun()
```

---

### 18.2 `pages/register.py`

```python
"""pages/register.py — Streamlit registration page."""

import streamlit as st
from auth.register import register_user
from preferences.engine import save_preferences


def show():
    st.title("🎙️ Join PodcastAI")
    st.caption("Set up your autonomous content pipeline in 2 minutes")
    st.divider()

    with st.form("register_form"):
        username   = st.text_input("Username (3–30 chars, alphanumeric)")
        email      = st.text_input("Email")
        password   = st.text_input("Password (min 8 chars)", type="password")
        channel_id = st.text_input(
            "YouTube Channel ID",
            placeholder="UCxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Find this in YouTube Studio → Settings → Channel → Advanced"
        )
        submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")

    if submitted:
        if not all([username, email, password, channel_id]):
            st.warning("Please fill in all fields.")
            return
        with st.spinner("Creating your account..."):
            result = register_user(username, email, password, channel_id)

        if result["success"]:
            # Create default preferences
            save_preferences(result["user_id"], {})
            st.success("✅ Account created! Please log in.")
            st.session_state["page"] = "login"
            st.rerun()
        else:
            st.error(f"❌ {result['message']}")

    st.divider()
    if st.button("← Back to Login"):
        st.session_state["page"] = "login"
        st.rerun()
```

---

### 18.3 `pages/dashboard.py`

```python
"""pages/dashboard.py — Main creator dashboard."""

import streamlit as st
from database.db import get_session
from database.models import Episode, RunLog
from analytics.dashboard import compute_metrics
from scheduler.job_scheduler import scheduler, schedule_user, stop_user_scheduler
from scheduler.channel_watcher import check_for_new_videos
from database.models import User


def show(user_id: str, username: str):
    st.title(f"🏠 Dashboard — Welcome, {username}! 👋")
    st.divider()

    # ── KPI Row ───────────────────────────────────────────────────
    metrics = compute_metrics(user_id)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🎬 Episodes",    metrics["total_runs"])
    c2.metric("✅ Success Rate", f"{metrics['success_rate']}%")
    c3.metric("📝 Avg Words",   f"{metrics['avg_words']:,}")
    c4.metric("📄 Blogs Made",  metrics["total_blogs"])
    c5.metric("🧠 RAG Used",    f"{metrics['rag_rate']}%")

    st.divider()

    col1, col2 = st.columns([2, 1])

    # ── Recent Episodes ───────────────────────────────────────────
    with col1:
        st.subheader("📹 Recent Episodes")
        session  = get_session()
        episodes = session.query(Episode).filter_by(user_id=user_id)\
                          .order_by(Episode.processed_at.desc()).limit(5).all()
        session.close()

        if episodes:
            for ep in episodes:
                pub = ep.publish_status or {}
                badges = " ".join([
                    "🌐" if pub.get("wordpress") else "",
                    "🐦" if pub.get("twitter")   else "",
                    "📧" if pub.get("mailchimp")  else "",
                ])
                with st.expander(f"**{ep.title[:55]}** {badges}", expanded=False):
                    st.caption(f"📅 {ep.upload_date} | 📝 {ep.word_count:,} words")
                    st.caption(f"🔗 Published: {pub}")
        else:
            st.info("No episodes processed yet. The scheduler will pick them up automatically!")

    # ── Automation Status ─────────────────────────────────────────
    with col2:
        st.subheader("⚡ Automation Status")

        job_id  = f"poll_user_{user_id}"
        running = scheduler.get_job(job_id) is not None

        if running:
            st.success("🟢 Watching your channel")
        else:
            st.warning("🔴 Scheduler not running")

        if st.button("▶ Start Watching" if not running else "⏹ Stop Watching"):
            if not running:
                if not scheduler.running: scheduler.start()
                schedule_user(user_id)
                st.success("✅ Started!")
            else:
                stop_user_scheduler(user_id)
                st.info("⏹ Stopped")
            st.rerun()

        st.divider()
        st.subheader("🔍 Manual Check")
        if st.button("Check for New Videos Now"):
            session = get_session()
            user    = session.query(User).filter_by(id=user_id).first()
            session.close()
            with st.spinner("Checking..."):
                new = check_for_new_videos(user)
            if new:
                st.success(f"Found {len(new)} new video(s)!")
                for v in new:
                    st.write(f"▶ {v['title'][:50]}")
            else:
                st.info("No new videos found.")
```

---

### 18.4 `pages/preferences.py`

```python
"""pages/preferences.py — Content preferences settings page."""

import streamlit as st
from preferences.engine import load_preferences, save_preferences

NICHE_OPTIONS = [
    "Technology & AI", "Business & Entrepreneurship", "Health & Wellness",
    "Science", "Finance & Investing", "Lifestyle", "Politics", "Sports",
    "Education", "Entertainment", "True Crime", "History",
]


def show(user_id: str):
    st.title("✍️ Content Preferences")
    st.caption("These preferences are injected into every AI agent to personalise your content.")
    st.divider()

    current = load_preferences(user_id)

    with st.form("preferences_form"):
        st.subheader("🖊️ Writing Style")
        col1, col2, col3 = st.columns(3)

        with col1:
            tone = st.selectbox(
                "Blog Tone",
                ["professional", "casual", "formal", "fun", "academic"],
                index=["professional","casual","formal","fun","academic"].index(
                    current.get("blog_tone","professional")
                ),
            )
        with col2:
            length = st.selectbox(
                "Blog Length",
                ["short (500w)", "medium (1000w)", "long (2000w)"],
                index=["short (500w)","medium (1000w)","long (2000w)"].index(
                    f"{current.get('blog_length','medium')} (1000w)"
                ) if current.get("blog_length","medium") == "medium" else 1,
            )
        with col3:
            audience = st.selectbox(
                "Target Audience",
                ["general", "technical experts", "beginners", "business professionals"],
                index=["general","technical experts","beginners","business professionals"].index(
                    current.get("target_audience","general")
                ) if current.get("target_audience","general") in ["general","technical experts","beginners","business professionals"] else 0,
            )

        st.divider()
        st.subheader("🏷️ Content Niche")
        st.caption("Select all niches that apply to your podcast")
        niche_tags = st.multiselect(
            "Your Niches",
            NICHE_OPTIONS,
            default=[n for n in current.get("niche_tags",[]) if n in NICHE_OPTIONS],
        )

        st.divider()
        st.subheader("📝 Style Sample (Optional)")
        st.caption("Paste a blog post you love — the AI will match its style")
        style_sample = st.text_area(
            "Style Sample",
            value=current.get("style_sample",""),
            height=150,
            placeholder="Paste a blog post example here to guide the AI's writing style...",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button("💾 Save Preferences", use_container_width=True, type="primary")

    if submitted:
        length_map = {"short (500w)": "short", "medium (1000w)": "medium", "long (2000w)": "long"}
        success = save_preferences(user_id, {
            "blog_tone":       tone,
            "blog_length":     length_map.get(length, "medium"),
            "target_audience": audience,
            "niche_tags":      niche_tags,
            "style_sample":    style_sample,
        })
        if success:
            st.success("✅ Preferences saved! All future content will reflect these settings.")
        else:
            st.error("❌ Save failed. Please try again.")
```

---

### 18.5 `pages/templates.py`

```python
"""pages/templates.py — Repeatable task template builder."""

import streamlit as st
import uuid
from datetime import datetime
from database.db import get_session
from database.models import Template


def show(user_id: str):
    st.title("🔁 Task Templates")
    st.caption("Define repeatable automation sequences triggered by new uploads or a fixed schedule.")
    st.divider()

    session   = get_session()
    templates = session.query(Template).filter_by(user_id=user_id).all()
    session.close()

    # ── Existing Templates ────────────────────────────────────────
    if templates:
        st.subheader("Your Templates")
        for tmpl in templates:
            tasks = tmpl.tasks or {}
            with st.expander(f"**{tmpl.name}** — {tmpl.trigger_type}", expanded=False):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.caption(f"Trigger: `{tmpl.trigger_type}`")
                    if tmpl.schedule_cron:
                        st.caption(f"Cron: `{tmpl.schedule_cron}`")
                    st.write("Tasks:")
                    for task, enabled in tasks.items():
                        icon = "✅" if enabled else "❌"
                        st.caption(f"{icon} {task}")
                with col2:
                    active_label = "🟢 Active" if tmpl.is_active else "🔴 Paused"
                    st.caption(active_label)
                    if st.button("🗑️ Delete", key=f"del_{tmpl.id}"):
                        s = get_session()
                        s.query(Template).filter_by(id=tmpl.id).delete()
                        s.commit()
                        s.close()
                        st.rerun()
        st.divider()

    # ── New Template Builder ──────────────────────────────────────
    st.subheader("➕ Create New Template")

    with st.form("template_form"):
        name = st.text_input("Template Name", placeholder="e.g. New Episode Drop")

        trigger = st.selectbox("Trigger", ["new_upload", "scheduled"])
        cron    = ""
        if trigger == "scheduled":
            cron = st.text_input("Cron Expression", placeholder="0 8 * * 2  (Tuesdays at 8am)")
            st.caption("Format: minute hour day month weekday — [crontab.guru](https://crontab.guru)")

        st.subheader("Tasks to Run")
        col1, col2 = st.columns(2)
        with col1:
            do_blog       = st.checkbox("📝 Generate Blog Post",        value=True)
            do_twitter    = st.checkbox("🐦 Post to Twitter",           value=True)
            do_newsletter = st.checkbox("📧 Send Newsletter",           value=True)
        with col2:
            do_linkedin   = st.checkbox("💼 Post to LinkedIn",          value=False)
            do_instagram  = st.checkbox("📸 Post to Instagram",         value=False)
            do_wordpress  = st.checkbox("🌐 Publish to WordPress",      value=True)

        submitted = st.form_submit_button("💾 Save Template", use_container_width=True, type="primary")

    if submitted and name:
        session = get_session()
        tmpl    = Template(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            trigger_type=trigger,
            schedule_cron=cron,
            tasks={
                "blog":       do_blog,
                "twitter":    do_twitter,
                "newsletter": do_newsletter,
                "linkedin":   do_linkedin,
                "instagram":  do_instagram,
                "wordpress":  do_wordpress,
            },
            is_active=True,
            created_at=datetime.utcnow(),
        )
        session.add(tmpl)
        session.commit()
        session.close()
        st.success(f"✅ Template '{name}' saved!")
        st.rerun()
```

---

### 18.6 `pages/publishers.py`

```python
"""pages/publishers.py — Connect publishing platform credentials."""

import streamlit as st
import uuid
from cryptography.fernet import Fernet
import os
from database.db import get_session
from database.models import ConnectedPlatform

FERNET_KEY = os.getenv("ENCRYPTION_KEY","").encode()


def encrypt(value: str) -> str:
    if not value or not FERNET_KEY: return value
    try:
        return Fernet(FERNET_KEY).encrypt(value.encode()).decode()
    except Exception:
        return value


def show(user_id: str):
    st.title("📤 Connect Publishing Platforms")
    st.caption("Connect your platforms once. The pipeline publishes automatically from then on.")
    st.divider()

    session   = get_session()
    platforms = {p.platform: p for p in session.query(ConnectedPlatform).filter_by(user_id=user_id).all()}
    session.close()

    # ── WordPress ────────────────────────────────────────────────
    with st.expander("🌐 WordPress", expanded="wordpress" not in platforms):
        if "wordpress" in platforms:
            st.success(f"✅ Connected — {platforms['wordpress'].platform_url}")
            if st.button("Disconnect WordPress"):
                s = get_session()
                s.query(ConnectedPlatform).filter_by(user_id=user_id, platform="wordpress").delete()
                s.commit(); s.close(); st.rerun()
        else:
            with st.form("wp_form"):
                site_url = st.text_input("WordPress Site URL", placeholder="https://yoursite.com")
                username = st.text_input("WordPress Username")
                app_pass = st.text_input("Application Password", type="password",
                                         help="WordPress Admin → Users → Application Passwords")
                if st.form_submit_button("Connect WordPress", type="primary"):
                    if site_url and username and app_pass:
                        s = get_session()
                        s.add(ConnectedPlatform(
                            id=str(uuid.uuid4()), user_id=user_id,
                            platform="wordpress", platform_url=site_url,
                            access_token=encrypt(username),
                            refresh_token=encrypt(app_pass), is_active=True,
                        ))
                        s.commit(); s.close()
                        st.success("✅ WordPress connected!"); st.rerun()

    # ── Twitter/X ────────────────────────────────────────────────
    with st.expander("🐦 Twitter / X", expanded="twitter" not in platforms):
        if "twitter" in platforms:
            st.success("✅ Twitter connected")
            if st.button("Disconnect Twitter"):
                s = get_session()
                s.query(ConnectedPlatform).filter_by(user_id=user_id, platform="twitter").delete()
                s.commit(); s.close(); st.rerun()
        else:
            with st.form("tw_form"):
                bearer = st.text_input("Bearer Token", type="password")
                st.caption("Get from [developer.twitter.com](https://developer.twitter.com)")
                if st.form_submit_button("Connect Twitter", type="primary"):
                    if bearer:
                        s = get_session()
                        s.add(ConnectedPlatform(
                            id=str(uuid.uuid4()), user_id=user_id,
                            platform="twitter", access_token=encrypt(bearer), is_active=True,
                        ))
                        s.commit(); s.close()
                        st.success("✅ Twitter connected!"); st.rerun()

    # ── Mailchimp ────────────────────────────────────────────────
    with st.expander("📧 Mailchimp", expanded="mailchimp" not in platforms):
        if "mailchimp" in platforms:
            st.success("✅ Mailchimp connected")
            if st.button("Disconnect Mailchimp"):
                s = get_session()
                s.query(ConnectedPlatform).filter_by(user_id=user_id, platform="mailchimp").delete()
                s.commit(); s.close(); st.rerun()
        else:
            with st.form("mc_form"):
                api_key = st.text_input("Mailchimp API Key", type="password")
                list_id = st.text_input("Audience/List ID",
                                        help="Mailchimp → Audience → Settings → Audience ID")
                if st.form_submit_button("Connect Mailchimp", type="primary"):
                    if api_key and list_id:
                        s = get_session()
                        s.add(ConnectedPlatform(
                            id=str(uuid.uuid4()), user_id=user_id,
                            platform="mailchimp", access_token=encrypt(api_key),
                            platform_url=list_id, is_active=True,
                        ))
                        s.commit(); s.close()
                        st.success("✅ Mailchimp connected!"); st.rerun()
```

---

### 18.7 `pages/episodes.py`

```python
"""pages/episodes.py — Episode history and manual processing."""

import streamlit as st
from database.db import get_session
from database.models import Episode
from scheduler.task_runner import run_for_user


def show(user_id: str):
    st.title("📹 Episodes")
    st.divider()

    # ── Manual Process ────────────────────────────────────────────
    st.subheader("⚡ Process a Video Manually")
    col1, col2 = st.columns([4,1])
    with col1:
        manual_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...",
                                   label_visibility="collapsed")
    with col2:
        run_btn = st.button("🚀 Run", use_container_width=True, type="primary")

    if run_btn and manual_url:
        with st.spinner("Running full pipeline..."):
            results = run_for_user(user_id=user_id, video_url=manual_url)
        if results:
            st.success("✅ Pipeline complete!")
            st.json({"publish_status": results.get("publish_status", {})})
        else:
            st.error("Pipeline failed. Check that Ollama is running.")

    st.divider()

    # ── Episode History ───────────────────────────────────────────
    st.subheader("📋 Processed Episodes")
    session  = get_session()
    episodes = session.query(Episode).filter_by(user_id=user_id)\
                      .order_by(Episode.processed_at.desc()).all()
    session.close()

    if not episodes:
        st.info("No episodes yet. The scheduler will process new uploads automatically, or run one manually above.")
        return

    for ep in episodes:
        pub = ep.publish_status or {}
        status_icons = "".join([
            "🌐" if pub.get("wordpress") else "",
            "🐦" if pub.get("twitter")   else "",
            "📧" if pub.get("mailchimp")  else "",
        ])
        with st.expander(f"**{ep.title[:60]}** {status_icons or '⏳'}"):
            col1, col2, col3 = st.columns(3)
            col1.metric("📅 Date",    ep.upload_date)
            col2.metric("📝 Words",   f"{ep.word_count:,}")
            col3.metric("🔗 Channel", ep.channel[:20] if ep.channel else "—")

            if ep.blog_path and st.button(f"View Blog", key=f"blog_{ep.id}"):
                try:
                    with open(ep.blog_path, "r", encoding="utf-8") as f:
                        st.markdown(f.read())
                except FileNotFoundError:
                    st.warning("Blog file not found on disk")
```

---

### 18.8 `pages/analytics.py`

```python
"""pages/analytics.py — Per-user analytics dashboard page."""

import streamlit as st
from analytics.dashboard import (
    compute_metrics, chart_runs_over_time,
    chart_word_counts, chart_success_pie, get_top_words
)
from rpa_bot.log_to_csv import read_log
import pandas as pd


def show(user_id: str):
    st.title("📊 Analytics Dashboard")
    st.caption("All metrics are scoped to your account")
    st.divider()

    metrics = compute_metrics(user_id)
    if metrics["total_runs"] == 0:
        st.info("📭 No runs yet. Process your first episode to see analytics here.")
        return

    # KPIs
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("🎬 Total Runs",    metrics["total_runs"])
    c2.metric("✅ Success Rate",  f"{metrics['success_rate']}%")
    c3.metric("📝 Avg Words",     f"{metrics['avg_words']:,}")
    c4.metric("📄 Blogs",         metrics["total_blogs"])
    c5.metric("🧠 RAG Rate",      f"{metrics['rag_rate']}%")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        fig = chart_runs_over_time(user_id)
        if fig: st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = chart_success_pie(user_id)
        if fig: st.plotly_chart(fig, use_container_width=True)

    fig = chart_word_counts(user_id)
    if fig: st.plotly_chart(fig, use_container_width=True)

    # Word cloud
    words = get_top_words(user_id)
    if words:
        st.subheader("☁️ Your Most Covered Topics")
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt
            wc  = WordCloud(width=1200, height=300, background_color="white",
                            colormap="viridis", max_words=40).generate_from_frequencies(words)
            fig2, ax = plt.subplots(figsize=(12,3))
            ax.imshow(wc, interpolation="bilinear"); ax.axis("off")
            st.pyplot(fig2)
        except ImportError:
            st.write(", ".join(f"**{w}**" for w in list(words.keys())[:20]))

    # Full log table
    st.divider()
    st.subheader("📋 Full Run History")
    records = read_log(user_id)
    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Export CSV", df.to_csv(index=False),
                           file_name=f"{user_id[:8]}_run_log.csv", mime="text/csv")
```

---

## 19. Full Code — Entry Points

### 19.1 `app.py`

```python
"""
app.py
------
Streamlit main entry point.
Handles routing between all 8 pages with session-based auth.
Run with: streamlit run app.py
"""

import streamlit as st
from database.db import init_db

# Initialise database on first run
init_db()

# ── PAGE CONFIG ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎙️ PodcastAI Platform",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SESSION INIT ──────────────────────────────────────────────────────
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "token"         not in st.session_state: st.session_state["token"]         = ""
if "user_id"       not in st.session_state: st.session_state["user_id"]       = ""
if "username"      not in st.session_state: st.session_state["username"]      = ""
if "page"          not in st.session_state: st.session_state["page"]          = "login"

# ── AUTH CHECK ────────────────────────────────────────────────────────
from auth.middleware import require_auth

if st.session_state["authenticated"]:
    if not require_auth(st.session_state):
        st.session_state["authenticated"] = False
        st.session_state["page"]          = "login"
        st.rerun()

# ── ROUTING ───────────────────────────────────────────────────────────
page    = st.session_state["page"]
user_id = st.session_state.get("user_id", "")
uname   = st.session_state.get("username", "")

# Public pages
if not st.session_state["authenticated"]:
    if page == "register":
        from pages.register import show; show()
    else:
        from pages.login import show; show()
    st.stop()

# ── AUTHENTICATED SIDEBAR ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microphone.png", width=50)
    st.markdown(f"**{uname}** 👤")
    st.divider()

    pages = {
        "🏠 Dashboard":    "dashboard",
        "📹 Episodes":     "episodes",
        "✍️ Preferences":  "preferences",
        "🔁 Templates":    "templates",
        "📤 Publishers":   "publishers",
        "📊 Analytics":    "analytics",
    }

    for label, key in pages.items():
        if st.button(label, use_container_width=True,
                     type="primary" if page == key else "secondary"):
            st.session_state["page"] = key
            st.rerun()

    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        for k in ["authenticated","token","user_id","username"]:
            st.session_state[k] = "" if k != "authenticated" else False
        st.session_state["page"] = "login"
        st.rerun()

# ── PAGE DISPATCH ─────────────────────────────────────────────────────
if   page == "dashboard":   from pages.dashboard   import show; show(user_id, uname)
elif page == "episodes":    from pages.episodes    import show; show(user_id)
elif page == "preferences": from pages.preferences import show; show(user_id)
elif page == "templates":   from pages.templates   import show; show(user_id)
elif page == "publishers":  from pages.publishers  import show; show(user_id)
elif page == "analytics":   from pages.analytics   import show; show(user_id)
else:
    from pages.dashboard import show; show(user_id, uname)
```

---

### 19.2 `main.py`

```python
"""
main.py
-------
Headless CLI runner for the full platform pipeline.

Usage:
    python main.py --url "URL" --user-id "UUID"
    python main.py --url "URL" --user-id "UUID" --skip-rag
    python main.py --start-scheduler       # Start all user schedulers
"""

import argparse
from database.db import init_db


def main():
    init_db()

    parser = argparse.ArgumentParser(description="PodcastAI Platform CLI")
    parser.add_argument("--url",              help="YouTube video URL to process")
    parser.add_argument("--user-id",          help="User UUID to run pipeline for")
    parser.add_argument("--skip-rag",         action="store_true")
    parser.add_argument("--start-scheduler",  action="store_true",
                        help="Start channel watchers for all active users")
    args = parser.parse_args()

    if args.start_scheduler:
        from scheduler.job_scheduler import start_all_schedulers
        import time
        start_all_schedulers()
        print("[CLI] Scheduler running. Press Ctrl+C to stop.")
        try:
            while True: time.sleep(60)
        except KeyboardInterrupt:
            print("[CLI] Scheduler stopped.")
        return

    if not args.url or not args.user_id:
        parser.error("--url and --user-id are required for pipeline runs")

    from scheduler.task_runner import run_for_user
    results = run_for_user(user_id=args.user_id, video_url=args.url)

    if results:
        print(f"\n✅ Pipeline complete")
        print(f"Blog path:       {results.get('blog_path','N/A')}")
        print(f"Social path:     {results.get('social_path','N/A')}")
        print(f"Newsletter path: {results.get('newsletter_path','N/A')}")
        print(f"Publish status:  {results.get('publish_status',{})}")
    else:
        print("❌ Pipeline failed")


if __name__ == "__main__":
    main()
```

---

### 19.3 `requirements.txt`

```
# ── Auth ──────────────────────────────────────────────
bcrypt>=4.0.1
PyJWT>=2.8.0
pydantic[email]>=2.0.0
cryptography>=41.0.0

# ── Database ──────────────────────────────────────────
sqlalchemy>=2.0.0

# ── RPA Bot ───────────────────────────────────────────
youtube-transcript-api==0.6.2
yt-dlp>=2024.1.1
pandas>=2.0.0

# ── AI Agents ─────────────────────────────────────────
ollama>=0.1.8
duckduckgo-search>=5.0.0

# ── RAG ───────────────────────────────────────────────
chromadb>=0.4.24

# ── Scheduler ─────────────────────────────────────────
APScheduler>=3.10.4
feedparser>=6.0.10

# ── Publishers ────────────────────────────────────────
tweepy>=4.14.0
requests>=2.31.0

# ── Analytics & Visualisation ─────────────────────────
plotly>=5.18.0
wordcloud>=1.9.3
matplotlib>=3.8.0

# ── Frontend ──────────────────────────────────────────
streamlit>=1.32.0
```

---

## 20. Automation Potential Analysis

| Task | Automatable? | Type | Justification |
|------|-------------|------|---------------|
| User registration + auth | ✅ Full | System | Rule-based validation, bcrypt hashing |
| YouTube RSS polling | ✅ Full | RPA | Scheduled, deterministic, no judgement |
| New video detection | ✅ Full | RPA | DB lookup comparison, rule-based |
| Transcript download | ✅ Full | RPA | API call, structured response |
| Metadata extraction | ✅ Full | RPA | Consistent yt-dlp response format |
| File organisation | ✅ Full | RPA | Date-based rule, fully deterministic |
| CSV audit logging | ✅ Full | RPA | Structured data entry |
| RAG embedding + storage | ✅ Full | Hybrid | Algorithmic chunking + vector DB |
| RAG context retrieval | ✅ Full | Hybrid | Cosine similarity, no human needed |
| Preference loading | ✅ Full | System | DB read + injection |
| Topic extraction | ✅ Full | AI Agent | NLP + semantic understanding |
| Web research | ✅ Full | AI Agent | Information retrieval + summarisation |
| Blog writing | ✅ Full | AI Agent | Creative generation + structure |
| Content editing | ✅ Full | AI Agent | Linguistic quality assessment |
| SEO optimisation | ✅ Full | AI Agent | Keyword strategy + structural rules |
| Social media posts | ✅ Full | AI Agent | Platform tone adaptation |
| Newsletter writing | ✅ Full | AI Agent | Summarisation + narrative voice |
| WordPress publishing | ✅ Full | RPA | REST API, rule-based |
| Twitter/X posting | ✅ Full | RPA | API call, rule-based |
| Mailchimp sending | ✅ Full | RPA | API call, rule-based |
| Feedback regeneration | ✅ Partial | AI + Human | Human provides direction, AI executes |
| Platform credential mgmt | ✅ Full | System | Encrypted storage, UI-managed |
| Analytics computation | ✅ Full | System | Deterministic math from log data |
| Final editorial review | ❌ Human | Human | Brand voice, legal, editorial judgement |

---

## 21. Multi-Agent Flow Explained

```
INPUT: transcript + metadata + preferences + RAG context
       │
       ▼
┌────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT                    │
│                                                        │
│  Role: Project Manager                                 │
│  • Plans execution sequence                            │
│  • Injects user preferences into each agent            │
│  • Passes outputs between agents                       │
│  • Handles per-agent errors gracefully                 │
│  • Saves all files to user-scoped output folders       │
└───┬──────────┬────────────┬────────────┬───────────────┘
    ▼          ▼            ▼            ▼
┌──────┐  ┌──────┐    ┌──────┐    ┌──────┐
│RESEAR│  │WRITER│    │EDITOR│    │  SEO │
│CH    │  │AGENT │    │AGENT │    │AGENT │
│      │  │      │    │      │    │      │
│1.LLM │  │1.Blog│    │1.Fix │    │1.KW  │
│  ext │  │2.Soc │    │  grm │    │  inj │
│  top │  │3.News│    │2.Flow│    │2.Meta│
│2.DDG │  │      │    │3.Tone│    │  dsc │
│  srch│  │Uses: │    │4.CTAs│    │3.Slug│
│3.LLM │  │-Res. │    │      │    │4.H1  │
│  sum │  │-RAG  │    │      │    │  H2  │
└──────┘  │-Prefs│    └──────┘    └──────┘
          │-Fdbk │
          └──────┘

PREFERENCE INJECTION (per user, per run):
  tone="formal"         → "Write in a formal, authoritative tone"
  niche=["AI","Tech"]   → "Focus content on AI and technology themes"
  audience="experts"    → "Assume expert-level technical knowledge"
  style_sample="..."    → "Match the style of: {sample}"
```

---

## 22. RAG System Explained

```
INGESTION (every new episode, per user):
  Transcript
      │
      ▼
  chunk_text()     ← 500-word overlapping segments
      │
      ▼
  embed_chunks()   ← Ollama nomic-embed-text (local)
      │
      ▼
  ChromaDB.add()   ← knowledge_base/{user_id}/ (isolated per user)


RETRIEVAL (before Writer Agent):
  Current Topics
      │
      ▼
  embed_text(topic)
      │
      ▼
  ChromaDB.query() ← cosine similarity search
      │
  Filter:
    Exclude current episode
    Exclude dist > 0.4
    Deduplicate across topics
      │
      ▼
  Format: "[From 'Episode Title']: relevant chunk text"
      │
      ▼
  Writer Agent uses it:
  "As explored in a previous episode on X..."

USER ISOLATION:
  User A → knowledge_base/user_a_id/ (their episodes only)
  User B → knowledge_base/user_b_id/ (their episodes only)
  No cross-contamination between accounts
```

---

## 23. Human-in-the-Loop Design

```
AUTO MODE (default — no intervention needed):
  Pipeline runs → content generated → published → done
  Creator logs in to review completed episodes at leisure

REVIEW MODE (optional):
  Creator visits Episodes page
  Opens any episode
  Reads generated blog
  Gives feedback → pipeline regenerates → accepts

FEEDBACK LOOP:
  Blog v1 → "Make it more casual" → Blog v2
          → "Add more stats"      → Blog v3
          → ✅ Accept             → Publish

VERSION TRACKING:
  All versions stored in session state
  Creator can navigate v1 ↔ v2 ↔ v3
  Accepted version is published
  feedback_iterations logged to DB for analytics
```

---

## 24. Security Architecture

```
PASSWORD SECURITY:
  Plain text password → bcrypt hash (12 rounds)
  Hash stored in DB — plain text never persisted
  Verification: bcrypt.checkpw() on login

SESSION SECURITY:
  JWT tokens — HS256 signed with SECRET_KEY
  24-hour expiry — auto-invalidated
  Validated on every protected page load
  No server-side session storage needed

API KEY SECURITY:
  All platform tokens encrypted with Fernet (AES-128-CBC)
  ENCRYPTION_KEY stored in environment variable only
  Encrypted value stored in DB — useless without key
  Decrypted only at publish time, never logged

DATA ISOLATION:
  Every DB query filtered by user_id
  Output files in outputs/{user_id}/
  Knowledge base in knowledge_base/{user_id}/
  Run logs in logs/{user_id}_run_log.csv
  No cross-user data access possible

ENVIRONMENT VARIABLES:
  SECRET_KEY         — JWT signing key (min 32 chars)
  ENCRYPTION_KEY     — Fernet key for API token encryption
  Never hardcoded — always from os.getenv()
```

---

## 25. Challenges & Mitigations

| Challenge | Impact | Mitigation |
|-----------|--------|-----------|
| Video has no transcript | Pipeline blocked | Graceful error, episode marked as failed in DB |
| YouTube RSS delay | New video not detected immediately | 30-min polling + manual check button in UI |
| Ollama not running | All AI steps fail | Clear error message with start command shown |
| LLM returns malformed JSON | Parse error | try/except with raw text fallback |
| Transcript too long | LLM context overflow | chunk_transcript() takes first+last 2000 words |
| Twitter API rate limits | Posts fail | Retry with exponential backoff, 1s sleep between tweets |
| WordPress auth failure | Blog not published | Status logged per platform, retryable from UI |
| Mailchimp list ID wrong | Campaign not sent | Validate list ID on connect, clear error shown |
| Duplicate episode processing | Double content | video_id checked in Episodes table before run |
| Multiple users, one Ollama | Slow concurrent runs | Queue requests; Ollama handles sequentially |
| ChromaDB corruption | RAG unavailable | Pipeline continues without RAG, non-fatal |
| JWT token expired | User locked out | Re-login flow, token refresh on next request |
| Large transcript files | Disk usage | Auto-cleanup of transcripts older than 90 days |
| User deletes account | Orphaned data | Cascade delete across all user-scoped tables |

---

## 26. Academic References

- van der Aalst, W. M. P. (2016). *Process Mining: Data Science in Action* (2nd ed.). Springer. https://doi.org/10.1007/978-3-662-49851-4

- Dumas, M., La Rosa, M., Mendling, J., & Reijers, H. A. (2018). *Fundamentals of Business Process Management* (2nd ed.). Springer. https://doi.org/10.1007/978-3-662-56509-4

- Lacity, M., & Willcocks, L. (2016). A new approach to automating services. *MIT Sloan Management Review*, 58(1), 41–49.

- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *Advances in Neural Information Processing Systems*, 33, 9459–9474.

- Mistral AI. (2024). *Mistral-7B-Instruct-v0.2*. HuggingFace. https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

- Object Management Group. (2013). *Business Process Model and Notation (BPMN) Version 2.0.2*. https://www.omg.org/spec/BPMN/2.0.2/

- Ollama. (2024). *Run large language models locally*. https://ollama.com

- OWASP Foundation. (2023). *OWASP Top Ten Web Application Security Risks*. https://owasp.org/Top10/

- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org

- Trummer, I. (2023). From BERT to GPT: A survey of large language models for NLP. *ACM Computing Surveys*, 56(1), 1–38.

- YouTube Transcript API. (2024). *youtube-transcript-api*. PyPI. https://pypi.org/project/youtube-transcript-api/

- yt-dlp Contributors. (2024). *yt-dlp*. GitHub. https://github.com/yt-dlp/yt-dlp

- APScheduler. (2024). *Advanced Python Scheduler documentation*. https://apscheduler.readthedocs.io

- ChromaDB. (2024). *Chroma: The AI-native open-source embedding database*. https://www.trychroma.com

- Streamlit Inc. (2024). *Streamlit documentation*. https://docs.streamlit.io

- Tweepy. (2024). *Tweepy: Twitter for Python documentation*. https://docs.tweepy.org

- Mailchimp. (2024). *Mailchimp Marketing API v3 documentation*. https://mailchimp.com/developer/marketing/api/

- WordPress. (2024). *WordPress REST API handbook*. https://developer.wordpress.org/rest-api/

---

*Document Version: 3.0 — SaaS Platform Edition*
*Last Updated: April 2026*
*Module: H9IAPA — Intelligent Agents & Process Automation*
*National College of Ireland*
*Covers: Multi-tenant auth, event-driven scheduler, multi-agent AI, RAG, human-in-the-loop, platform publishing*
