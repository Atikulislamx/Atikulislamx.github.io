"""Static GitHub Pages smoke check; standard library only. Run: python3 scripts/check-site.py."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / 'index.html', *sorted(ROOT.glob('*/index.html')),
         *sorted(ROOT.glob('*/*/index.html'))]
errors = []

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.ids = []
        self.in_main = False
        self.h1_count = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append((tag, a))
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'main': self.in_main = True
        if tag == 'h1' and self.in_main: self.h1_count += 1
    def handle_endtag(self, tag):
        if tag == 'main': self.in_main = False

def check_page(page, indexable=True):
    source = page.read_text()
    scan = Scan(); scan.feed(source)
    expected = 'https://atikulislam.me/' + ('' if page == ROOT / 'index.html' else page.parent.relative_to(ROOT).as_posix() + '/')
    if scan.h1_count != 1: errors.append(f'{page}: expected one main h1, got {scan.h1_count}')
    for ident, count in Counter(scan.ids).items():
        if count > 1: errors.append(f'{page}: duplicate id {ident}')
    links = {(a.get('rel'), a.get('href')) for tag, a in scan.tags if tag == 'link'}
    meta = {(a.get('name') or a.get('property')): a.get('content') for tag, a in scan.tags if tag == 'meta'}
    if indexable:
        if ('canonical', expected) not in links: errors.append(f'{page}: canonical must be {expected}')
        for key in ('description', 'og:title', 'og:description', 'og:image', 'og:url',
                    'twitter:title', 'twitter:description', 'twitter:image'):
            if not meta.get(key): errors.append(f'{page}: missing {key}')
        if meta.get('og:url') != expected: errors.append(f'{page}: incorrect og:url')
        for key in ('og:image', 'twitter:image'):
            if not (meta.get(key) or '').startswith('https://atikulislam.me/'):
                errors.append(f'{page}: invalid {key}')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
            try:
                json.loads(block)
                if 'REPLACE-WITH' in block: errors.append(f'{page}: placeholder schema domain')
            except ValueError as exc: errors.append(f'{page}: malformed JSON-LD: {exc}')
    for tag, attrs in scan.tags:
        for key in ('href', 'src', 'poster'):
            value = attrs.get(key, '')
            if value.startswith('https://atikulislam.me/'):
                value = value.removeprefix('https://atikulislam.me')
            if value.startswith('/') and not value.startswith('//'):
                path = Path(unquote(urlsplit(value).path).lstrip('/'))
                if not path.suffix: path /= 'index.html'
                if not (ROOT / path).is_file(): errors.append(f'{page}: missing {key}={value}')
        if tag == 'img' and 'alt' not in attrs: errors.append(f'{page}: image missing alt')
        if tag == 'a' and attrs.get('target') == '_blank':
            if not {'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()):
                errors.append(f'{page}: unsafe target=_blank')
    if not any('data-mobile-nav' in a for _, a in scan.tags): errors.append(f'{page}: mobile nav missing')

for page in PAGES: check_page(page)
check_page(ROOT / '404.html', indexable=False)
urls = {el.text for el in ET.parse(ROOT / 'sitemap.xml').iter() if el.tag.endswith('loc')}
expected_urls = {'https://atikulislam.me/' + ('' if p == ROOT / 'index.html' else p.parent.relative_to(ROOT).as_posix() + '/') for p in PAGES}
if urls != expected_urls: errors.append(f'sitemap mismatch: missing={expected_urls-urls}, extra={urls-expected_urls}')
manifest = json.loads((ROOT / 'site.webmanifest').read_text())
for icon in manifest['icons']:
    if not (ROOT / icon['src'].lstrip('/')).is_file(): errors.append('manifest icon missing: ' + icon['src'])
for css in (ROOT / 'css').rglob('*.css'):
    for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)', css.read_text()):
        if url.startswith('/') and not (ROOT / url.lstrip('/')).is_file():
            errors.append(f'{css}: missing CSS asset {url}')
print(f'Checked {len(PAGES)} indexable pages, 404, links/assets, metadata, JSON-LD, sitemap, manifest and CSS URLs.')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('Static checks passed.')
