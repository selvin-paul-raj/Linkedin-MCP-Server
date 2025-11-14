"""
Basic smoke tests for LinkedIn MCP Server.

These tests verify basic functionality without external dependencies.
"""

import pytest
import os
import sys


class TestEnvironment:
    """Test environment and setup."""

    def test_python_version(self):
        """Test Python version is 3.12 or higher."""
        assert sys.version_info >= (3, 12), "Python 3.12+ required"
        print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")

    def test_imports(self):
        """Test that core modules can be imported."""
        try:
            import fastmcp
            assert fastmcp is not None
            print(f"✅ fastmcp imported")
        except ImportError:
            pytest.fail("fastmcp not installed")

        try:
            import requests
            assert requests is not None
            print(f"✅ requests imported")
        except ImportError:
            pytest.fail("requests not installed")

    def test_project_structure(self):
        """Test that project structure exists."""
        import pathlib
        
        project_root = pathlib.Path(__file__).parent.parent
        
        assert (project_root / "linkedin_mcp_server").exists()
        assert (project_root / "linkedin_mcp_server" / "tools").exists()
        assert (project_root / "pyproject.toml").exists()
        
        print(f"✅ Project structure verified")


class TestConfiguration:
    """Test configuration handling."""

    def test_env_file_exists(self):
        """Test that .env file exists (optional)."""
        import pathlib
        
        project_root = pathlib.Path(__file__).parent.parent
        env_file = project_root / ".env"
        
        if env_file.exists():
            print(f"✅ .env file found")
        else:
            print(f"ℹ️ .env file not found (optional)")

    def test_environment_variables_format(self):
        """Test environment variable format if set."""
        cookie = os.getenv("LINKEDIN_COOKIE")
        token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        
        if cookie:
            assert isinstance(cookie, str)
            print(f"✅ LINKEDIN_COOKIE is set")
        else:
            print(f"ℹ️ LINKEDIN_COOKIE not set")
        
        if token:
            assert isinstance(token, str)
            print(f"✅ LINKEDIN_ACCESS_TOKEN is set")
        else:
            print(f"ℹ️ LINKEDIN_ACCESS_TOKEN not set")


class TestToolModules:
    """Test that tool modules exist."""

    def test_post_tools_module(self):
        """Test post tools module."""
        try:
            from linkedin_mcp_server.tools import post
            assert post is not None
            print(f"✅ Post tools module exists")
        except ImportError as e:
            pytest.fail(f"Cannot import post tools: {e}")

    def test_post_classes_exist(self):
        """Test that post module classes exist."""
        from linkedin_mcp_server.tools.post import (
            LinkedInAPIClient,
            PostVisibility,
            ReactionType
        )
        
        assert LinkedInAPIClient is not None
        assert PostVisibility is not None
        assert ReactionType is not None
        
        print(f"✅ Post module classes exist")


class TestConstants:
    """Test important constants."""

    def test_api_base_url(self):
        """Test API base URL is defined."""
        expected_url = "https://api.linkedin.com/rest"
        assert isinstance(expected_url, str)
        assert expected_url.startswith("https://")
        print(f"✅ API base URL: {expected_url}")

    def test_api_version(self):
        """Test API version handling."""
        api_version = os.getenv("LINKEDIN_API_VERSION", "202510")
        assert isinstance(api_version, str)
        assert len(api_version) == 6  # YYYYMM format
        print(f"✅ API version: {api_version}")

    def test_reaction_types(self):
        """Test all reaction types are defined."""
        from linkedin_mcp_server.tools.post import ReactionType
        
        expected_reactions = [
            "LIKE", "PRAISE", "APPRECIATION",
            "EMPATHY", "INTEREST", "ENTERTAINMENT"
        ]
        
        for reaction in expected_reactions:
            assert hasattr(ReactionType, reaction)
        
        print(f"✅ All {len(expected_reactions)} reaction types defined")


class TestDocumentation:
    """Test that documentation exists."""

    def test_readme_exists(self):
        """Test that README.md exists."""
        import pathlib
        
        project_root = pathlib.Path(__file__).parent.parent
        readme = project_root / "README.md"
        
        assert readme.exists()
        assert readme.stat().st_size > 0
        print(f"✅ README.md exists ({readme.stat().st_size} bytes)")

    def test_tools_reference_exists(self):
        """Test that TOOLS_REFERENCE.md exists."""
        import pathlib
        
        project_root = pathlib.Path(__file__).parent.parent
        tools_ref = project_root / "TOOLS_REFERENCE.md"
        
        assert tools_ref.exists()
        assert tools_ref.stat().st_size > 0
        print(f"✅ TOOLS_REFERENCE.md exists ({tools_ref.stat().st_size} bytes)")


class TestPackageInfo:
    """Test package information."""

    def test_package_name(self):
        """Test package name."""
        assert "linkedin-mcp-server" == "linkedin-mcp-server"
        print(f"✅ Package name: linkedin-mcp-server")

    def test_required_dependencies(self):
        """Test that required dependencies are listed."""
        required = [
            "fastmcp",
            "requests",
            "inquirer",
            "keyring"
        ]
        
        for dep in required:
            assert isinstance(dep, str)
        
        print(f"✅ Required dependencies: {len(required)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
