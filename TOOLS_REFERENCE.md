# LinkedIn MCP Server - Tools Reference

Complete documentation for all 16 LinkedIn automation tools available in this MCP server.

---

## 📑 Table of Contents

- [Scraping Tools (Browser-based)](#scraping-tools-browser-based)
  - [get_person_profile](#get_person_profile)
  - [get_company_profile](#get_company_profile)
  - [get_job_details](#get_job_details)
  - [search_jobs](#search_jobs)
  - [search_recommended_jobs](#search_recommended_jobs)
  - [close_session](#close_session)
- [API Tools (REST API-based)](#api-tools-rest-api-based)
  - [create_linkedin_post](#create_linkedin_post)
  - [update_linkedin_post](#update_linkedin_post)
  - [delete_linkedin_post](#delete_linkedin_post)
  - [upload_linkedin_image](#upload_linkedin_image)
  - [get_linkedin_image](#get_linkedin_image)
  - [add_linkedin_reaction](#add_linkedin_reaction)
  - [remove_linkedin_reaction](#remove_linkedin_reaction)
  - [get_linkedin_reactions](#get_linkedin_reactions)
  - [get_linkedin_profile](#get_linkedin_profile)
  - [validate_linkedin_credentials](#validate_linkedin_credentials)

---

## Scraping Tools (Browser-based)

These tools use browser automation via Selenium to scrape LinkedIn data. Requires a valid LinkedIn session cookie.

### get_person_profile

Extract detailed information from a LinkedIn profile.

**Parameters:**
- `profile_url` (string, required): LinkedIn profile URL
  - Format: `https://www.linkedin.com/in/username`
  - Example: `https://www.linkedin.com/in/selvin-paul-raj`

**Returns:**
```python
{
  "name": "Selvin PaulRaj K",
  "job_title": "Senior Software Engineer",
  "company": "Tech Company Inc.",
  "location": "San Francisco, CA",
  "about": "Passionate developer...",
  "experiences": [
    {
      "title": "Senior Engineer",
      "company": "Tech Company",
      "duration": "2020-Present",
      "description": "..."
    }
  ],
  "education": [...],
  "skills": ["Python", "JavaScript", "AI"],
  "contact_info": {...}
}
```

**Example Usage:**
```
Claude: "Get the LinkedIn profile for https://www.linkedin.com/in/selvin-paul-raj"
```

**Common Errors:**
- `Profile not found` - Invalid URL or profile doesn't exist
- `Cookie expired` - Need to refresh LinkedIn session cookie

---

### get_company_profile

Get comprehensive company information from LinkedIn.

**Parameters:**
- `company_url` (string, required): LinkedIn company URL
  - Format: `https://www.linkedin.com/company/company-name`
  - Example: `https://www.linkedin.com/company/microsoft`

**Returns:**
```python
{
  "name": "Microsoft",
  "tagline": "Our mission is to empower...",
  "about": "Microsoft Corporation is...",
  "website": "https://www.microsoft.com",
  "industry": "Software Development",
  "company_size": "10,001+ employees",
  "headquarters": "Redmond, Washington",
  "founded": "1975",
  "specialties": ["Cloud Computing", "AI", ...]
}
```

**Example Usage:**
```
Claude: "Get information about Microsoft from LinkedIn"
Claude: "What does the company at https://www.linkedin.com/company/openai do?"
```

**Common Errors:**
- `Company page not found` - Invalid URL or private company page
- `Access denied` - Company has restricted access

---

### get_job_details

Retrieve detailed information about a specific job posting.

**Parameters:**
- `job_url` (string, required): LinkedIn job posting URL
  - Format: `https://www.linkedin.com/jobs/view/123456789`
  - Example: `https://www.linkedin.com/jobs/view/3845678912`

**Returns:**
```python
{
  "title": "Senior Python Developer",
  "company": "Tech Startup Inc.",
  "location": "San Francisco, CA (Remote)",
  "employment_type": "Full-time",
  "seniority_level": "Mid-Senior level",
  "posted_date": "2 days ago",
  "applicants": "120 applicants",
  "description": "We are seeking...",
  "qualifications": [...],
  "benefits": [...],
  "apply_url": "..."
}
```

**Example Usage:**
```
Claude: "Get details for this job: https://www.linkedin.com/jobs/view/3845678912"
```

**Common Errors:**
- `Job not found` - Job posting has been removed or filled
- `Login required` - Job requires authentication to view

---

### search_jobs

Search for jobs on LinkedIn with optional filters.

**Parameters:**
- `keywords` (string, optional): Job search keywords
  - Example: `"python developer"`, `"data scientist remote"`
- `location` (string, optional): Job location
  - Example: `"San Francisco, CA"`, `"Remote"`
- `job_type` (string, optional): Employment type
  - Values: `"full-time"`, `"part-time"`, `"contract"`, `"internship"`
- `experience_level` (string, optional): Experience level
  - Values: `"entry"`, `"associate"`, `"mid-senior"`, `"director"`, `"executive"`
- `remote` (boolean, optional): Filter for remote jobs
  - Default: `false`
- `limit` (integer, optional): Maximum results to return
  - Default: `25`, Max: `100`

**Returns:**
```python
{
  "total_results": 1245,
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "Remote",
      "url": "https://www.linkedin.com/jobs/view/123...",
      "posted_date": "1 day ago",
      "applicants": "50 applicants"
    },
    ...
  ]
}
```

**Example Usage:**
```
Claude: "Find data engineer jobs in San Francisco"
Claude: "Search for remote Python developer positions with mid-senior experience level"
Claude: "Look for entry-level internships in AI/ML"
```

**Common Errors:**
- `No results found` - Try broader search terms
- `Rate limited` - LinkedIn has rate limits, try again later

---

### search_recommended_jobs

Get personalized job recommendations based on your LinkedIn profile.

**Parameters:**
- `limit` (integer, optional): Maximum recommendations to return
  - Default: `25`, Max: `100`

**Returns:**
```python
{
  "total_recommendations": 85,
  "jobs": [
    {
      "title": "Machine Learning Engineer",
      "company": "AI Startup",
      "location": "San Francisco, CA",
      "url": "https://www.linkedin.com/jobs/view/...",
      "match_score": "95%",
      "why_recommended": "Your skills match 8 of 10 required skills"
    },
    ...
  ]
}
```

**Example Usage:**
```
Claude: "What jobs does LinkedIn recommend for me?"
Claude: "Get my top 10 job recommendations"
```

**Common Errors:**
- `No recommendations` - Update your LinkedIn profile for better matches
- `Cookie expired` - Recommendations require active session

---

### close_session

Properly close the browser session to free resources.

**Parameters:** None

**Returns:**
```python
{
  "status": "success",
  "message": "Browser session closed successfully"
}
```

**Example Usage:**
```
Claude: "Close the LinkedIn browser session"
```

**Notes:**
- Sessions auto-close after 30 minutes of inactivity
- Recommended after completing scraping tasks
- Frees up system memory and browser resources

---

## API Tools (REST API-based)

These tools use the LinkedIn REST API for content creation and management. Requires a valid access token with `w_member_social` permission.

### create_linkedin_post

Create and publish a post on LinkedIn with optional image.

**Parameters:**
- `text` (string, required): Post content (max 3000 characters)
- `image_url` (string, optional): URL of image to attach
  - Formats: JPG, PNG, GIF
  - Max size: 5MB
  - Will be automatically downloaded and uploaded

**Returns:**
```python
{
  "status": "success",
  "post_id": "urn:li:share:7234567890123456789",
  "post_url": "https://www.linkedin.com/feed/update/urn:li:share:7234567890123456789",
  "message": "Post created successfully",
  "author": "urn:li:person:vnEC3sIkEF"
}
```

**Example Usage:**
```
Claude: "Create a LinkedIn post: 'Excited to announce my new project! 🚀'"

Claude: "Post on LinkedIn: 'Check out this amazing visualization!' with image https://example.com/chart.png"

Claude: "Share this on LinkedIn: 'Just completed my certification in AI/ML. Here's what I learned: [...]'"
```

**Text Formatting:**
- Maximum 3000 characters
- Supports Unicode/emojis: ✅ 🚀 💡
- Line breaks preserved
- URLs automatically linkified

**Common Errors:**
- `Text too long` - Reduce to under 3000 characters
- `Invalid image URL` - Check URL is publicly accessible
- `Upload failed` - Image may be too large (max 5MB)
- `Unauthorized` - Access token missing or invalid

---

### update_linkedin_post

Update an existing LinkedIn post.

**Parameters:**
- `post_id` (string, required): Post URN to update
  - Format: `urn:li:share:1234567890123456789`
- `text` (string, required): New post content

**Returns:**
```python
{
  "status": "success",
  "post_id": "urn:li:share:7234567890123456789",
  "message": "Post updated successfully"
}
```

**Example Usage:**
```
Claude: "Update post urn:li:share:7234567890123456789 with text 'Updated content goes here'"
```

**Limitations:**
- Can only update your own posts
- Images cannot be changed (must delete and recreate)
- Some metadata (visibility, timestamp) cannot be changed

**Common Errors:**
- `Post not found` - Invalid post_id or post was deleted
- `Permission denied` - Can only update your own posts
- `Post locked` - LinkedIn locked the post for policy violation

---

### delete_linkedin_post

Delete a LinkedIn post.

**Parameters:**
- `post_id` (string, required): Post URN to delete
  - Format: `urn:li:share:1234567890123456789`

**Returns:**
```python
{
  "status": "success",
  "message": "Post deleted successfully"
}
```

**Example Usage:**
```
Claude: "Delete LinkedIn post urn:li:share:7234567890123456789"
Claude: "Remove my last post"
```

**Notes:**
- Deletion is permanent and cannot be undone
- All reactions and comments are also deleted
- Can only delete your own posts

**Common Errors:**
- `Post not found` - Already deleted or invalid ID
- `Permission denied` - Can only delete your own posts

---

### upload_linkedin_image

Upload an image to LinkedIn for use in posts.

**Parameters:**
- `image_url` (string, required): Publicly accessible image URL
  - Formats: JPG, PNG, GIF
  - Max size: 5MB
  - Must be downloadable without authentication

**Returns:**
```python
{
  "status": "success",
  "image_id": "urn:li:digitalmediaAsset:C5605AQHx...",
  "message": "Image uploaded successfully",
  "metadata": {
    "size": 245678,
    "format": "image/jpeg"
  }
}
```

**Example Usage:**
```
Claude: "Upload this image to LinkedIn: https://example.com/photo.jpg"
```

**Supported Formats:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)

**Common Errors:**
- `Download failed` - URL not accessible or requires auth
- `Invalid format` - Use JPG, PNG, or GIF only
- `File too large` - Compress image to under 5MB
- `Upload timeout` - Large images may timeout, reduce size

---

### get_linkedin_image

Get metadata about an uploaded LinkedIn image.

**Parameters:**
- `image_id` (string, required): Image URN
  - Format: `urn:li:digitalmediaAsset:C5605AQHx...`

**Returns:**
```python
{
  "status": "success",
  "image_id": "urn:li:digitalmediaAsset:C5605AQHx...",
  "metadata": {
    "uploadDate": "2024-01-15T10:30:00Z",
    "size": 245678,
    "format": "image/jpeg",
    "status": "AVAILABLE"
  }
}
```

**Example Usage:**
```
Claude: "Get info for image urn:li:digitalmediaAsset:C5605AQHx..."
```

**Common Errors:**
- `Image not found` - Invalid ID or image was deleted
- `Access denied` - Can only view your own uploaded images

---

### add_linkedin_reaction

Add a reaction to a LinkedIn post.

**Parameters:**
- `post_id` (string, required): Post URN to react to
  - Format: `urn:li:share:1234567890123456789`
- `reaction_type` (string, optional): Type of reaction
  - Values: `"LIKE"`, `"PRAISE"`, `"APPRECIATION"`, `"EMPATHY"`, `"INTEREST"`, `"ENTERTAINMENT"`
  - Default: `"LIKE"`

**Returns:**
```python
{
  "status": "success",
  "message": "Reaction added successfully",
  "reaction_type": "PRAISE"
}
```

**Reaction Types:**
- `LIKE` - 👍 Classic like
- `PRAISE` - 🎉 Celebrate
- `APPRECIATION` - ❤️ Love
- `EMPATHY` - 🤗 Support
- `INTEREST` - 💡 Insightful
- `ENTERTAINMENT` - 😂 Funny

**Example Usage:**
```
Claude: "Add a PRAISE reaction to post urn:li:share:7234567890123456789"
Claude: "React with APPRECIATION to the latest post"
Claude: "Like this post: urn:li:share:7234567890123456789"
```

**Notes:**
- Only one reaction per post (will replace existing)
- Cannot react to private/deleted posts

**Common Errors:**
- `Post not found` - Invalid post_id
- `Invalid reaction type` - Use one of the supported types
- `Already reacted` - Previous reaction will be replaced

---

### remove_linkedin_reaction

Remove your reaction from a LinkedIn post.

**Parameters:**
- `post_id` (string, required): Post URN to remove reaction from
  - Format: `urn:li:share:1234567890123456789`

**Returns:**
```python
{
  "status": "success",
  "message": "Reaction removed successfully"
}
```

**Example Usage:**
```
Claude: "Remove my reaction from post urn:li:share:7234567890123456789"
Claude: "Unlike this post: urn:li:share:7234567890123456789"
```

**Common Errors:**
- `No reaction found` - You haven't reacted to this post
- `Post not found` - Invalid post_id

---

### get_linkedin_reactions

Get all reactions on a LinkedIn post.

**Parameters:**
- `post_id` (string, required): Post URN to get reactions for
  - Format: `urn:li:share:1234567890123456789`

**Returns:**
```python
{
  "status": "success",
  "total_reactions": 245,
  "reactions": {
    "LIKE": 150,
    "PRAISE": 45,
    "APPRECIATION": 30,
    "EMPATHY": 10,
    "INTEREST": 8,
    "ENTERTAINMENT": 2
  },
  "your_reaction": "LIKE"
}
```

**Example Usage:**
```
Claude: "How many reactions does post urn:li:share:7234567890123456789 have?"
Claude: "Show me the reaction breakdown for my latest post"
```

**Common Errors:**
- `Post not found` - Invalid post_id or private post
- `Access denied` - Post visibility settings prevent viewing reactions

---

### get_linkedin_profile

Get your authenticated LinkedIn profile information.

**Parameters:** None

**Returns:**
```python
{
  "status": "success",
  "profile": {
    "person_urn": "urn:li:person:vnEC3sIkEF",
    "sub": "vnEC3sIkEF",
    "name": "Selvin PaulRaj K",
    "given_name": "Selvin",
    "family_name": "PaulRaj K",
    "email": "selvinpaulgomathi@gmail.com",
    "email_verified": true,
    "picture": "https://media.licdn.com/dms/image/..."
  }
}
```

**Example Usage:**
```
Claude: "What's my LinkedIn profile information?"
Claude: "Get my LinkedIn Person URN"
```

**Notes:**
- Uses `/v2/userinfo` endpoint
- Returns information based on access token
- Person URN used for post creation

**Common Errors:**
- `Unauthorized` - Access token invalid or expired
- `Permission denied` - Token missing required scopes

---

### validate_linkedin_credentials

Validate that LinkedIn API credentials are working.

**Parameters:** None

**Returns:**
```python
{
  "status": "valid",
  "person_urn": "urn:li:person:vnEC3sIkEF",
  "message": "Credentials are valid and working",
  "permissions": ["w_member_social"]
}
```

**Example Usage:**
```
Claude: "Check if my LinkedIn API credentials are valid"
Claude: "Validate LinkedIn access token"
```

**Validation Checks:**
- Access token present
- Token format valid
- Can retrieve person URN
- API endpoint accessible

**Common Errors:**
- `Invalid token` - Token malformed or expired
- `Missing permissions` - Token lacks required scopes
- `API unreachable` - Network or LinkedIn API issues

---

## 🔍 Tool Selection Guide

### When to use Scraping Tools vs API Tools

**Use Scraping Tools when:**
- ✅ Reading profile information (yours or others)
- ✅ Researching companies
- ✅ Searching for jobs
- ✅ Getting job recommendations
- ✅ Viewing public content

**Use API Tools when:**
- ✅ Creating your own posts
- ✅ Managing your content (update/delete)
- ✅ Uploading media (images)
- ✅ Reacting to posts
- ✅ Programmatic content creation

---

## 🛡️ Best Practices

### General
1. **Handle errors gracefully** - Always check for error responses
2. **Rate limiting** - Don't spam requests, use reasonable delays
3. **Validate inputs** - Check URLs and parameters before calling
4. **Clean up** - Close sessions when done scraping

### Scraping
1. **Cookie rotation** - Refresh cookies every 30 days
2. **Respect robots.txt** - Don't scrape aggressively
3. **Use delays** - Add delays between requests
4. **Handle captchas** - Be prepared for anti-bot measures

### API
1. **Token security** - Never expose access tokens
2. **Check permissions** - Verify token has required scopes
3. **Monitor quotas** - LinkedIn has API usage limits
4. **Error handling** - Implement retry logic for network errors

---

## 📊 Common Workflows

### Profile Research Workflow
```
1. get_person_profile - Get target profile
2. get_company_profile - Research their company
3. search_jobs - Find related opportunities
4. close_session - Clean up
```

### Content Creation Workflow
```
1. validate_linkedin_credentials - Check API access
2. upload_linkedin_image - Upload media (if needed)
3. create_linkedin_post - Publish post
4. add_linkedin_reaction - React to engage
```

### Job Search Workflow
```
1. search_jobs - Find relevant jobs
2. get_job_details - Get detailed info
3. search_recommended_jobs - Get personalized matches
4. close_session - Clean up
```

---

## 🔧 Troubleshooting

### Tool Not Working

**Check:**
1. Are credentials configured correctly?
2. Is the cookie/token expired?
3. Are parameters in the correct format?
4. Check error message for specific issue

### Performance Issues

**Solutions:**
1. Use `limit` parameter to reduce result size
2. Close sessions when done
3. Avoid parallel scraping requests
4. Use API tools instead of scraping when possible

### API Errors

**Common fixes:**
1. Regenerate access token
2. Verify app permissions
3. Check LinkedIn API status
4. Review API usage quota

---

**For additional support, see [README.md](README.md) or open an issue on GitHub.**

**Author:** Selvin PaulRaj K  
**GitHub:** https://github.com/selvin-paul-raj
