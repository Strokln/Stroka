"""Validate the shipped Russian resource coverage, format arguments and locale registration."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

res = Path(__file__).resolve().parents[1] / 'app/src/main/res'
locales = ET.parse(res / 'xml/locales_config.xml').getroot()
listed = [node.attrib['{http://schemas.android.com/apk/res/android}name'] for node in locales]
shipped = ['zh' if path.name == 'values' else path.name.removeprefix('values-')
           for path in res.glob('values*') if (path / 'strings.xml').exists()]
assert sorted(listed) == sorted(shipped), (listed, shipped)
assert listed[0] == 'zh' and 'ru' in listed
count = 0
for source in (res / 'values-en').glob('strings*.xml'):
    en = {x.attrib['name']: ''.join(x.itertext()) for x in ET.parse(source).getroot()}
    ru = {x.attrib['name']: ''.join(x.itertext()) for x in ET.parse(res / 'values-ru' / source.name).getroot()}
    assert en.keys() == ru.keys(), (source.name, en.keys() ^ ru.keys())
    for name in en:
        placeholders = lambda s: sorted(re.findall(r'%(?:\d+\$)?[dsf]', s))
        assert placeholders(en[name]) == placeholders(ru[name]), name
        assert not re.search('[\u4e00-\u9fff]', ru[name]), name
    count += len(ru)
print(f'PASS: locale registration, {count} translated resource keys and format arguments')
