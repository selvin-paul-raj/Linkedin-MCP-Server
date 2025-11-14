# src/linkedin_mcp_server/tools/__init__.py
"""
LinkedIn tools package.

This package contains the MCP tool implementations for LinkedIn operations including
both web scraping and API-based functionality.

Available Tools:
- Person tools: LinkedIn profile scraping and analysis
- Company tools: Company profile and information extraction
- Job tools: Job posting details and search functionality
- Post tools: LinkedIn post creation via API (optional, requires access token)

Architecture:
- FastMCP integration for MCP-compliant tool registration
- Shared error handling through centralized error_handler module
- Singleton driver pattern for session persistence (scraping tools)
- LinkedIn API client for post creation (API tools)
- Structured data return format for consistent MCP responses
"""
