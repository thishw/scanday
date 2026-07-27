import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.replace(old, new))
        print(f"Updated {filepath}")
    else:
        print(f"'{old}' not found in {filepath}")

replace_in_file('index.html', 'assets/hero_bg.png" alt="북스캔과 태블릿"', 'assets/smart_bookscan_hero.jpg" alt="북스캔과 태블릿"')
replace_in_file('blog/index.html', '../assets/hero_bg.png" alt="북스캔과 태블릿"', '../assets/smart_bookscan_hero.jpg" alt="북스캔과 태블릿"')

# For the actual blog post, the main image is on line 89 or so. Let's just replace all instances of hero_bg.png for now, except wait! The blog post MIGHT use hero_bg.png for the header. Let's check.
