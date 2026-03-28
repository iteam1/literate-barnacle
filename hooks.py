"""MkDocs hook: percent-encode non-ASCII characters in llms.txt URLs."""

import re
from pathlib import Path
from urllib.parse import quote, urlparse, urlunparse


def _encode_url(url: str) -> str:
    parsed = urlparse(url)
    encoded_path = quote(parsed.path, safe="/:@!$&'()*+,;=")
    return urlunparse(parsed._replace(path=encoded_path))


def on_post_build(config, **kwargs):
    site_dir = Path(config["site_dir"])
    for name in ("llms.txt", "llms-full.txt"):
        path = site_dir / name
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        encoded = re.sub(
            r"\]\(([^)]+)\)",
            lambda m: "](" + _encode_url(m.group(1)) + ")",
            original,
        )
        if encoded != original:
            path.write_text(encoded, encoding="utf-8-sig")
