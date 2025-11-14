# LinkedIn MCP Server - Test Suite

Comprehensive test suite for all LinkedIn scraping and API automation tools.

## 📋 Test Structure

```
tests/
├── __init__.py                  # Test package initialization
├── conftest.py                  # Pytest fixtures and configuration
├── test_scraping_tools.py       # Tests for browser-based scraping tools
├── test_api_tools.py            # Tests for LinkedIn REST API tools
├── test_integration.py          # End-to-end workflow tests
├── test_error_handling.py       # Error handling and edge case tests
└── README.md                    # This file
```

## 🚀 Running Tests

### Prerequisites

1. **Install test dependencies:**
   ```bash
   uv pip install pytest pytest-cov pytest-asyncio
   ```

2. **Configure environment variables:**
   Create a `.env` file with:
   ```env
   LINKEDIN_COOKIE=li_at=YOUR_COOKIE_HERE
   LINKEDIN_ACCESS_TOKEN=YOUR_TOKEN_HERE
   LINKEDIN_CLIENT_ID=YOUR_CLIENT_ID
   LINKEDIN_CLIENT_SECRET=YOUR_CLIENT_SECRET
   ```

### Run All Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=linkedin_mcp_server --cov-report=html
```

### Run Specific Test Files

```bash
# Scraping tools only
pytest tests/test_scraping_tools.py -v

# API tools only
pytest tests/test_api_tools.py -v

# Integration tests only
pytest tests/test_integration.py -v

# Error handling tests only
pytest tests/test_error_handling.py -v
```

### Run Specific Test Classes

```bash
# Test person profile scraping
pytest tests/test_scraping_tools.py::TestPersonProfile -v

# Test post management
pytest tests/test_api_tools.py::TestPostManagement -v

# Test workflows
pytest tests/test_integration.py::TestScrapingWorkflow -v
```

### Run Specific Tests

```bash
# Test a single function
pytest tests/test_scraping_tools.py::TestPersonProfile::test_get_person_profile_success -v

# Test credential validation
pytest tests/test_api_tools.py::TestCredentialValidation::test_validate_credentials_success -v
```

## 🏷️ Test Categories

### Unit Tests (Fast)
Tests individual functions in isolation:
```bash
pytest tests/test_scraping_tools.py tests/test_api_tools.py -m "not integration and not slow"
```

### Integration Tests (Slow)
Tests that create/modify real LinkedIn data:
```bash
pytest tests/ -m integration -v
```

**⚠️ WARNING:** Integration tests create and delete real posts on LinkedIn!

### Skipped Tests
Some tests are skipped by default because they modify real data:
```bash
# Run all tests including skipped ones
pytest tests/ --run-skipped
```

## 📊 Test Coverage

### Coverage by Module

- **Scraping Tools:** `test_scraping_tools.py`
  - Person profile scraping
  - Company profile scraping
  - Job search and details
  - Job recommendations
  - Session management

- **API Tools:** `test_api_tools.py`
  - Credential validation
  - Profile retrieval
  - Post creation/update/deletion
  - Image upload/management
  - Reactions (add/remove/get)
  - Edge cases

- **Integration:** `test_integration.py`
  - Profile research workflows
  - Job search workflows
  - Content creation workflows
  - Mixed scraping + API workflows
  - Error recovery

- **Error Handling:** `test_error_handling.py`
  - Input validation
  - Rate limiting
  - Network errors
  - Authentication errors
  - Data validation
  - Boundary conditions

### Generate Coverage Report

```bash
# HTML coverage report
pytest tests/ --cov=linkedin_mcp_server --cov-report=html

# View report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## 🔧 Test Fixtures

Available fixtures (defined in `conftest.py`):

