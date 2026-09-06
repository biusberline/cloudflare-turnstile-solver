<a href="https://peak.fo/?utm_source=github&utm_medium=readme&utm_campaign=packages&utm_content=cloudflare-turnstile-solver">
  <img src="./assets/peak-banner.png" alt="Peak - solve Cloudflare Turnstile & the 5s challenge in ~1s" width="100%">
</a>

# Cloudflare Turnstile Solver — Get a Turnstile Token in Python

The **Cloudflare Turnstile Solver** package makes it easy to work with
Cloudflare Turnstile from Python: it **finds the Turnstile sitekey** on any page,
**creates a valid Turnstile token** via the Peak API, and hands you a
`cf-turnstile-response` token you can inject into a form or request. It is a
small, dependency-free library plus a CLI — designed for CI pipelines, QA
automation, and integration engineering.

**Table of Contents:**
- What this package does
- Quick start
- Finding a Turnstile sitekey
- Creating a Turnstile token
- Python API reference
- CLI usage
- Examples
- Powered by Peak
- License
## What this package does

Cloudflare Turnstile protects pages with a widget that issues a token. Two things
are always needed: **find the sitekey** the page is using, and **create a token**
for that sitekey. This package provides both:

1. `find_sitekey()` — scan a page for its `data-sitekey`.
2. `create_token()` — submit a solve task to the Peak API and get a valid token.
3. `token_for_page()` — do both in one call.

It has no browser dependency. A single Python file, standard library only, works
on headless servers and CI runners.

## Quick start

```console
$ export PEAK_API_KEY=pk_your_api_key
$ python -m cloudflare_turnstile_solver --url https://example.com/
0.AgAAABBqzz...
```

Or find the sitekey first, then create the token:

```python
from cloudflare_turnstile_solver import find_sitekey, create_token

sitekey = find_sitekey("https://example.com/")
token = create_token("pk_...", sitekey, "https://example.com/")
print(token)  # -> "0.AgAAABBqzz..."
```

## Finding a Turnstile sitekey

Turnstile widgets expose the sitekey in the markup:

```html
<div class="cf-turnstile" data-sitekey="0x4AAAAAAAxxxx"></div>
```

`find_sitekey()` reads it for you:

```python
from cloudflare_turnstile_solver import find_sitekey

sitekey = find_sitekey("https://example.com/")
print(sitekey)  # -> "0x4AAAAAAAxxxx"
```

It also finds `data-action` when present, so tokens are scoped correctly.

## Creating a Turnstile token

A token is tied to the sitekey, the page URL, and optionally the action. To
create one with the Peak API:

```python
from cloudflare_turnstile_solver import create_token

result = create_token("pk_...", "0x4AAAAAAAxxxx", "https://example.com/",
                      proxy="http://u:p@1.2.3.4:8080")
print(result.token)
```

Submit the returned token as `cf-turnstile-response`:

```
cf-turnstile-response: 0.AgAAABBqzz...
```

> ⚠️ **If the token is rejected**, check the basics. The token is bound to the
> page URL and environment that created it. Use the same proxy and a matching
> user agent for the request.

## Python API reference

| Function | Description |
|----------|-------------|
| `find_sitekey(url, html=None)` | Scan a page for its Turnstile sitekey. |
| `find_action(html)` | Find an optional `data-action` value. |
| `create_token(api_key, sitekey, url, proxy=None, action=None, cdata=None, ...)` | Create a valid token via the Peak API. |
| `token_for_page(api_key, url, proxy=None, html=None)` | Find the sitekey and create a token in one call. |

All functions raise `TurnstileTokenError` on failure. `create_token` retries
transient failures automatically.

## CLI usage

```console
$ python -m cloudflare_turnstile_solver --url https://example.com/ --output json
{
  "sitekey": "0x4AAAAAAAxxxx",
  "token": "0.AgAAABBqzz...",
  "success": true
}
```

Flags: `--url` (required), `--sitekey`, `--proxy`, `--api-key`, `--output
{text,json}`, `--retries`.

## Examples

### In a script with requests

```python
import requests
from cloudflare_turnstile_solver import token_for_page

result = token_for_page("pk_...", "https://example.com/")
resp = requests.post("https://example.com/submit",
                     data={"cf-turnstile-response": result.token})
print(resp.status_code)
```

### In CI / shell

```bash
TOKEN=$(python -m cloudflare_turnstile_solver --url https://example.com/)
curl -X POST https://example.com/submit \
  -H "cf-turnstile-response: $TOKEN" \
  -d "payload=..."
```

## Powered by Peak

This package uses [Peak](https://peak.fo/?utm_source=github&utm_medium=readme&utm_campaign=packages&utm_content=cloudflare-turnstile-solver) to solve Turnstile.

- ✅ **1,000 free solves to start - no card.** [Grab 1,000 free solves](https://peak.fo/?utm_source=github&utm_medium=readme&utm_campaign=packages&utm_content=cloudflare-turnstile-solver) and pay only for successful solves.
- From **$0.8 / 1,000** successful solves.
- Solve Cloudflare Turnstile & the 5s challenge in about a second.

[Get your free API key](https://peak.fo/?utm_source=github&utm_medium=readme&utm_campaign=packages&utm_content=cloudflare-turnstile-solver) • [Docs](https://peak.fo/docs/turnstile?utm_source=github&utm_medium=readme&utm_campaign=packages&utm_content=cloudflare-turnstile-solver) • [Pricing](https://peak.fo/pricing?utm_source=github&utm_medium=readme&utm_campaign=packages&utm_content=cloudflare-turnstile-solver)

## FAQ

**Does it run headless / without a browser?**

Yes. The whole package is a single Python file on the standard library - no
browser, no webdriver, no Node. It runs the same on a headless CI runner as it
does locally.

**How do I use a proxy?**

Pass it to `create_token` / `token_for_page` with the `proxy` argument, or use
`--proxy` on the CLI:

```console
$ python -m cloudflare_turnstile_solver --url https://example.com/ --proxy http://u:p@1.2.3.4:8080
```

**Can I use it for multiple pages on the same site?**

Yes - call `token_for_page` per page URL. Each token is bound to the page URL
it was created for, so don't reuse one token across different pages.

## License

MIT