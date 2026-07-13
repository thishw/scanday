import os
import subprocess
from datetime import datetime

BASE_URL = "https://scanday.kr"
DIRECTORIES = [".", "blog", "services"]
EXCLUDE_DIRS = ["private", ".github", ".git", ".agents", "scripts", "assets", "contents", "style", "marketing_strategy"]

def get_git_lastmod(filepath):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        date_str = result.stdout.strip()
        if date_str:
            return date_str
    except Exception:
        pass
    # Fallback to current time if not in git or error
    return datetime.now().astimezone().replace(microsecond=0).isoformat()

def generate_sitemap():
    sitemap_entries = []
    
    for directory in DIRECTORIES:
        if directory == ".":
            path_dir = "."
        else:
            path_dir = directory
            
        for root, dirs, files in os.walk(path_dir):
            # Skip excluded dirs
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
            
            # If we are in root, only process root files (os.walk will traverse deeper, but we only want to process explicitly allowed subdirs)
            if directory == "." and root != ".":
                continue
                
            for file in files:
                if not file.endswith(".html"):
                    continue
                    
                # Full relative path
                rel_path = os.path.relpath(os.path.join(root, file), ".")
                # Clean up path for URL
                url_path = rel_path.replace("\\", "/")
                
                # Special cases for index.html
                if url_path == "index.html":
                    url_path = ""
                elif url_path.endswith("/index.html"):
                    url_path = url_path.replace("index.html", "")
                
                full_url = f"{BASE_URL}/{url_path}"
                lastmod = get_git_lastmod(rel_path)
                
                sitemap_entries.append({
                    "loc": full_url,
                    "lastmod": lastmod
                })

    # Generate XML
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for entry in sitemap_entries:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{entry["loc"]}</loc>')
        xml_content.append(f'    <lastmod>{entry["lastmod"]}</lastmod>')
        xml_content.append('  </url>')
        
    xml_content.append('</urlset>')
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_content))
    
    print("sitemap.xml generated successfully.")

if __name__ == "__main__":
    generate_sitemap()
