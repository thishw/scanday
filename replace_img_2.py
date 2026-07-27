import os
filepath = 'blog/why-recommend-bookscan.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('assets/hero_bg.png', 'assets/smart_bookscan_hero.jpg')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated blog post image references")
