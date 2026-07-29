import os
import re
from datetime import datetime
from email.utils import format_datetime

BLOG_DIR = 'blog'
BASE_URL = 'https://scanday.kr'
OUTPUT_FILE = 'rss.xml'

def extract_meta(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1).split('|')[0].strip() if title_match else "No Title"

    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    description = desc_match.group(1) if desc_match else ""

    date_match = re.search(r'"datePublished":\s*"(.*?)"', content)
    pub_date = date_match.group(1) if date_match else ""

    if not pub_date:
        # try to get from html text
        meta_date = re.search(r'작성일:\s*([\d\. ]+)', content)
        if meta_date:
            # Example: 2026. 07. 10 -> 2026-07-10
            date_str = meta_date.group(1).replace(' ', '')
            if date_str.endswith('.'):
                date_str = date_str[:-1]
            date_str = date_str.replace('.', '-')
            pub_date = date_str
        else:
            pub_date = datetime.now().strftime("%Y-%m-%d")

    return {
        'title': title,
        'description': description,
        'pubDate': pub_date
    }

def build_rss():
    items = []
    for filename in os.listdir(BLOG_DIR):
        if filename.endswith('.html') and filename != 'index.html':
            filepath = os.path.join(BLOG_DIR, filename)
            meta = extract_meta(filepath)
            
            # format date to RFC 822 (required for RSS)
            try:
                # Assuming YYYY-MM-DD
                dt = datetime.strptime(meta['pubDate'], "%Y-%m-%d")
            except:
                dt = datetime.now()
            
            rfc_date = format_datetime(dt.astimezone())

            url = f"{BASE_URL}/blog/{filename}"

            item = f"""
    <item>
      <title><![CDATA[{meta['title']}]]></title>
      <link>{url}</link>
      <description><![CDATA[{meta['description']}]]></description>
      <pubDate>{rfc_date}</pubDate>
      <guid>{url}</guid>
    </item>"""
            items.append((dt, item))

    # Sort items by date descending
    items.sort(key=lambda x: x[0], reverse=True)
    item_strings = [x[1] for x in items]

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>스캔데이 인사이트</title>
    <link>{BASE_URL}</link>
    <description>왕십리 셀프 북스캔 스캔데이 공식 블로그입니다.</description>
    <language>ko</language>
    <atom:link href="{BASE_URL}/rss.xml" rel="self" type="application/rss+xml" />
    {''.join(item_strings)}
  </channel>
</rss>"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    print(f"Generated {OUTPUT_FILE} with {len(items)} items.")

if __name__ == '__main__':
    build_rss()
