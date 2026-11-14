"""Build/install a wheel into an isolated venv; run from outside the checkout."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import venv

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='sgo-wheel-') as directory:
        base = Path(directory)
        subprocess.run([sys.executable, '-m', 'pip', 'wheel', '--no-deps', '.', '-w', str(base)], cwd=ROOT, check=True)
        wheel, = base.glob('*.whl')
        venv.create(base / 'env', with_pip=True)
        bin_dir = base / 'env' / ('Scripts' if os.name == 'nt' else 'bin')
        python = bin_dir / ('python.exe' if os.name == 'nt' else 'python')
        cli = bin_dir / ('sgo.exe' if os.name == 'nt' else 'sgo')
        subprocess.run([str(python), '-m', 'pip', 'install', str(wheel)], cwd=base, check=True)
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        for args in (['tour','--json'], ['validate'], ['byod',str(ROOT/'examples/user-metrics.json')]):
            result = subprocess.check_output([str(cli),*args], cwd=base, env=env, text=True)
            payload = json.loads(result)
            if args[0] == 'tour':
                assert len(payload) == 8 and all(row['result']['status'] == row['expected_status'] for row in payload)
            elif args[0] == 'validate':
                assert payload['valid']
            else:
                assert payload['total'] == payload['passed'] == 4
        subprocess.run([str(python), '-I', '-m', 'sgo', 'tour'], cwd=base, env=env, check=True, stdout=subprocess.DEVNULL)
        print('PASS: isolated wheel, bundled schema/registry, console and module entry points, BYOD')


if __name__ == '__main__':
    main()
