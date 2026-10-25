# Coffee storefront example

This is an illustrative page built from the public coffee-shop pilot brief in [`evals/protocol.json`](../../evals/protocol.json). It is **not** an output from the earlier sample run, a result from an independent evaluation, or proof that a coding-agent host discovered and followed Glasspring.

The storefront, product names, prices, copy, and photography are fictional. The “Add to bag” buttons update local page state only; there is no checkout, payment, or order service. The hero, product, and botanical images were generated for this example with the built-in image generator on 2026-10-25. The desktop, mobile, and open-bag screenshots in `assets/preview-*.png` were captured from the local page in Chrome; they are illustrative page captures, not an earlier sample run or an evaluation result. The page uses no remote fonts, libraries, or image URLs.

To preview it locally from the repository root:

```sh
python -m http.server 8000 --directory examples/coffee-storefront
```

Then open `http://127.0.0.1:8000/` in a browser.
