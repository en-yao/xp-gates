"""Twilio SMS service with validation, status tracking, and CLI support."""
import argparse
import base64
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SMSResult:
    """Result of an SMS send operation."""
    success: bool
    message_sid: Optional[str] = None
    status: Optional[str] = None
    to: Optional[str] = None
    from_number: Optional[str] = None
    body: Optional[str] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        result = {"success": self.success}
        if self.message_sid:
            result["message_sid"] = self.message_sid
        if self.status:
            result["status"] = self.status
        if self.to:
            result["to"] = self.to
        if self.from_number:
            result["from"] = self.from_number
        if self.body:
            result["body"] = self.body
        if self.error_code:
            result["error_code"] = self.error_code
        if self.error_message:
            result["error_message"] = self.error_message
        return result


class TwilioSMSService:
    """Service for sending SMS via Twilio API."""

    MAX_BODY_LENGTH = 1600
    PHONE_PATTERN = re.compile(r"^\+[1-9]\d{1,14}$")
    API_BASE = "https://api.twilio.com/2010-04-01"

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        default_from: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize the Twilio SMS service."""
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.default_from = default_from
        self.timeout = timeout
        self._auth_header = self._create_auth_header()

    def _create_auth_header(self) -> str:
        """Create the Basic Auth header."""
        credentials = f"{self.account_sid}:{self.auth_token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def _validate_phone_number(self, number: str) -> bool:
        """Validate phone number format (E.164)."""
        return bool(self.PHONE_PATTERN.match(number))

    def _validate_body(self, body: str) -> tuple[bool, Optional[str]]:
        """Validate message body."""
        if not body:
            return False, "Message body cannot be empty"
        if len(body) > self.MAX_BODY_LENGTH:
            return False, f"Message body exceeds {self.MAX_BODY_LENGTH} characters"
        return True, None

    def send(
        self,
        to: str,
        body: str,
        from_number: Optional[str] = None
    ) -> SMSResult:
        """
        Send an SMS message.

        Args:
            to: Destination phone number (E.164 format)
            body: Message content
            from_number: Sender phone number (defaults to service default)

        Returns:
            SMSResult with success status and details
        """
        from_number = from_number or self.default_from

        # Validate inputs
        if not from_number:
            return SMSResult(
                success=False,
                error_message="No from_number provided and no default configured"
            )

        if not self._validate_phone_number(to):
            return SMSResult(
                success=False,
                error_message=f"Invalid destination phone number: {to}"
            )

        if not self._validate_phone_number(from_number):
            return SMSResult(
                success=False,
                error_message=f"Invalid source phone number: {from_number}"
            )

        valid_body, body_error = self._validate_body(body)
        if not valid_body:
            return SMSResult(success=False, error_message=body_error)

        # Build request
        url = f"{self.API_BASE}/Accounts/{self.account_sid}/Messages.json"
        data = urllib.parse.urlencode({
            "To": to,
            "From": from_number,
            "Body": body
        }).encode()

        request = urllib.request.Request(url, data=data, method="POST")
        request.add_header("Authorization", self._auth_header)
        request.add_header("Content-Type", "application/x-www-form-urlencoded")

        # Send request
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_data = json.loads(response.read().decode())
                return SMSResult(
                    success=True,
                    message_sid=response_data.get("sid"),
                    status=response_data.get("status"),
                    to=response_data.get("to"),
                    from_number=response_data.get("from"),
                    body=response_data.get("body")
                )
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            try:
                error_data = json.loads(error_body)
                return SMSResult(
                    success=False,
                    error_code=error_data.get("code"),
                    error_message=error_data.get("message", str(e.reason))
                )
            except json.JSONDecodeError:
                return SMSResult(
                    success=False,
                    error_code=e.code,
                    error_message=str(e.reason)
                )
        except urllib.error.URLError as e:
            return SMSResult(
                success=False,
                error_message=f"Network error: {e.reason}"
            )
        except Exception as e:
            return SMSResult(
                success=False,
                error_message=f"Unexpected error: {str(e)}"
            )


def send_sms(
    to: str,
    body: str,
    account_sid: Optional[str] = None,
    auth_token: Optional[str] = None,
    from_number: Optional[str] = None
) -> SMSResult:
    """
    Convenience function to send an SMS.

    Credentials can be provided directly or via environment variables:
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN
    - TWILIO_FROM_NUMBER
    """
    import os

    account_sid = account_sid or os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = auth_token or os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = from_number or os.environ.get("TWILIO_FROM_NUMBER")

    if not account_sid or not auth_token:
        return SMSResult(
            success=False,
            error_message="Missing Twilio credentials"
        )

    service = TwilioSMSService(account_sid, auth_token, from_number)
    return service.send(to, body, from_number)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Send SMS via Twilio")
    parser.add_argument("to", help="Destination phone number (E.164 format)")
    parser.add_argument("body", help="Message body")
    parser.add_argument("--from", dest="from_number", help="Source phone number")
    parser.add_argument("--sid", help="Twilio Account SID")
    parser.add_argument("--token", help="Twilio Auth Token")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    result = send_sms(
        to=args.to,
        body=args.body,
        account_sid=args.sid,
        auth_token=args.token,
        from_number=args.from_number
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        if result.success:
            print(f"✓ Message sent: {result.message_sid}")
            print(f"  Status: {result.status}")
        else:
            print(f"✗ Failed to send message")
            if result.error_code:
                print(f"  Error code: {result.error_code}")
            print(f"  Error: {result.error_message}")

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
