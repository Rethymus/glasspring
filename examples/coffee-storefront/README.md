# Coffee storefront example

This is a standalone illustrative page inspired by the planned coffee-shop task in [`evals/protocol.json`](../../evals/protocol.json). That task refers to a supplied cream-and-terracotta palette, but no palette file is included in the public repository. This page uses its own illustrative styling and cannot be reproduced from the task inputs. It is **not** an output from a Glasspring agent run or an evaluation result, and it does not show that a coding-agent host discovered or followed Glasspring.

The storefront, product names, prices, copy, and photography are fictional. The “Add to bag” buttons update local page state only; there is no checkout, payment, or order service. The hero, product, and botanical images were generated for this example with the built-in image generator on 2026-10-25. The desktop, mobile, and open-bag screenshots in `assets/preview-*.png` were captured from the local page in Chrome; they are illustrative page captures, not an earlier sample run or an evaluation result. The page uses no remote fonts, libraries, or image URLs.

To preview it locally from the repository root:

```sh
python -m http.server 8000 --directory examples/coffee-storefront
```

Then open `http://127.0.0.1:8000/` in a browser.
