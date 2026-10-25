# Installation and host verification

Use a disposable project first. No user-level installation or global configuration changes are required for these checks.

```sh
node skills/glasspring/scripts/install.mjs --target /absolute/path/to/project --host codex
node skills/glasspring/scripts/install.mjs --target /absolute/path/to/project --host claude
```

The installer copies the same source to the host's project-level directory. Use `--dry-run` to preview and `--replace` to update with a retained backup. It rejects symlinks requiring manual review, source-descendant destinations, missing targets and unexpected arguments. It verifies referenced files and copied bytes before promoting the staged copy.

To restore a replacement, close the host, move the current `glasspring` folder aside, and rename the printed `glasspring.backup-…` sibling to `glasspring`. Retain the current folder until restoration is checked. Backups are local and are not uploaded.

After installing, start a new host session in the project. Confirm the skill is listed, invoke it by name, and verify that it reads the intended installed file. Then run one small task and retain the output and transcript. Installation alone is not a discovery or triggering test.

| Host / environment | File-copy test | Fresh-session discovery | Task behavior |
|---|---|---|---|
| Codex directory layout, Windows | Passed in disposable directories | Not run | Not run |
| Claude Code directory layout, Windows | Passed in disposable directories | Not run | Not run |
| Codex / Claude Code, macOS and Linux | CI configured; not executed here | Not run | Not run |
| Cursor, ZCode and other hosts | Not run | Not run | Not run |

Installed CLI versions were inspected only: Codex CLI 0.153.4 and Claude Code 2.1.39. No new host model calls were made. Do not convert their presence into a compatibility claim.

Official location references, checked during the audit:

- [Codex local skill locations](https://learn.chatgpt.com/docs/build-skills).
- [Claude Code skill locations](https://code.claude.com/docs/en/skills).
- [Agent Skills format](https://agentskills.io/specification).

Run `doctor.py --selftest` from the installed `scripts` directory to inspect tooling. Do not run a deliverable contract check against an empty project and describe it as installation verification. A meaningful contract check needs a generated run directory with its expected artifacts.

MCP registration is optional and manual. Use an absolute path to `mcp_server.py` and a Python executable available to that host. The audit tested the local stdio handshake through the server selftest; it did not test a production host MCP integration.
