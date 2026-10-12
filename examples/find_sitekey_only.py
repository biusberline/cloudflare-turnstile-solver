"""Example: discover the Turnstile sitekey on a page without creating a token.

Only the page markup is read - no solve request is made and no API key is
needed. Handy for checking which sitekey (and action) a form is using.

Usage:
    python examples/find_sitekey_only.py https://example.com/login
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudflare_turnstile_solver import (  # noqa: E402
    TurnstileTokenError,
    find_action,
    find_sitekey,
    read_page,
)

DEFAULT_URL = "https://example.com/"


def main(url):
    html = read_page(url)
    try:
        sitekey = find_sitekey(url, html=html)
    except TurnstileTokenError:
        print(f"{url} -> no Turnstile widget found")
        return
    action = find_action(html)
    suffix = f" (action={action})" if action else ""
    print(f"{url} -> {sitekey}{suffix}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL)
