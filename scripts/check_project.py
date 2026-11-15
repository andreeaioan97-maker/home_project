"""Pre-publish checks for home_project (public repo)."""
import subprocess, sys, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
errors = []
# stored reversed so this file does not itself contain the strings it guards against
PATTERN = '|'.join(w[::-1] for w in ['or.erailibomi', '046139572', 'aibarasaB'])
files = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
for f in files:  # private material must never be published
    if f == 'apartment/listing.md' or f.startswith('apartment/photos/'):
        errors.append(f'private file would be published: {f}')
for f in files:
    p = ROOT / f
    if p.suffix in {'.html', '.md', '.json', '.py'} and p.exists():
        t = p.read_text(errors='ignore')
        if re.search(PATTERN, t) and f != 'scripts/check_project.py':
            errors.append(f'listing/location detail found in {f}')
for page in ['apartment/floor-plan.html', 'apartment/apartment-3d.html']:
    t = (ROOT / page).read_text()
    if '<title>' not in t or '</html>' not in t:
        errors.append(f'{page} looks incomplete')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('ok: no private files or listing details; pages complete')
