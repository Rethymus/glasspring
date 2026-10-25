# Security and privacy

Private vulnerability reporting is enabled for this repository. Use [GitHub's private vulnerability reporting form](https://github.com/Rethymus/glasspring/security/advisories/new) to report security issues. Do not post exploit details, secrets, application data or private screenshots in public issues.

The tools run with the host user's filesystem and process permissions. The prompt's scope rule is guidance, not a filesystem sandbox. MCP path arguments are not restricted to a configured workspace. Use trusted projects and review paths before granting host access.

Browser probes launch a temporary Chromium profile, navigate to the supplied URL and execute page code. They also retrieve axe-core from a public CDN. Remote resources in previews may make network requests. No telemetry uploader was found in the reviewed first-party scripts, but this is not a guarantee about pages, dependencies or the host model provider.

Do not put secrets, application data or private screenshots in a release archive. The original private baseline is a recovery artifact and must not be uploaded with the candidate. The audit's pattern scan found no matches for its limited credential patterns; it was not a complete secret scanner, screenshot OCR audit or proof that the original workspace is safe to publish.
