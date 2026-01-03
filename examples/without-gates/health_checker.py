"""HTTP health checker with concurrent checks, response timing, and CLI support."""
import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class HealthResult:
    """Result of a health check for a single URL."""
    url: str
    status: str  # 'up' or 'down'
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "url": self.url,
            "status": self.status,
        }
        if self.status_code is not None:
            result["status_code"] = self.status_code
        if self.response_time_ms is not None:
            result["response_time_ms"] = round(self.response_time_ms, 2)
        if self.error is not None:
            result["error"] = self.error
        return result


def check_single_url(url: str, timeout: int = 10, headers: Optional[dict] = None) -> HealthResult:
    """Check health of a single URL."""
    headers = headers or {}
    headers.setdefault("User-Agent", "HealthChecker/1.0")

    request = urllib.request.Request(url, headers=headers)
    start_time = time.time()

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            elapsed_ms = (time.time() - start_time) * 1000
            return HealthResult(
                url=url,
                status="up",
                status_code=response.status,
                response_time_ms=elapsed_ms
            )
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return HealthResult(
            url=url,
            status="down",
            status_code=e.code,
            response_time_ms=elapsed_ms,
            error=str(e.reason)
        )
    except urllib.error.URLError as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return HealthResult(
            url=url,
            status="down",
            response_time_ms=elapsed_ms,
            error=str(e.reason)
        )
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return HealthResult(
            url=url,
            status="down",
            response_time_ms=elapsed_ms,
            error=str(e)
        )


def check_health(
    urls: list[str],
    timeout: int = 10,
    max_workers: int = 5,
    headers: Optional[dict] = None
) -> dict:
    """
    Check health of multiple URLs concurrently.

    Returns dict with 'results', 'summary', and 'all_healthy' keys.
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(check_single_url, url, timeout, headers): url
            for url in urls
        }

        for future in as_completed(future_to_url):
            result = future.result()
            results.append(result)

    # Sort by original order
    url_order = {url: i for i, url in enumerate(urls)}
    results.sort(key=lambda r: url_order.get(r.url, 999))

    up_count = sum(1 for r in results if r.status == "up")
    down_count = sum(1 for r in results if r.status == "down")

    return {
        "results": [r.to_dict() for r in results],
        "summary": {
            "total": len(results),
            "up": up_count,
            "down": down_count,
            "healthy_percentage": round(up_count / len(results) * 100, 1) if results else 0
        },
        "all_healthy": down_count == 0
    }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Check health of HTTP endpoints")
    parser.add_argument("urls", nargs="*", help="URLs to check")
    parser.add_argument("-f", "--file", help="File containing URLs (one per line)")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Timeout in seconds")
    parser.add_argument("-w", "--workers", type=int, default=5, help="Max concurrent workers")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    urls = list(args.urls)
    if args.file:
        with open(args.file) as f:
            urls.extend(line.strip() for line in f if line.strip() and not line.startswith("#"))

    if not urls:
        print("No URLs provided", file=sys.stderr)
        sys.exit(1)

    results = check_health(urls, timeout=args.timeout, max_workers=args.workers)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results["results"]:
            status_icon = "✓" if r["status"] == "up" else "✗"
            time_str = f" ({r['response_time_ms']}ms)" if "response_time_ms" in r else ""
            error_str = f" - {r['error']}" if "error" in r else ""
            print(f"{status_icon} {r['url']}: {r['status']}{time_str}{error_str}")

        print()
        summary = results["summary"]
        print(f"Summary: {summary['up']}/{summary['total']} up ({summary['healthy_percentage']}%)")

    sys.exit(0 if results["all_healthy"] else 1)


if __name__ == "__main__":
    main()