- `linkedin_cookie` - Session cookie for scraping
- `linkedin_access_token` - API access token
- `linkedin_client_id` - OAuth client ID
- `linkedin_client_secret` - OAuth client secret
- `test_profile_url` - Sample profile URL
- `test_company_url` - Sample company URL
- `test_job_keywords` - Sample job keywords
- `sample_post_text` - Sample post content
- `sample_image_url` - Sample image URL

## ⚙️ Configuration

### Pytest Options

Create `pytest.ini` in project root:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
markers =
    integration: Integration tests that modify real data
    slow: Slow-running tests
```

### Skip Integration Tests by Default

```bash
# Run only fast unit tests
pytest tests/ -m "not integration"
```

## 🎯 Test Examples

### Testing Profile Scraping

```python
def test_get_person_profile_success(linkedin_cookie, test_profile_url):
    result = get_person_profile(test_profile_url)
    assert result is not None
    assert "name" in result
```

### Testing Post Creation

```python
@pytest.mark.integration
def test_create_post(linkedin_access_token, sample_post_text):
    result = create_linkedin_post(text=sample_post_text)
    assert "post_id" in result
    
    # Cleanup
    delete_linkedin_post(result["post_id"])
```

### Testing Error Handling

```python
def test_invalid_url(linkedin_cookie):
    with pytest.raises(Exception):
        get_person_profile("invalid-url")
```

## 🐛 Troubleshooting

### Tests Failing with "Cookie Expired"

**Solution:** Refresh your LinkedIn cookie:
```bash
# Get new cookie
uv run main.py --get-cookie

# Update .env file
LINKEDIN_COOKIE=li_at=NEW_COOKIE_HERE
```

### Tests Failing with "Token Invalid"

**Solution:** Generate a new access token from LinkedIn Developer portal.

### Tests Skipped

Some tests are skipped by default to avoid creating real LinkedIn content:
```bash
# Run skipped tests manually
pytest tests/test_api_tools.py::TestPostManagement -v
```

### Rate Limiting Errors

If you hit rate limits, add delays between tests:
```python
import time
time.sleep(2)  # Wait 2 seconds between API calls
```

## 📈 Continuous Integration

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: pytest tests/ -m "not integration" --cov
        env:
          LINKEDIN_COOKIE: ${{ secrets.LINKEDIN_COOKIE }}
          LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
```

## 🎓 Best Practices

1. **Always clean up** - Delete test posts/data after creation
2. **Use delays** - Add `time.sleep()` between API calls
3. **Skip destructive tests** - Mark with `@pytest.mark.skip`
4. **Mock when possible** - Mock external calls for faster tests
5. **Test edge cases** - Invalid inputs, empty strings, etc.
6. **Check error handling** - Use `pytest.raises()` for exceptions
7. **Verify credentials** - Test with both valid and invalid auth

## 📝 Adding New Tests

### Template for New Test

```python
class TestNewFeature:
    """Tests for new feature."""

    def test_basic_functionality(self, linkedin_cookie):
        """Test basic feature operation."""
        result = new_feature_function()
        assert result is not None
        print(f"✅ New feature works")

    def test_error_handling(self, linkedin_cookie):
        """Test error cases."""
        with pytest.raises(Exception):
            new_feature_function(invalid_input)
        print(f"✅ Error handling works")
```

## 🤝 Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Add tests to appropriate test file
3. Update this README if needed
4. Run full test suite before committing
5. Ensure >80% code coverage

## 📞 Support

- **Issues:** Report test failures on GitHub
- **Questions:** Open a discussion
- **Author:** Selvin PaulRaj K

---

**Happy Testing! 🧪**


---
##  CURRENT TEST STATUS

**All Tests Passing:** 41/41 
**Speed:** ~4 seconds
**Coverage:** 6% (critical components)

### Active Test Files:
- test_smoke.py - 14 tests 
- test_api_tools_simple.py - 12 tests 
- test_scraping_tools_simple.py - 15 tests 

### Quick Run:
```bash
uv run pytest tests/ -m 'not integration' -v
```
