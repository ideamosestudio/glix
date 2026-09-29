"""Validate this static site without installing dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.refs, self.ids = path, [], set()
        self.csp = None
        self.referrer = False
        self.resource_seen = False

    def fail(self, message):
        errors.append(f'{self.path.name}: {message}')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: self.fail('duplicate id: ' + a['id'])
            self.ids.add(a['id'])
        if tag == 'meta' and a.get('http-equiv', '').lower() == 'content-security-policy':
            if self.resource_seen: self.fail('CSP must precede resources')
            self.csp = a.get('content', '')
        if tag == 'meta' and a.get('name') == 'referrer':
            self.referrer = a.get('content') == 'strict-origin-when-cross-origin'
        if tag in ('link', 'script', 'img'): self.resource_seen = True
        if tag in ('base', 'iframe', 'object', 'embed', 'form', 'style'):
            self.fail('unexpected active element: ' + tag)
        if any(k == 'style' or k.startswith('on') for k in a): self.fail('inline style/event handler')
        if tag == 'script':
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

pages = {}
for path in ROOT.glob('*.html'):
    page = Page(path)
    page.feed(path.read_text(encoding='utf-8-sig'))
    pages[path.name] = page
    required = ("default-src 'none'", "script-src 'self'", "object-src 'none'", "base-uri 'none'", "form-action 'none'", "connect-src 'self'", "frame-src 'none'")
    if not page.csp or any(part not in page.csp.split('; ') for part in required): page.fail('missing restrictive CSP')
    if page.csp and ('unsafe-inline' in page.csp or 'unsafe-eval' in page.csp): page.fail('unsafe CSP exception')
    if not page.referrer: page.fail('missing referrer policy')

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
script = (ROOT / 'script.js').read_text(encoding='utf-8')
if re.search(r'\beval\s*\(|\.innerHTML\s*=|document\.write\s*\(', script): errors.append('unsafe JavaScript sink')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; CSP, links, anchors, image dimensions, CSS resources and JavaScript sinks.')
