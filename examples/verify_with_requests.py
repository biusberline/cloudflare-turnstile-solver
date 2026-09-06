"""Example: create a token and verify it against a form endpoint before submitting."""

import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudflare_turnstile_solver import token_for_page  # noqa: E402

API_KEY = os.environ.get("PEAK_API_KEY", "pk_your_api_key")
TARGET = "https://example.com/submit"


def main():
    result = token_for_page(API_KEY, TARGET)

    # Verify the token is accepted before posting real payload data.
    resp = requests.post(
        TARGET,
        data={"cf-turnstile-response": result.token},
        timeout=30,
    )
    if resp.status_code == 403:
        # Token rejected: re-check the page URL, proxy, and user agent -
        # tokens are bound to the environment that created them.
        print("token rejected - check proxy/UA match with the creating call")
        sys.exit(1)

    print("token accepted, status:", resp.status_code)


if __name__ == "__main__":
    main()
