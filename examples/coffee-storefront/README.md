# Coffee storefront worked example

This is a **manual, Glasspring-guided implementation of the same fictional task brief in the root README**. It follows the new-preview contract: the three core files [`tokens.css`](tokens.css), [`preview.html`](preview.html), and [`design-notes.md`](design-notes.md), plus narrow and desktop PNG captures in [`shots/`](shots/). The skill version, route, decisions, checks, and limits are recorded in the design notes.

This page is not an Agent host session, an independent efficacy result, or a replay of [`evals/protocol.json`](../../evals/protocol.json). That public protocol still lacks referenced inputs, so a benchmark replay is not possible from this repository. The example demonstrates a page and its local behavior; it does not show host discovery or prove that the Skill improves design quality.

The storefront, products, prices, and copy are fictional. The bag changes local page state and subtotal only. No order or payment service exists. Hero, product, and botanical images were generated for this example with the built-in image generator on 2026-10-25. There are no remote fonts, scripts, libraries, or image URLs.

The desktop and mobile full-page captures were made locally on 2026-10-26 at 1440px and 390px. The open-bag capture is a 1440×900 viewport showing two House Blend items and a $36 subtotal. The five-frame interaction GIF was recaptured on the same date at 960×667, showing the initial page, adding one item, opening the bag, increasing the quantity to two, and removing the item. See the design notes for browser details and the limits of the checks.

To preview it from the repository root:

```sh
python -m http.server 8000 --directory examples/coffee-storefront
```

Then open `http://127.0.0.1:8000/preview.html`.
