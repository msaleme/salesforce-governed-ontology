"""Verify local behavior, deterministic example output, and Markdown file links."""
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-v'],
                   cwd=ROOT, check=True)
    subprocess.run([sys.executable, 'explore.py', 'validate'], cwd=ROOT, check=True)
    subprocess.run([sys.executable, 'explore.py', 'tour', '--json'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable, 'reliability.py'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    output = subprocess.check_output([sys.executable, 'demo.py'], cwd=ROOT, text=True)
    expected = json.loads((ROOT / 'examples/demo-output.json').read_text())
    if json.loads(output) != expected:
        raise SystemExit('FAIL: generated demo differs from examples/demo-output.json')
    model = json.loads((ROOT / 'ontology.json').read_text())
    graph = 'flowchart LR\n' + '\n'.join(
        f"  {r['source']} -->|{r['predicate']}| {r['target']}" for r in model['relationships'])
    diagram = (ROOT / 'docs/DATA-MODEL.md').read_text()
    if f'```mermaid\n{graph}\n```' not in diagram:
        raise SystemExit('FAIL: ontology diagram differs from registry relationships')
    transcript = subprocess.check_output([sys.executable, 'scripts/reproduce.py', '--demo'], cwd=ROOT, text=True)
    guide = (ROOT / 'docs/RUN-GUIDE.md').read_text()
    captured = guide.split('<!-- BEGIN GENERATED TRANSCRIPT -->\n', 1)[1].split('<!-- END GENERATED TRANSCRIPT -->', 1)[0]
    if transcript != captured:
        raise SystemExit('FAIL: captured demonstration differs from current behavior')
    if (ROOT / 'ontology.json').read_bytes() != (ROOT / 'sgo/ontology.json').read_bytes():
        raise SystemExit('FAIL: packaged ontology differs from root registry')
    links = 0
    for document in ROOT.rglob('*.md'):
        if any(part in {'.git', '.venv', 'build', 'dist'} or part.endswith('.egg-info') for part in document.relative_to(ROOT).parts):
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (document.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                raise SystemExit(f'FAIL: broken or out-of-repo link in {document.relative_to(ROOT)}: {target}')
            links += 1
    print(f'PASS: registry, tour, diagram, and example output match; {links} local Markdown file links resolve.')


if __name__ == '__main__':
    main()
