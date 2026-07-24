import os
tag = '  <meta name="naver-site-verification" content="434c06e5dd45b952ba3fe3e7b7217db9660a5e69" />\n</head>'
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.agents' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'naver-site-verification' not in content:
                    content = content.replace('</head>', tag)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Added to {path}")
            except Exception as e:
                print(f"Error processing {path}: {e}")
