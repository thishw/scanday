import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.replace(old, new))
        print(f"Updated {filepath}")

replace_in_file('index.html', 'assets/smart_bookscan_hero.jpg', 'assets/smart_bookscan_hero.png')
replace_in_file('blog/index.html', 'assets/smart_bookscan_hero.jpg', 'assets/smart_bookscan_hero.png')
replace_in_file('blog/why-recommend-bookscan.html', 'assets/smart_bookscan_hero.jpg', 'assets/smart_bookscan_hero.png')
