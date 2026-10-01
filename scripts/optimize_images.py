"""Generate smaller web assets from the original PNGs (requires Pillow).

Run manually after adding images; originals stay available for future exports.
Generated files are committed, so deployment does not need Pillow.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def optimize():
    original_bytes = optimized_bytes = 0
    for source in sorted((ROOT / 'assets').glob('*.png')):
        if source.name.startswith('favicon'):
            continue
        with Image.open(source) as original:
            image = ImageOps.exif_transpose(original).convert('RGB' if 'A' not in original.getbands() else 'RGBA')
            for width, suffix in [(min(image.width, 1440), ''), (min(image.width, 480), '-480')]:
                target = image.copy()
                target.thumbnail((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
                output = source.with_name(source.stem + suffix + '.webp')
                target.save(output, 'WEBP', quality=86, method=6)
                if not suffix:
                    original_bytes += source.stat().st_size
                    optimized_bytes += output.stat().st_size
        print(f'{source.name}: {source.stat().st_size:,} -> {source.with_suffix(".webp").stat().st_size:,} bytes')
    with Image.open(ROOT / 'assets/favicon.png') as original:
        icon = original.convert('RGBA')
        icon.thumbnail((64, 64), Image.Resampling.LANCZOS)
        icon.save(ROOT / 'assets/favicon-64.png', optimize=True)
    print(f'Total main variants: {original_bytes:,} -> {optimized_bytes:,} bytes ({(1-optimized_bytes/original_bytes)*100:.1f}% smaller)')


if __name__ == '__main__':
    optimize()
