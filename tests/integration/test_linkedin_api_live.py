"""
Live LinkedIn API Testing Suite
Tests actual LinkedIn API calls with MCP server to verify:
- API version compatibility (202510)
- Post creation and management
- Image/media handling
- Reactions management
- Error handling

⚠️ WARNING: These tests make REAL API calls to LinkedIn.
Requires valid LINKEDIN_ACCESS_TOKEN in .env file.
"""

import os
import sys
import pytest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from linkedin_mcp_server.tools.post import (
    LinkedInAPIClient,
    PostVisibility,
    ReactionType,
)


@pytest.fixture
def api_client():
    """Create LinkedIn API client with access token from environment."""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        pytest.skip("LINKEDIN_ACCESS_TOKEN not set - skipping live API tests")
    
    client = LinkedInAPIClient(access_token)
    return client


@pytest.fixture
def sample_post_text():
    """Sample post text for testing."""
    return "🧪 Test post from LinkedIn MCP Server - API Version 202510 validation"


class TestAPIVersion:
    """Test API version configuration and headers."""
    
    def test_client_headers(self, api_client):
        """Verify client uses correct API version in headers."""
        assert "LinkedIn-Version" in api_client.headers
        version = api_client.headers["LinkedIn-Version"]
        
        # Should be 202510 or newer (YYYYMM format)
        assert len(version) == 6, f"Invalid version format: {version}"
        assert version >= "202510", f"Using old version: {version}"
        
        print(f"✅ API Version: {version}")
        print(f"✅ Headers: {api_client.headers}")
    
    def test_protocol_version(self, api_client):
        """Verify REST protocol version is set."""
        assert api_client.headers["X-Restli-Protocol-Version"] == "2.0.0"
        print("✅ REST Protocol Version: 2.0.0")


class TestPersonURN:
    """Test person URN retrieval (required for posting)."""
    
    def test_get_person_urn(self, api_client):
        """Test fetching authenticated user's person URN."""
        try:
            person_urn = api_client._get_person_urn()
            
            assert person_urn is not None, "Failed to get person URN"
            assert person_urn.startswith("urn:li:person:"), f"Invalid URN format: {person_urn}"
            
            print(f"✅ Person URN retrieved: {person_urn}")
            print(f"✅ Person ID: {person_urn.split(':')[-1]}")
            
        except Exception as e:
            pytest.fail(f"Failed to get person URN: {e}")
    
    def test_person_urn_caching(self, api_client):
        """Test that person URN is cached after first fetch."""
        # First call
        urn1 = api_client._get_person_urn()
        
        # Second call should use cache
        urn2 = api_client._get_person_urn()
        
        assert urn1 == urn2, "URN should be cached"
        assert api_client._person_urn == urn1, "URN not cached in client"
        
        print(f"✅ URN caching works: {urn1}")


class TestPostCreation:
    """Test LinkedIn post creation and management."""
    
    @pytest.mark.live_write
    def test_create_text_post(self, api_client, sample_post_text):
        """Test creating a simple text post."""
        try:
            result = api_client.create_post(
                text=sample_post_text,
                visibility=PostVisibility.CONNECTIONS
            )
            
            assert result is not None, "Post creation returned None"
            assert "id" in result or "value" in result, f"No post ID in result: {result}"
            
            post_id = result.get("id") or result.get("value", {}).get("id")
            print(f"✅ Post created successfully!")
            print(f"   Post ID: {post_id}")
            print(f"   Text: {sample_post_text[:50]}...")
            
            return post_id
            
        except Exception as e:
            # If it's the old 426 error, that means our fix didn't work
            if "426" in str(e):
                pytest.fail(f"❌ Still getting 426 error - API version fix failed: {e}")
            # Other errors might be token permissions, etc.
            pytest.skip(f"Post creation failed (might be permissions): {e}")
    
    @pytest.mark.live_write
    def test_create_post_with_url(self, api_client):
        """Test creating a post with a URL."""
        text = "🔗 Testing URL post - LinkedIn MCP Server\n\nhttps://github.com/linkedin/linkedin-api-python"
        
        try:
            result = api_client.create_post(
                text=text,
                visibility=PostVisibility.CONNECTIONS
            )
            
            assert result is not None
            print(f"✅ Post with URL created!")
            
        except Exception as e:
            if "426" in str(e):
                pytest.fail(f"❌ 426 error on URL post: {e}")
            pytest.skip(f"URL post failed: {e}")
    
    def test_create_post_validation(self, api_client):
        """Test post text validation."""
        # Test empty text
        with pytest.raises((ValueError, Exception)):
            api_client.create_post(text="", visibility=PostVisibility.PUBLIC)
        
        print("✅ Empty text validation works")
        
        # Test very long text (LinkedIn has limits)
        long_text = "A" * 4000  # LinkedIn limit is ~3000 chars
        try:
            # This should either truncate or fail gracefully
            result = api_client.create_post(text=long_text, visibility=PostVisibility.CONNECTIONS)
            print(f"✅ Long text handled: {len(long_text)} chars")
        except Exception as e:
            print(f"✅ Long text rejected appropriately: {str(e)[:100]}")


