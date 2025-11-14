#!/usr/bin/env python3
"""
Test script to read LinkedIn posts from URLs.
Tests with the provided desktop and mobile URLs.
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_mcp_server.tools.post import LinkedInAPIClient

# Load environment
load_dotenv()


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def print_post_details(result):
    """Pretty print post details."""
    if result["status"] == "success":
        print("✅ Post retrieved successfully!\n")
        
        data = result["data"]
        
        print(f"📝 Post ID: {result.get('post_id', 'Unknown')}")
        print(f"🔗 URL: {result.get('url', 'Unknown')}\n")
        
        print(f"👤 Author: {data.get('author', 'Unknown')}")
        if data.get('author_title'):
            print(f"   Title: {data.get('author_title')}")
        
        print(f"📅 Posted: {data.get('posted_date', 'Unknown')}")
        print()
        
        print("📊 Engagement:")
        print(f"   👍 Reactions: {data.get('reactions', '0')}")
        print(f"   💬 Comments: {data.get('comments', '0')}")
        print(f"   🔄 Reposts: {data.get('reposts', '0')}")
        print()
        
        if data.get('content'):
            print("📄 Content:")
            print("-" * 80)
            print(data['content'])
            print("-" * 80)
        else:
            print("📄 Content: (No text content or failed to extract)")
        
        if data.get('images'):
            print(f"\n🖼️  Images: {len(data['images'])} found")
            for i, img in enumerate(data['images'][:3], 1):
                print(f"   {i}. {img[:70]}...")
        
        if data.get('has_video'):
            print("\n🎥 Video: Present")
        
        if data.get('article_title'):
            print(f"\n📰 Article: {data['article_title']}")
        
    else:
        print(f"❌ Error: {result.get('message', 'Unknown error')}")
        if 'note' in result:
            print(f"   Note: {result['note']}")
        if 'extracted_post_id' in result:
            print(f"   Extracted ID: {result['extracted_post_id']}")


async def test_url_extraction():
    """Test URL parsing and ID extraction."""
    print_header("Testing URL Parsing")
    
    test_urls = [
        "https://www.linkedin.com/posts/adinathm_machine-learning-overview-activity-7394701839126016000-3V9W?utm_source=social_share_send",
        "https://www.linkedin.com/posts/aemal_llm-ai-promptengineering-activity-7394335719143555072-ye8K?utm_source=social_share_send",
        "https://www.linkedin.com/feed/update/urn:li:activity:7394701839126016000",
    ]
    
    for url in test_urls:
        post_id = LinkedInAPIClient.extract_post_id_from_url(url)
        if post_id:
            print(f"✅ URL: {url[:60]}...")
            print(f"   Post ID: {post_id}\n")
        else:
            print(f"❌ Failed to extract ID from: {url[:60]}...\n")


async def test_read_post(post_url, label):
    """Test reading a LinkedIn post."""
    print_header(f"Testing: {label}")
    
    print(f"URL: {post_url}\n")
    print("Fetching post data...\n")
    
    # Directly test the extraction and scraping
    try:
        # Test ID extraction
        post_id = LinkedInAPIClient.extract_post_id_from_url(post_url)
        print(f"✅ Extracted Post ID: {post_id}\n")
        
        # Now simulate what the MCP tool would do
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        import time
        
        linkedin_cookie = os.getenv("LINKEDIN_COOKIE")
        
        # Setup Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # Login with cookie
            driver.get("https://www.linkedin.com")
            driver.add_cookie({
                'name': 'li_at',
                'value': linkedin_cookie.replace('li_at=', ''),
                'domain': '.linkedin.com'
            })
            
            # Navigate to post
            clean_url = post_url.split('?')[0]
            driver.get(clean_url)
            time.sleep(4)  # Wait for page load
            
            # Extract post data
            result = {
                "status": "success",
                "post_id": post_id,
                "url": clean_url,
                "data": {}
            }
            
            try:
                author_elem = driver.find_element(By.CSS_SELECTOR, ".update-components-actor__name, .feed-shared-actor__name")
                result["data"]["author"] = author_elem.text
            except Exception as e:
                result["data"]["author"] = f"Unknown (error: {str(e)[:50]})"
            
            try:
                title_elem = driver.find_element(By.CSS_SELECTOR, ".update-components-actor__description, .feed-shared-actor__description")
                result["data"]["author_title"] = title_elem.text
            except:
                result["data"]["author_title"] = ""
            
            try:
                content_elem = driver.find_element(By.CSS_SELECTOR, ".feed-shared-update-v2__description, .feed-shared-text, .break-words")
                result["data"]["content"] = content_elem.text
            except:
                try:
                    content_elem = driver.find_element(By.CSS_SELECTOR, "[dir='ltr'] .break-words")
                    result["data"]["content"] = content_elem.text
                except:
                    result["data"]["content"] = ""
            
            try:
                date_elem = driver.find_element(By.CSS_SELECTOR, ".update-components-actor__sub-description, .feed-shared-actor__sub-description")
                result["data"]["posted_date"] = date_elem.text.split('•')[0].strip()
            except:
                result["data"]["posted_date"] = "Unknown"
            
            try:
                reactions_elem = driver.find_element(By.CSS_SELECTOR, ".social-details-social-counts__reactions-count, [aria-label*='reaction']")
                result["data"]["reactions"] = reactions_elem.text
            except:
                result["data"]["reactions"] = "0"
            
            try:
                comments_elem = driver.find_element(By.CSS_SELECTOR, ".social-details-social-counts__comments, [aria-label*='comment']")
                result["data"]["comments"] = comments_elem.text.split()[0] if comments_elem.text else "0"
            except:
                result["data"]["comments"] = "0"
            
            try:
                reposts_elem = driver.find_element(By.CSS_SELECTOR, "[aria-label*='repost']")
                result["data"]["reposts"] = reposts_elem.text.split()[0] if reposts_elem.text else "0"
            except:
                result["data"]["reposts"] = "0"
            
            try:
                image_elems = driver.find_elements(By.CSS_SELECTOR, ".feed-shared-image__container img, .feed-shared-image img")
                images = []
                for img in image_elems:
                    src = img.get_attribute("src")
                    if src and 'media.licdn.com' in src:
                        images.append(src)
                result["data"]["images"] = images[:5]
            except:
                result["data"]["images"] = []
            
            try:
                video_elem = driver.find_element(By.CSS_SELECTOR, "video")
                result["data"]["has_video"] = True
            except:
                result["data"]["has_video"] = False
            
            try:
                article_elem = driver.find_element(By.CSS_SELECTOR, ".feed-shared-article, .feed-shared-external-article")
                article_title = article_elem.find_element(By.CSS_SELECTOR, ".feed-shared-article__title").text
                result["data"]["article_title"] = article_title
            except:
                result["data"]["article_title"] = None
            
            print_post_details(result)
            
        finally:
            driver.quit()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Main test function."""
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " LinkedIn Post Reader - Test Script".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    
    # Check environment
    print_header("Environment Check")
    
    cookie = os.getenv("LINKEDIN_COOKIE")
    if cookie:
        print(f"✅ LINKEDIN_COOKIE: Set ({len(cookie)} chars)")
    else:
        print("❌ LINKEDIN_COOKIE: Not set")
        print("   Set LINKEDIN_COOKIE in .env file to test scraping")
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if token:
        print(f"✅ LINKEDIN_ACCESS_TOKEN: Set ({token[:20]}...)")
    else:
        print("⚠️  LINKEDIN_ACCESS_TOKEN: Not set (API features disabled)")
    
    # Test URL extraction
    await test_url_extraction()
    
    # Test URLs provided by user
    desktop_url = "https://www.linkedin.com/posts/adinathm_machine-learning-overview-activity-7394701839126016000-3V9W?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAEF8MFYB-iBhV0RpnDuuQeYMlnP1J6y6Eso"
    
    phone_url = "https://www.linkedin.com/posts/aemal_llm-ai-promptengineering-activity-7394335719143555072-ye8K?utm_source=social_share_send&utm_medium=android_app&rcm=ACoAAEF8MFYB-iBhV0RpnDuuQeYMlnP1J6y6Eso&utm_campaign=copy_link"
    
    if cookie:
        # Test desktop URL
        await test_read_post(desktop_url, "Desktop URL - Machine Learning Post")
        
        # Test phone URL
        await test_read_post(phone_url, "Mobile URL - LLM/AI Post")
    else:
        print_header("Skipping Post Reading Tests")
        print("LINKEDIN_COOKIE not set. Install instructions:")
        print()
        print("1. Login to LinkedIn in Chrome")
        print("2. Open Developer Tools (F12)")
        print("3. Go to Application > Cookies > https://www.linkedin.com")
        print("4. Copy the 'li_at' cookie value")
        print("5. Add to .env file: LINKEDIN_COOKIE=li_at=YOUR_COOKIE_VALUE")
        print()
        print("Extracted Post IDs from URLs:")
        print(f"  Desktop: {LinkedInAPIClient.extract_post_id_from_url(desktop_url)}")
        print(f"  Mobile: {LinkedInAPIClient.extract_post_id_from_url(phone_url)}")
    
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " Test Complete!".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()


if __name__ == "__main__":
    asyncio.run(main())
