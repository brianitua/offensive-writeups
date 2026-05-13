## Hammer Room - Rate Limit Bypass
This script automates the password recovery brute-force for the Hammer room.

### Features
*   **Session Rotation:** Automatically rotates the `PHPSESSID` every 6 attempts to bypass the security dashboard's rate limiting.
*   **Error Handling:** Retries session generation if the server hangs or resets.
*   **Response Analysis:** Uses response length validation (`len(r.text.split())`) to detect the successful recovery code.
