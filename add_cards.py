#!/usr/bin/env python3
"""Rebuild the gallery in index.html from the files images/card-NN.jpg.

Run it from the site folder:   python3 add_cards.py
It only touches the gallery cards and one line of the language script.
Safe to run again after adding, removing or re-pricing cards.

It also makes a small, fast-loading copy of every photo in images/thumbs/
for the gallery grid (the full photo is shown when a card is clicked).
That needs Pillow:   python3 -m pip install --user pillow
"""
import glob, os, re, sys

DEFAULT_PRICE = 3                      # euros, for any card not listed below
PRICES = {                             # card number: price in euros
    1: 5, 2: 5, 8: 5, 67: 5, 70: 5,                  # big round ornament in the centre
    20: 4, 21: 4,                                    # cards with a star
    4: 4, 11: 4, 13: 4, 24: 4, 25: 4, 49: 4, 51: 4,  # cards with a wide ribbon
    5: 4, 19: 4, 34: 4, 36: 4, 37: 4, 38: 4, 39: 4,  # big hanging baubles
    41: 4, 43: 4, 45: 4, 53: 4, 57: 4,
    47: 4, 52: 4,                                    # snowmen
    32: 4, 50: 4, 65: 4, 66: 4,                      # fully painted: gifts, tree, angels
}
SOLD = set()                           # card numbers to leave out, e.g. {3, 17}
HIDDEN = {70}                          # cards not ready to show yet (photo stays in images/)
FIRST = [70, 1, 2, 8, 67]              # cards shown at the top of the gallery, in this order
THUMB_WIDTH = 720                      # pixels; about twice the size a card is shown at in the grid
THUMB_QUALITY = 90                     # 0-100

html = open('index.html', encoding='utf-8').read()
start = html.find('<figure')
end = html.rfind('</figure>')
if start < 0 or end < 0:
    sys.exit('Could not find the gallery in index.html - nothing changed.')
end += len('</figure>')
template = html[start:html.find('</figure>', start) + len('</figure>')]

numbers = sorted(int(re.search(r'card-(\d+)\.jpg$', p).group(1)) for p in glob.glob('images/card-*.jpg'))
numbers = [n for n in numbers if n not in SOLD and n not in HIDDEN]
numbers = [n for n in FIRST if n in numbers] + [n for n in numbers if n not in FIRST]
if not numbers:
    sys.exit('No images/card-NN.jpg files found - nothing changed.')

def thumbnails(numbers):
    """Make images/thumbs/card-NN.webp for every card; True if they are all there."""
    try:
        from PIL import Image
    except ImportError:
        print('Note: Pillow is not installed, so the gallery will load the full-size photos (slower).')
        print('      Install it with:  python3 -m pip install --user pillow   and run this again.')
        return False
    os.makedirs('images/thumbs', exist_ok=True)
    made = 0
    for n in numbers:
        src, dst = 'images/card-%02d.jpg' % n, 'images/thumbs/card-%02d.webp' % n
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        im = Image.open(src).convert('RGB')
        if im.width > THUMB_WIDTH:
            im = im.resize((THUMB_WIDTH, round(THUMB_WIDTH * im.height / im.width)), Image.LANCZOS)
        im.save(dst, 'WEBP', quality=THUMB_QUALITY, method=6)
        made += 1
    wanted = {'card-%02d.webp' % n for n in numbers}
    for old in glob.glob('images/thumbs/card-*.webp'):      # sold or removed cards
        if os.path.basename(old) not in wanted:
            os.remove(old)
    if made:
        print('Made %d thumbnail(s) in images/thumbs/' % made)
    return True

THUMBS = thumbnails(numbers)

def card(n):
    f = template
    picture = 'images/thumbs/card-%02d.webp' % n if THUMBS else 'images/card-%02d.jpg' % n
    f = re.sub(r'images/(?:thumbs/)?card-\d+\.(?:jpg|webp)', picture, f)
    f = re.sub(r' data-i18n-alt="[^"]*"', '', f)
    f = re.sub(r' data-card="[^"]*"', '', f)
    f = re.sub(r'alt="[^"]*"', 'alt="Картичка № %d" data-card="%d"' % (n, n), f, count=1)
    f = re.sub(r'№ \d+', '№ %d' % n, f)
    f = re.sub(r'>\s*\d+ €\s*<', '>%d €<' % PRICES.get(n, DEFAULT_PRICE), f)
    return f

html = html[:start] + '\n\n'.join(card(n) for n in numbers) + html[end:]

# make the BG / EN switch translate the photo descriptions too
line = "document.querySelectorAll('img[data-card]').forEach(el => { el.alt = t.card + ' № ' + el.dataset.card; });"
if line not in html:
    anchor = "document.querySelectorAll('.lang').forEach(b => b.setAttribute("
    if anchor in html:
        html = html.replace(anchor, line + '\n  ' + anchor, 1)
    else:
        print('Note: language script not found; photo descriptions will stay in Bulgarian.')

open('index.html', 'w', encoding='utf-8').write(html)
print('Gallery rebuilt with %d cards: %s' % (len(numbers), ', '.join(map(str, numbers))))
