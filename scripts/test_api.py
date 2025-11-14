#!/usr/bin/env python3
"""
Quick LinkedIn API Test Script
Run this to verify your LinkedIn API integration is working.

Usage:
    python test_api.py              # Run health check
    python test_api.py --full       # Run full test suite
    python test_api.py --post       # Create a test post
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_mcp_server.tools.post import (
    LinkedInAPIClient,
    PostVisibility,
    ReactionType,
)


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def health_check():
    """Run API health check."""
    print_header("LinkedIn API Health Check")
    
    # Check environment
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("❌ LINKEDIN_ACCESS_TOKEN not found in environment")
        print("   Make sure you have a .env file with your access token")
        return False
    
    print(f"✅ Access token found: {token[:20]}...")
    
    # Check API version
    api_version = os.getenv("LINKEDIN_API_VERSION", "202510")
    print(f"✅ API Version: {api_version}")
    
    if api_version < "202510":
        print(f"⚠️  WARNING: Using old API version {api_version}")
        print(f"   Current version is 202510 (October 2025)")
    
    # Initialize client
    try:
        client = LinkedInAPIClient(token)
        print(f"✅ API Client initialized")
        print(f"   Base URL: {client.base_url}")
        print(f"   Headers: {len(client.headers)} headers set")
        
        # Verify headers
        if client.headers.get("LinkedIn-Version") != api_version:
            print(f"⚠️  Header version mismatch!")
            print(f"   Expected: {api_version}")
            print(f"   Got: {client.headers.get('LinkedIn-Version')}")
        
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return False
    
    # Test person URN
    print("\n📋 Testing Person URN Retrieval...")
    try:
        urn = client._get_person_urn()
        if urn:
            print(f"✅ Person URN: {urn}")
            person_id = urn.split(":")[-1]
            print(f"   Person ID: {person_id}")
        else:
            print("❌ Failed to get person URN")
            return False
    except Exception as e:
        print(f"❌ Person URN error: {e}")
        if "426" in str(e):
            print("\n⚠️  Getting 426 errors - API version issue!")
            print("   Your API version may be deprecated")
        elif "401" in str(e):
            print("\n⚠️  Getting 401 errors - token issue!")
            print("   Check your LINKEDIN_ACCESS_TOKEN is valid")
        return False
    
    print_header("✅ Health Check PASSED!")
    return True


def test_post_creation():
    """Test creating a LinkedIn post."""
    print_header("Test Post Creation")
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("❌ No access token found")
        return False
    
    client = LinkedInAPIClient(token)
    
    # Create test post
    test_text = """🧪 LinkedIn MCP Server - API Test

This is an automated test post to verify:
✅ API version 202510 compatibility
✅ Post creation functionality
✅ MCP server integration

If you see this, the LinkedIn API is working correctly! 🎉

#LinkedInAPI #MCPServer #Testing"""
    
    print(f"📝 Creating test post...")
    print(f"   Text length: {len(test_text)} characters")
    print(f"   Visibility: CONNECTIONS only")
    
    confirm = input("\n⚠️  This will create a REAL post on LinkedIn. Continue? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Post creation cancelled")
        return False
    
    try:
        result = client.create_post(
            text=test_text,
            visibility=PostVisibility.CONNECTIONS
        )
        
        if result:
            post_id = result.get("id") or result.get("value", {}).get("id")
            print(f"\n✅ Post created successfully!")
            print(f"   Post ID: {post_id}")
            print(f"   Result: {result}")
            
            # Save post ID for future tests
            print(f"\n💡 TIP: Save this post URN for testing reactions:")
            print(f"   export TEST_POST_URN=urn:li:share:{post_id}")
            
            return True
        else:
            print("❌ Post creation returned no result")
            return False
            
    except Exception as e:
        print(f"\n❌ Post creation failed: {e}")
        
        if "426" in str(e):
            print("\n⚠️  ERROR 426: Upgrade Required")
            print("   This means your API version is deprecated")
            print("   Current version should be: 202510")
            print(f"   Your version: {os.getenv('LINKEDIN_API_VERSION', 'not set')}")
        elif "401" in str(e):
            print("\n⚠️  ERROR 401: Unauthorized")
            print("   Check your access token is valid and has w_member_social permission")
        elif "403" in str(e):
            print("\n⚠️  ERROR 403: Forbidden")
            print("   Your token may not have the required permissions")
        
        return False


def test_reactions():
    """Test reaction functionality."""
    print_header("Test Reactions")
    
    post_urn = os.getenv("TEST_POST_URN")
    if not post_urn:
        print("❌ TEST_POST_URN not set in environment")
        print("   Set it with: export TEST_POST_URN=urn:li:share:YOUR_POST_ID")
        return False
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    client = LinkedInAPIClient(token)
    
    print(f"📝 Testing reactions on post: {post_urn}")
    
    # List available reactions
    print("\n🎭 Available reaction types:")
    for reaction in ReactionType:
        print(f"   - {reaction.value}")
    
    # Test getting reactions
    print(f"\n📊 Getting current reactions...")
    try:
        reactions = client.get_post_reactions(entity_urn=post_urn)
        print(f"✅ Reactions retrieved: {reactions}")
    except Exception as e:
        print(f"❌ Get reactions failed: {e}")
    
    # Test adding reaction
    confirm = input("\n⚠️  Add a LIKE reaction to this post? (yes/no): ")
    if confirm.lower() == "yes":
        try:
            result = client.add_reaction(
                entity_urn=post_urn,
                reaction_type=ReactionType.LIKE
            )
            print(f"✅ Reaction added: {result}")
        except Exception as e:
            print(f"❌ Add reaction failed: {e}")
    
    return True


def run_full_tests():
    """Run full pytest test suite."""
    print_header("Running Full Test Suite")
    
    import subprocess
    
    cmd = [
        "pytest",
        "tests/test_linkedin_api_live.py",
        "-v",
        "--tb=short",
        "-m", "not live_write"  # Skip write tests by default
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--full":
            success = run_full_tests()
        elif arg == "--post":
            success = test_post_creation()
        elif arg == "--reactions":
            success = test_reactions()
        elif arg == "--help":
            print(__doc__)
            return
        else:
            print(f"Unknown argument: {arg}")
            print(__doc__)
            return
    else:
        # Default: run health check
        success = health_check()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
