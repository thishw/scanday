"""Validate the static site's crawlable pages, internal links and feeds.

Run from any directory: python scripts/audit_site.py
Uses only the Python standard library; does not modify the site.
"""
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://scanday.kr'


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.source = path.read_text(encoding='utf-8')
        self.ids, self.links, self.images, self.canonicals = [], [], [], []
        self.meta = {}
        self.h1 = 0
        self.feed(self.source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property', ''))] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'img':
            self.images.append(attrs)
            for candidate in attrs.get('srcset', '').split(','):
                if candidate.strip():
                    self.links.append(('img', candidate.strip().split()[0]))
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append((tag, attrs[key]))

    @property
    def url(self):
        relative = self.path.relative_to(ROOT).as_posix()
        return BASE + '/' + (relative[:-10] if relative.endswith('index.html') else relative)

    @property
    def indexable(self):
        return 'noindex' not in self.meta.get('robots', '').lower()


def audit():
    paths = sorted([*ROOT.glob('*.html'), *ROOT.joinpath('blog').glob('*.html'), *ROOT.joinpath('services').glob('*.html')])
    pages = {path.resolve(): Page(path) for path in paths}
    errors = []
    for path, page in pages.items():
        label = path.relative_to(ROOT).as_posix()

        def fail(message):
            errors.append(f'{label}: {message}')

        if page.indexable:
            if page.h1 != 1:
                fail(f'expected one h1, found {page.h1}')
            if page.canonicals != [page.url]:
                fail(f'canonical must be {page.url}')
            if not page.meta.get('description'):
                fail('missing description')
        if any(n > 1 for n in Counter(page.ids).values()):
            fail('duplicate element IDs')
        for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page.source, re.S):
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                fail(f'invalid JSON-LD: {exc}')
        for image in page.images:
            if 'alt' not in image:
                fail(f'image lacks alt: {image.get("src")}')
        for tag, link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme and parsed.scheme not in ('http', 'https'):
                continue
            if parsed.netloc and parsed.netloc != 'scanday.kr':
                continue
            if parsed.netloc or parsed.path.startswith('/'):
                target = ROOT / unquote(parsed.path).lstrip('/')
            elif parsed.path:
                target = path.parent / unquote(parsed.path)
            else:
                target = path
            target = target.resolve()
            if target.is_dir():
                target = target / 'index.html'
            if not target.exists():
                fail(f'broken local resource: {link}')
            elif tag == 'a' and parsed.fragment and target in pages:
                if unquote(parsed.fragment) not in pages[target].ids:
                    fail(f'broken anchor: {link}')
        if 'why3445' in page.source or '050-71303-3463' in page.source:
            fail('obsolete contact destination')

    sitemap = ET.parse(ROOT / 'sitemap.xml')
    actual = [element.text for element in sitemap.findall('.//{*}loc')]
    expected = {p.url for p in pages.values() if p.indexable}
    if set(actual) != expected or len(actual) != len(set(actual)):
        errors.append(f'sitemap mismatch: missing={expected-set(actual)}, unexpected={set(actual)-expected}')
    rss = ET.parse(ROOT / 'rss.xml')
    items = rss.findall('./channel/item')
    posts = [p for p in pages.values() if p.path.parent.name == 'blog' and p.path.name != 'index.html']
    if {item.findtext('link') for item in items} != {p.url for p in posts}:
        errors.append('RSS does not match published blog URLs')
    titles = {p.url: re.search(r'<title>(.*?)</title>', p.source, re.S).group(1).split('|')[0].strip() for p in posts}
    for item in items:
        if item.findtext('title') != titles.get(item.findtext('link')):
            errors.append(f'RSS title is stale: {item.findtext("link")}')
    for error in errors:
        print('FAIL', error)
    print(f'{len(pages)} HTML pages; {len(expected)} indexable URLs; {len(posts)} blog posts; {len(errors)} errors.')
    return bool(errors)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(audit())
