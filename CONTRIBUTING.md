# Contributing

Keep changes focused on a demonstrated user outcome or reproducible tool defect. Preserve the existing design system unless a redesign was requested. Add a discriminating regression case for changes to evidence handling, installation or acceptance behavior.

Run the targeted tests first:

```sh
python -m unittest discover -s tests -v
node skills/glasspring/scripts/install.mjs --selftest
python skills/glasspring/scripts/verify_output.py --selftest
python skills/glasspring/scripts/mcp_server.py --selftest
```

Run browser selftests when changing rendering, accessibility or interaction checks. Preserve complete logs and exit codes. A browser exception, missing CDN response, unavailable dependency or skipped sample cannot be reported as a pass. Report configured CI separately from executed CI.

Do not change a failed fixture solely to match the implementation. Provide the original failure and expected behavior. Exemptions must match the exact known finding; an exemption for one contrast defect must not suppress an unrelated crash or motion failure.

New reference material needs a pinned source, a clear distinction between observation and recommendation, rights evidence for any copied material, and an example showing why it helps. Avoid leaked private prompts and unverified claims about vendor behavior. Keep client work, tokens, internal paths and raw conversations out of commits.
