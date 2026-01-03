import base64
import urllib.parse
import urllib.request
import urllib.error
from urllib.request import urlopen


def send_sms(to: str, body: str, account_sid: str, auth_token: str, from_number: str) -> dict:
    """Send SMS via Twilio. Returns {'success': True/False, 'error': ...}."""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    credentials = base64.b64encode(f"{account_sid}:{auth_token}".encode()).decode()
    data = urllib.parse.urlencode({"To": to, "From": from_number, "Body": body}).encode()

    request = urllib.request.Request(url, data=data, method="POST")
    request.add_header("Authorization", f"Basic {credentials}")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urlopen(request, timeout=30) as response:
            return {"success": True}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": str(e.reason)}
    except Exception as e:
        return {"success": False, "error": str(e)}