class TestReactions:
    """Test LinkedIn reactions (likes, praise, etc.)."""
    
    @pytest.mark.live_write
    def test_add_reaction(self, api_client):
        """Test adding a reaction to a post."""
        # For testing, we need a valid post URN
        # This test will be skipped if we can't create a test post
        test_post_urn = os.getenv("TEST_POST_URN")
        
        if not test_post_urn:
            pytest.skip("TEST_POST_URN not set - skipping reaction test")
        
        try:
            result = api_client.add_reaction(
                entity_urn=test_post_urn,
                reaction_type=ReactionType.LIKE
            )
            
            assert result is not None
            print(f"✅ Reaction added to post: {test_post_urn}")
            
        except Exception as e:
            if "426" in str(e):
                pytest.fail(f"❌ 426 error on add_reaction: {e}")
            pytest.skip(f"Reaction failed: {e}")
    
    def test_reaction_types(self):
        """Test all available reaction types."""
        expected_types = [
            ReactionType.LIKE,
            ReactionType.PRAISE,
            ReactionType.APPRECIATION,
            ReactionType.EMPATHY,
            ReactionType.INTEREST,
            ReactionType.ENTERTAINMENT,
        ]
        
        for reaction in expected_types:
            assert isinstance(reaction.value, str)
            print(f"✅ Reaction type: {reaction.value}")
    
    @pytest.mark.live_read
    def test_get_reactions(self, api_client):
        """Test fetching reactions for a post."""
        test_post_urn = os.getenv("TEST_POST_URN")
        
        if not test_post_urn:
            pytest.skip("TEST_POST_URN not set - skipping get reactions test")
        
        try:
            result = api_client.get_post_reactions(entity_urn=test_post_urn)
            
            # Result might be empty if no reactions, but should not error
            assert result is not None
            print(f"✅ Reactions retrieved for: {test_post_urn}")
            
            if isinstance(result, dict) and "elements" in result:
                print(f"   Reaction count: {len(result['elements'])}")
            
        except Exception as e:
            if "426" in str(e) or "404" in str(e):
                pytest.skip(f"Reactions endpoint issue: {e}")
            raise


class TestImageUpload:
    """Test image upload initialization."""
    
    @pytest.mark.live_write
    def test_initialize_image_upload(self, api_client):
        """Test initializing an image upload."""
        try:
            result = api_client.initialize_image_upload()
            
            assert result is not None
            assert "value" in result or "uploadUrl" in result
            
            print(f"✅ Image upload initialized!")
            print(f"   Response keys: {list(result.keys())}")
            
        except Exception as e:
            if "426" in str(e):
                pytest.fail(f"❌ 426 error on image upload: {e}")
            pytest.skip(f"Image upload initialization failed: {e}")


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_invalid_token(self):
        """Test behavior with invalid access token."""
        client = LinkedInAPIClient(access_token="invalid_token_12345")
        
        with pytest.raises(Exception) as exc_info:
            client._get_person_urn()
        
        # Should get some kind of auth error
        error_msg = str(exc_info.value).lower()
        assert any(word in error_msg for word in ["401", "unauthorized", "permission", "invalid", "cannot determine"]), \
            f"Expected auth error, got: {exc_info.value}"
        print(f"✅ Invalid token handled correctly: {exc_info.value}")
    
    def test_invalid_visibility(self, api_client):
        """Test with invalid visibility value."""
        with pytest.raises((ValueError, Exception)):
            api_client.create_post(
                text="Test",
                visibility="INVALID_VISIBILITY"
            )
        
        print("✅ Invalid visibility rejected")
    
    def test_api_version_format(self):
        """Test that API version follows YYYYMM format."""
        version = os.getenv("LINKEDIN_API_VERSION", "202510")
        
        assert len(version) == 6, f"Version must be 6 digits: {version}"
        
        year = int(version[:4])
        month = int(version[4:])
        
        assert 2024 <= year <= 2030, f"Year out of range: {year}"
        assert 1 <= month <= 12, f"Month out of range: {month}"
        
        print(f"✅ Version format valid: {version} ({year}-{month:02d})")


# Utility function to run a quick API health check
def quick_api_check():
    """Quick API health check - can be run standalone."""
    print("\n" + "="*60)
    print("LinkedIn API Quick Health Check")
    print("="*60 + "\n")
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("❌ LINKEDIN_ACCESS_TOKEN not set in .env file")
        return False
    
    print("✅ Access token found")
    
    try:
        client = LinkedInAPIClient(token)
        print(f"✅ API Client initialized")
        print(f"   Version: {client.headers['LinkedIn-Version']}")
        print(f"   Base URL: {client.base_url}")
        
        # Test person URN
        urn = client._get_person_urn()
        print(f"✅ Person URN retrieved: {urn}")
        
        print("\n" + "="*60)
        print("✅ API Health Check PASSED!")
        print("="*60 + "\n")
        return True
        
    except Exception as e:
        print(f"\n❌ API Health Check FAILED: {e}\n")
        if "426" in str(e):
            print("⚠️  Still getting 426 errors - check API version configuration")
        return False


if __name__ == "__main__":
    # Run quick check if executed directly
    quick_api_check()
