"""Verify local behavior, deterministic example output, and Markdown file links."""
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    subprocess.run([sys.executable, '-m', 'unittest', '-v', 'test_demo.py'],
                   cwd=ROOT, check=True)
    output = subprocess.check_output([sys.executable, 'demo.py'], cwd=ROOT, text=True)
    expected = json.loads((ROOT / 'examples/demo-output.json').read_text())
    if json.loads(output) != expected:
        raise SystemExit('FAIL: generated demo differs from examples/demo-output.json')
    links = 0
    for document in ROOT.rglob('*.md'):
        if '.git' in document.relative_to(ROOT).parts:
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (document.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                raise SystemExit(f'FAIL: broken or out-of-repo link in {document.relative_to(ROOT)}: {target}')
            links += 1
    print(f'PASS: example output matches; {links} local Markdown file links resolve.')


if __name__ == '__main__':
    main()
