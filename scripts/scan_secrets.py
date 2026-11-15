#!/usr/bin/env python3
"""Scan the files tracked by git for strings that look like credentials.

Exit code 1 when a match is found. Dependency-free by design, so that it runs
in CI without installing anything. To accept a false positive, add the file
path and the line text to `.secret-scan-allow` (one "path::fragment" per line).
"""
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "GitHub token": r"gh[pousr]_[A-Za-z0-9]{30,}",
    "GitHub fine-grained token": r"github_pat_[A-Za-z0-9_]{30,}",
    "Anthropic or OpenAI-style key": r"(?<![A-Za-z0-9_-])sk-(?:ant-)?[A-Za-z0-9_-]{32,}",
    "AWS access key id": r"AKIA[0-9A-Z]{16}",
    "Slack token": r"xox[abprs]-[A-Za-z0-9-]{10,}",
    "Private key block": r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY",
}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".epub", ".docx",
                 ".pptx", ".zip", ".woff", ".woff2", ".ico", ".svg"}


def allowed(root: Path) -> list[tuple[str, str]]:
    f = root / ".secret-scan-allow"
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        if "::" in line and not line.startswith("#"):
            p, frag = line.split("::", 1)
            out.append((p.strip(), frag.strip()))
    return out


def main() -> int:
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    files = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0")
    allow = allowed(root)
    compiled = {k: re.compile(v) for k, v in PATTERNS.items()}
    hits = 0
    for name in filter(None, files):
        path = root / name
        if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for label, rx in compiled.items():
                if rx.search(line) and not any(name == p and frag in line for p, frag in allow):
                    print(f"{name}:{n}: possible {label}")
                    hits += 1
    print(f"secret scan: {hits} possible secret(s) in {len(files)} tracked files")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
