"""Validate this static site without installing dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import json
import hashlib
import base64

ROOT = Path(__file__).resolve().parents[1]
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.refs, self.ids = path, [], set()
        self.csp = None
        self.schema = None
        self.schema_text = ""
        self.in_schema = False
        self.meta = {}
        self.canonical = None
        self.referrer = False
        self.resource_seen = False

    def fail(self, message):
        errors.append(f'{self.path.name}: {message}')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta': self.meta[a.get('property', a.get('name', ''))] = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a.get('href')
        if 'id' in a:
            if a['id'] in self.ids: self.fail('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'meta' and a.get('http-equiv', '').lower() == 'content-security-policy':
            if self.resource_seen: self.fail('CSP must precede resources')
            self.csp = a.get('content', '')
        if tag == 'meta' and a.get('name') == 'referrer':
            self.referrer = a.get('content') == 'strict-origin-when-cross-origin'
        if tag in ('link', 'script', 'img'): self.resource_seen = True
        if tag in ('base', 'iframe', 'object', 'embed', 'style'):
            self.fail('unexpected active element: ' + tag)
        if any(k == 'style' or k.startswith('on') for k in a): self.fail('inline style/event handler')
        if tag == 'form' and (a.get('action') != 'https://mail.glixerp.com/api/glix-contact.php' or a.get('method') != 'post'):
            self.fail('unexpected form destination')
        if tag == 'script' and a.get('type') == 'application/ld+json':
            if self.schema is not None or self.schema_text: self.fail('duplicate structured data')
            if a.get('src'): self.fail('structured data must be embedded')
            self.in_schema = True
        elif tag == 'script':
            if not a.get('src') or urlsplit(a['src']).netloc: self.fail('scripts must be local files')
            if 'defer' not in a: self.fail('script must defer execution')
        if tag == 'img':
            if not all(a.get(k, '').isdigit() for k in ('width', 'height')): self.fail('image dimensions missing')
            if 'alt' not in a: self.fail('image alt missing')
        if a.get('target') == '_blank' and not {'noopener','noreferrer'} <= set(a.get('rel','').split()):
            self.fail('unsafe external link')
        if 'srcset' in a:
            self.refs.extend(candidate.strip().split()[0] for candidate in a['srcset'].split(','))
        for key in ('src', 'href'):
            if key not in a: continue
            url = a[key]
            parsed = urlsplit(url)
            if parsed.scheme in ('javascript', 'data', 'http'): self.fail('disallowed URL: ' + url)
            if not parsed.scheme and not parsed.netloc: self.refs.append(url)
            if tag == 'link' and a.get('rel') == 'stylesheet' and parsed.netloc :
                self.fail('unexpected external stylesheet')

    def handle_data(self, data):
        if self.in_schema: self.schema_text += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.in_schema = False
            try: self.schema = json.loads(self.schema_text)
            except ValueError: self.fail('invalid structured data JSON')

pages = {}
for path in ROOT.glob('*.html'):
    page = Page(path)
    page.feed(path.read_text(encoding='utf-8-sig'))
    pages[path.name] = page
    required = ("default-src 'none'", "object-src 'none'", "base-uri 'none'", "form-action 'none'", "connect-src 'self' https://mail.glixerp.com", "frame-src 'none'")
    if not page.csp or any(part not in page.csp.split('; ') for part in required): page.fail('missing restrictive CSP')
    if page.csp and ('unsafe-inline' in page.csp or 'unsafe-eval' in page.csp): page.fail('unsafe CSP exception')
    if not page.referrer: page.fail('missing referrer policy')
    expected_url = 'https://glixerp.com/' + ('' if path.name == 'index.html' else path.name)
    if page.canonical != expected_url or page.meta.get('og:url') != expected_url: page.fail('canonical/OG URL mismatch')
    if page.meta.get('twitter:card') != 'summary_large_image': page.fail('missing large social card')
    social = page.meta.get('og:image', '')
    if not social.startswith('https://glixerp.com/assets/social/') or not (ROOT / urlsplit(social).path.lstrip('/')).is_file(): page.fail('missing public social image')
    if page.meta.get('twitter:image') != social: page.fail('social image mismatch')
    for key in ('description', 'og:title', 'og:description', 'og:image:alt', 'og:image:width', 'og:image:height'):
        if not page.meta.get(key): page.fail('missing metadata: ' + key)
    if not page.schema or page.schema.get('@context') != 'https://schema.org': page.fail('missing structured data')
    else:
        graph = page.schema.get('@graph', [])
        if not {'Organization', 'WebSite', 'WebPage'} <= {node.get('@type') for node in graph}: page.fail('incomplete structured data')
        if not any(node.get('@type') == 'WebPage' and node.get('url') == expected_url for node in graph): page.fail('structured page URL mismatch')
    schema_hash = base64.b64encode(hashlib.sha256(page.schema_text.encode()).digest()).decode()
    if not page.csp or f"script-src 'self' 'sha256-{schema_hash}'" not in page.csp.split('; '): page.fail('structured data must have its exact CSP hash')

for page in pages.values():
    for url in page.refs:
        parsed = urlsplit(url)
        target = ROOT / unquote(parsed.path) if parsed.path else page.path
        if not target.is_file(): page.fail('missing resource: ' + url)
        if parsed.fragment and target.name in pages and unquote(parsed.fragment) not in pages[target.name].ids:
            page.fail('missing anchor: ' + url)
for css in ROOT.rglob('*.css'):
    for ref in re.findall(r'url\([\"\']?([^\)\"\']+)', css.read_text(encoding='utf-8')):
        if not (css.parent / urlsplit(ref).path).is_file(): errors.append(f'{css.name}: missing CSS resource {ref}')
for name in ['script.js','contact.js']:
    script = (ROOT / name).read_text(encoding='utf-8')
    if re.search(r'\beval\s*\(|\.innerHTML\s*=|document\.write\s*\(', script): errors.append(name+': unsafe JavaScript sink')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; CSP, links, anchors, image dimensions, social metadata, structured data, CSS resources and JavaScript sinks.')
