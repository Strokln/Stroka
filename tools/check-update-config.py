"""Check updater routing and published manifest consistency for this project."""
import json
import re
from pathlib import Path
from urllib.parse import urlparse
root = Path(__file__).resolve().parents[1]
repo = 'Strokln/Stroka'
source = (root / 'app/src/main/java/io/github/jackwener/dsh/core/update/UpdateManifest.kt').read_text()
assert f'private const val REPO = "{repo}"' in source
assert 'jackwener/DSH-Android' not in source
manifest = json.loads((root / 'update/latest.json').read_text())
assert manifest['format'] == 1
assert manifest['packageName'] == 'io.github.jackwener.dsh'
assert manifest['signerSha256'] == 'a36e75295012cd85eac06a1a2fdfc7b224d579f394ffbd91ed8b5973a87bc269'
assert manifest['versionCode'] > 0 and manifest['apk']['size'] > 0
assert re.fullmatch('[0-9a-f]{64}', manifest['apk']['sha256'])
assert manifest['notes'].get('ru') and manifest['notes'].get('en')
for url in manifest['apk']['urls']:
    u = urlparse(url)
    assert u.scheme == 'https' and u.hostname == 'github.com'
    assert u.path.startswith(f'/{repo}/releases/download/v{manifest["versionName"]}/')
print('PASS: update endpoints, repository, signer, manifest and release notes')
