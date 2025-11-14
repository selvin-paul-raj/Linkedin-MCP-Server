"""
Pytest configuration and fixtures for LinkedIn MCP Server tests.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def linkedin_cookie():
    """Get LinkedIn session cookie from environment."""
    cookie = os.getenv("LINKEDIN_COOKIE")
    if not cookie:
        pytest.skip("LINKEDIN_COOKIE not set in environment")
    return cookie


@pytest.fixture(scope="session")
def linkedin_access_token():
    """Get LinkedIn API access token from environment."""
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        pytest.skip("LINKEDIN_ACCESS_TOKEN not set in environment")
    return token


@pytest.fixture(scope="session")
def linkedin_client_id():
    """Get LinkedIn client ID from environment."""
    return os.getenv("LINKEDIN_CLIENT_ID")


@pytest.fixture(scope="session")
def linkedin_client_secret():
    """Get LinkedIn client secret from environment."""
    return os.getenv("LINKEDIN_CLIENT_SECRET")


@pytest.fixture(scope="session")
def test_profile_url():
    """Test LinkedIn profile URL."""
    return "https://www.linkedin.com/in/williamhgates"


@pytest.fixture(scope="session")
def test_company_url():
    """Test LinkedIn company URL."""
    return "https://www.linkedin.com/company/microsoft"


@pytest.fixture(scope="session")
def test_job_keywords():
    """Test job search keywords."""
    return "python developer"


@pytest.fixture
def sample_post_text():
    """Sample text for creating test posts."""
    return "🚀 Test post from LinkedIn MCP Server automated testing suite. #Testing #Automation"


@pytest.fixture
def sample_image_url():
    """Sample public image URL for testing."""
    return "https://picsum.photos/800/600"
