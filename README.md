
# LinkedIn MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LinkedIn API](https://img.shields.io/badge/LinkedIn-API%20v202510-blue)](https://learn.microsoft.com/en-us/linkedin/)

Complete LinkedIn automation toolkit. Scrape profiles, manage posts, read any LinkedIn content, and automate interactions via MCP (Model Context Protocol).

---

## 📘 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Quickstart](#quickstart)
- [Authentication](#authentication)
- [Usage](#usage)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Available Tools](#available-tools)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [API Versioning](#api-versioning)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Changelog](#changelog)

---

# Overview

`linkedin-mcp` is a fully featured MCP server that provides automation tools for LinkedIn.  
It supports browser-based scraping and API-based operations for content management, media uploads, and reactions.

Repository: **[Linkedin MCP Server](https://github.com/selvin-paul-raj/Linkedin-MCP-Server)**

---

# Features

### 🔍 Scraping (Browser-Based)
- Extract **full LinkedIn profiles**
- Scrape **company pages**
- Read **job listings**
- Read **ANY LinkedIn post**
- Extract images, videos, engagement metrics

### 📝 API-Based Post Management
- Create, update, delete LinkedIn posts
- Add or remove reactions
- Upload images and documents
- Supports all official LinkedIn REST API features

### 🧩 MCP Integration
- Works with Claude Desktop and any MCP-compatible client
- 17 total tools included

### 🧪 Testing
- 50+ tests
- Covers scraping, API, and MCP tools

---

# Quickstart

### Install

```bash
git clone https://github.com/selvin-paul-raj/Linkedin-MCP-Server.git
cd Linkedin-MCP-Server

# create environment config
cp .env.example .env

# install dependencies
pip install -e .
````

### Run

```bash
# Standard MCP server
uv run linkedin-mcp

# Debug mode (shows browser)
uv run main.py --debug --no-headless --no-lazy-init

# HTTP mode
uv run main.py --transport streamable-http
```

---

# Authentication

## 1. Scraping (LinkedIn Cookie)

Get your `li_at` cookie:

1. Log in to LinkedIn in Chrome
2. Press **F12**
3. Application → Cookies → [https://www.linkedin.com](https://www.linkedin.com)
4. Copy the `li_at` cookie value
5. Add to `.env`:

```
LINKEDIN_COOKIE=li_at=YOUR_COOKIE_VALUE
```

---

## 2. API (OAuth Access Token)

Add these fields to `.env`:



```
LINKEDIN_CLIENT_ID=your_id
LINKEDIN_CLIENT_SECRET=your_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_API_VERSION=202510
```

### Quick OAuth Link

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=w_member_social%20r_liteprofile%20r_emailaddress
```

Exchange auth code:

```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_CODE" \
  -d "redirect_uri=YOUR_REDIRECT_URI" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

---

# Usage

### Read any LinkedIn post

```json
{
  "tool": "read_linkedin_post",
  "input": "https://www.linkedin.com/posts/...activity-123456..."
}
```

### Create a post

```json
{
  "tool": "create_linkedin_post",
  "input": {
    "text": "Excited to announce our new product launch! 🚀",
    "visibility": "PUBLIC"
  }
}
```

### Upload image

```json
{
  "tool": "upload_linkedin_image",
  "input": { "image_url": "https://example.com/image.jpg" }
}
```

---

# Claude Desktop Integration

Add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\MCP\\linkedin-mcp",
        "run",
        "linkedin-mcp"
      ],
      "env": {
        "LINKEDIN_COOKIE": "li_at=YOUR_COOKIE",
        "LINKEDIN_ACCESS_TOKEN": "YOUR_TOKEN"
      }
    }
  }
}
```

---

# Available Tools

### 📖 Content Reading

* `read_linkedin_post`

### 🌐 Scraping

* `get_person_profile`
* `get_company_profile`
* `get_job_details`
* `search_jobs`
* `search_recommended_jobs`
* `close_session`

### 📝 Post Management

* `create_linkedin_post`
* `update_linkedin_post`
* `delete_linkedin_post`

### 🖼️ Media

* `upload_linkedin_image`
* `get_linkedin_image`

### 💙 Reactions

* `add_linkedin_reaction`
* `remove_linkedin_reaction`
* `get_linkedin_reactions`

### 👤 Profile & Auth

* `get_linkedin_profile`
* `validate_linkedin_credentials`

More details. See `TOOLS_REFERENCE.md`.

---

# Project Structure

```
linkedin-mcp/
├── linkedin_mcp_server/
│   ├── server.py
│   ├── cli.py
│   ├── config/
│   ├── drivers/
│   └── tools/
├── tests/
│   ├── unit/
│   ├── integration/
├── scripts/
├── .env.example
├── pyproject.toml
├── README.md
└── TOOLS_REFERENCE.md
```

---

# Testing

```bash
# unit tests
uv run pytest tests/unit -v

# integration tests
uv run pytest tests/integration -v

# all tests
uv run pytest tests/ -v
```

Quick API test:

```bash
uv run python scripts/test_api.py
```

---

# Troubleshooting

### ❌ "426 Client Error: Upgrade Required"

Fix:

```
LINKEDIN_API_VERSION=202510
```

### ❌ "LINKEDIN_COOKIE required"

Get fresh cookie from Chrome.

### ❌ "401 Unauthorized"

Generate a new access token.

### ChromeDriver issues

```bash
pip install --upgrade selenium webdriver-manager
```

---

# API Versioning

Current default:

```
202510
```

Check latest:
[https://learn.microsoft.com/en-us/linkedin/marketing/versioning](https://learn.microsoft.com/en-us/linkedin/marketing/versioning)

Update:

```
LINKEDIN_API_VERSION=202511
```

Restart the server.

---

# Contributing

```bash
git clone https://github.com/selvin-paul-raj/Linkedin-MCP-Server.git
cd Linkedin-MCP-Server
uv sync
uv run pytest tests/ -v
uv run ruff format .
uv run pre-commit run --all-files
```

Pull requests welcome.

---

# License

MIT License.
See the `LICENSE` file.

---

# Disclaimer

This tool is for educational and automation purposes.
Follow LinkedIn TOS, API terms, and usage limits.
Use responsibly.

---


**Built with ❤️ for LinkedIn automation**

