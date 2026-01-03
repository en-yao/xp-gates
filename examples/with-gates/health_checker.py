from urllib.request import urlopen


def check_health(urls: list[str]) -> dict[str, str]:
    """Check if URLs are reachable. Returns {url: 'up'/'down'}."""
    results = {}
    for url in urls:
        try:
            urlopen(url, timeout=5)
            results[url] = "up"
        except Exception:
            results[url] = "down"
    return results
