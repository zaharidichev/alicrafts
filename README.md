# ali-crafts.eu

Static site for Alexandra's handmade Christmas cards. No build step: GitHub Pages serves the files as they are.

## Files

- `index.html` – the whole page: layout, styles, and all text in Bulgarian and English.
- `images/card-01.jpg` … `card-08.jpg` – gallery photos (1000×1400).
- `images/thumbs/card-NN.webp` – small copies of the gallery photos for the grid, made by `python3 add_cards.py` (needs Pillow: `python3 -m pip install --user pillow`). The full photo opens when a card is clicked.
- `images/hero-02.jpg`, `hero-05.jpg`, `hero-07.jpg` – the three cards at the top of the page.
- `.nojekyll` – tells GitHub Pages to serve the files untouched.

## Publish on GitHub Pages

1. Push this folder to the `main` branch of a repository.
2. In the repository: Settings → Pages → Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The site appears at `https://<user>.github.io/<repo>/` after a minute or two.

## Custom domain (ali-crafts.eu)

1. Settings → Pages → Custom domain: enter `ali-crafts.eu` and save. GitHub adds a `CNAME` file to the repo.
2. At the domain registrar, add the DNS records GitHub lists on that page (A records for the bare domain, a CNAME for `www`).
3. Once the domain check passes, tick "Enforce HTTPS".

## Common edits

- **Text:** edit the `TEXTS` block at the bottom of `index.html`. Each line exists twice, under `bg` and `en`.
- **Price:** search for the card number in `index.html`; the price is on the line just below it.
- **Sold card:** delete its `<figure>…</figure>` block in the gallery.
- **New card:** add `images/card-09.jpg`, copy one `<figure>` block, and change the file name, the number, the price and the `alt` keys (add matching `alt9` lines to both languages in `TEXTS`).
- **Phone number:** search for `359876711066`; it appears in the Viber link, the call link and as visible text.
