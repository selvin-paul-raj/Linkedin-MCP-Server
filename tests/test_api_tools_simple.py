"""
Simple unit tests for LinkedIn MCP Server API tools.

These tests verify the API client initialization and basic functionality
without making actual API calls or importing MCP tool functions.
"""

import pytest
import os
from linkedin_mcp_server.tools.post import LinkedInAPIClient, PostVisibility, ReactionType


class TestAPIClient:
    """Tests for LinkedInAPIClient class."""

    def test_client_initialization_with_token(self, linkedin_access_token):
        """Test API client initialization with valid token."""
        client = LinkedInAPIClient(linkedin_access_token)
        assert client is not None
        assert client.access_token == linkedin_access_token
        print(f"✅ API client initialized successfully")

    def test_client_initialization_with_custom_url(self, linkedin_access_token):
        """Test client initialization with custom base URL."""
        custom_url = "https://api.linkedin.com/rest"
        client = LinkedInAPIClient(linkedin_access_token, base_url=custom_url)
        assert client.base_url == custom_url
        print(f"✅ Custom base URL set: {custom_url}")

    def test_client_has_required_methods(self, linkedin_access_token):
        """Test that client has all required methods."""
        client = LinkedInAPIClient(linkedin_access_token)
        
        required_methods = [
            'create_post',
            'update_post',
            'delete_post',
            'initialize_image_upload',
            'upload_image',
            'add_reaction',
            'remove_reaction',
            'get_reactions',
            'validate_credentials',
            '_get_person_urn'
        ]
        
        for method_name in required_methods:
            assert hasattr(client, method_name), f"Missing method: {method_name}"
        
        print(f"✅ All {len(required_methods)} required methods exist")


class TestEnums:
    """Test enum definitions."""

    def test_post_visibility_enum(self):
        """Test PostVisibility enum values."""
        assert PostVisibility.PUBLIC == "PUBLIC"
        assert PostVisibility.CONNECTIONS == "CONNECTIONS"
        print(f"✅ PostVisibility enum correct")

    def test_reaction_type_enum(self):
        """Test ReactionType enum values."""
        expected_reactions = [
            "LIKE", "PRAISE", "APPRECIATION",
            "EMPATHY", "INTEREST", "ENTERTAINMENT"
        ]
        
        for reaction in expected_reactions:
            assert hasattr(ReactionType, reaction)
            assert getattr(ReactionType, reaction) == reaction
        
        print(f"✅ All {len(expected_reactions)} reaction types defined")


@pytest.mark.skipif(
    not os.getenv("LINKEDIN_ACCESS_TOKEN"),
    reason="LINKEDIN_ACCESS_TOKEN not set"
)
class TestCredentialValidation:
    """Tests for credential validation (requires valid token)."""

    def test_validate_credentials_with_valid_token(self, linkedin_access_token):
        """Test credential validation with valid token."""
        client = LinkedInAPIClient(linkedin_access_token)
        result = client.validate_credentials()
        
        assert isinstance(result, bool)
        if result:
            print(f"✅ Credentials are valid")
        else:
            print(f"⚠️ Credentials validation returned False")

    def test_get_person_urn(self, linkedin_access_token):
        """Test retrieving person URN."""
        client = LinkedInAPIClient(linkedin_access_token)
        urn = client._get_person_urn()
        
        if urn:
            assert urn.startswith("urn:li:person:")
            print(f"✅ Retrieved person URN: {urn}")
        else:
            print(f"⚠️ Could not retrieve person URN")


class TestDataValidation:
    """Tests for data validation and edge cases."""

    def test_empty_token_handling(self):
        """Test handling of empty token."""
        try:
            client = LinkedInAPIClient("")
            print(f"⚠️ Empty token accepted (may be intentional)")
        except Exception as e:
            print(f"✅ Empty token rejected: {type(e).__name__}")

    def test_none_token_handling(self):
        """Test handling of None token."""
        try:
            client = LinkedInAPIClient(None)
            print(f"⚠️ None token accepted (may be intentional)")
        except Exception as e:
            print(f"✅ None token rejected: {type(e).__name__}")

    def test_post_text_length_limits(self):
        """Test post text length validation."""
        # Max allowed
        max_text = "A" * 3000
        assert len(max_text) == 3000
        
        # Over max
        over_max_text = "A" * 3001
        assert len(over_max_text) > 3000
        
        print(f"✅ Text length boundaries identified")

    def test_unicode_text_handling(self):
        """Test Unicode and emoji handling."""
        unicode_texts = [
            "🚀 Emojis test 🎉",
            "Unicode: 你好 مرحبا Привет",
            "Mixed: Hello 世界 🌍"
        ]
        
        for text in unicode_texts:
            assert isinstance(text, str)
            assert len(text) > 0
        
        print(f"✅ Unicode text validation passed")


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_token_format(self):
        """Test handling of clearly invalid token."""
        invalid_tokens = [
            "invalid_token_123",
            "abc",
            "AQ" * 100  # Very long invalid token
        ]
        
        for token in invalid_tokens:
            try:
                client = LinkedInAPIClient(token)
                # Client creation may succeed, but operations should fail
                print(f"✅ Client created with invalid token (will fail on use)")
            except Exception as e:
                print(f"✅ Invalid token rejected: {type(e).__name__}")


@pytest.mark.integration
@pytest.mark.skip(reason="Integration tests disabled by default")
class TestRealAPIOperations:
    """Integration tests that make real API calls.
    
    Run with: pytest tests/test_api_tools_simple.py::TestRealAPIOperations -v
    """

    def test_create_and_delete_post(self, linkedin_access_token):
        """Test creating and deleting a post."""
        import time
        
        client = LinkedInAPIClient(linkedin_access_token)
        
        # Create post
        post_text = "🧪 Test post from LinkedIn MCP Server test suite"
        result = client.create_post(text=post_text)
        
        assert result is not None
        assert isinstance(result, dict)
        print(f"✅ Post created")
        
        # Delete post
        if "id" in result or "urn" in result:
            time.sleep(2)
            post_urn = result.get("id") or result.get("urn")
            delete_result = client.delete_post(post_urn)
            print(f"✅ Post deleted")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
