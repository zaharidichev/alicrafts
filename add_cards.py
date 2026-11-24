

#!/usr/bin/env python3
"""Rebuild the gallery in index.html from the files images/card-NN.jpg.

Run it from the site folder:   python3 add_cards.py
It only touches the gallery cards and one line of the language script.
Safe to run again after adding, removing or re-pricing cards.
"""
import glob, re, sys

DEFAULT_PRICE = 4                      # euros, for any card not listed below
PRICES = {                             # card number: price in euros
    1: 5, 2: 5, 8: 5, 20: 5, 21: 5, 70: 5,           # cards with a star
    4: 5, 11: 5, 13: 5, 24: 5, 25: 5, 49: 5, 51: 5,  # cards with a wide ribbon
}
SOLD = set()                           # card numbers to leave out, e.g. {3, 17}

html = open('index.html', encoding='utf-8').read()
start = html.find('<figure')
end = html.rfind('</figure>')
if start < 0 or end < 0:
    sys.exit('Could not find the gallery in index.html - nothing changed.')
end += len('</figure>')
template = html[start:html.find('</figure>', start) + len('</figure>')]

numbers = sorted(int(re.search(r'card-(\d+)\.jpg$', p).group(1)) for p in glob.glob('images/card-*.jpg'))
numbers = [n for n in numbers if n not in SOLD]
if not numbers:
    sys.exit('No images/card-NN.jpg files found - nothing changed.')

def card(n):
    f = template
    f = re.sub(r'images/card-\d+\.jpg', 'images/card-%02d.jpg' % n, f)
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
