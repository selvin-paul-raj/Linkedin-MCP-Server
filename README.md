# LinkedIn API Integration

A brief description of your project and what it does.

## Installation

Provide instructions on how to install and set up the project.

```bash
# Example installation commands
pip install -r requirements.txt
```

## Usage

Explain how to use the project after installation.

```bash
# Example usage commands
python main.py
```

## Authentication

### 1. 🌐 Chrome DevTools Guide

1.  Open [LinkedIn](https://www.linkedin.com/) and log in.
2.  Open Chrome DevTools (`F12` or right-click → `Inspect`).
3.  Go to `Application` > `Storage` > `Cookies` > `https://www.linkedin.com`.
4.  Find the cookie named `li_at`.
5.  Copy the `Value` field (this is your LinkedIn session cookie).
6.  Use this value as your `LINKEDIN_COOKIE` in the configuration.

### 2. Generate an Access Token

#### Option A: Using LinkedIn's Token Generator (Easiest)

1.  In your app dashboard, look for "OAuth Token Tools" or similar in the `Auth` section.
2.  Select the scopes: `w_member_social`.
3.  Click "Generate token".
4.  Copy the access token (valid for 60 days).

#### Option B: Using Postman

1.  Open Postman and create a new request.
2.  Go to the `Authorization` tab.
3.  Select `Type`: `OAuth 2.0`.
4.  Configure:
    *   **Token Name:** LinkedIn Token
    *   **Grant Type:** Authorization Code
    *   **Callback URL:** `https://oauth.pstmn.io/v1/callback`
    *   **Auth URL:** `https://www.linkedin.com/oauth/v2/authorization`
    *   **Access Token URL:** `https://www.linkedin.com/oauth/v2/accessToken`
    *   **Client ID:** Your LinkedIn app's Client ID
    *   **Client Secret:** Your LinkedIn app's Client Secret
    *   **Scope:** `w_member_social r_liteprofile r_emailaddress`
5.  Click "Get New Access Token".
6.  Authorize the app in the browser window that opens.
7.  Copy the access token from Postman.

#### Option C: Manual OAuth Flow

1.  Direct users to:
    ```
    https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=w_member_social%20r_liteprofile%20r_emailaddress
    ```
2.  After authorization, extract the `code` parameter from the callback URL.
3.  Exchange the code for an access token:
    ```bash
    curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'grant_type=authorization_code' \
      -d 'code=YOUR_AUTH_CODE' \
      -d 'redirect_uri=http://localhost:8080/callback' \
      -d 'client_id=YOUR_CLIENT_ID' \
      -d 'client_secret=YOUR_CLIENT_SECRET'
    ```

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
