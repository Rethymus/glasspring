# Installation and host verification

Use a disposable project first. No user-level installation or global configuration changes are required for these checks.

```sh
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host claude
```

Replace `PATH_TO_PROJECT` with a path valid for your shell, such as `C:\work\project` in PowerShell or `/home/me/project` on macOS and Linux.

The installer copies the same source to the host's project-level directory. Use `--dry-run` to preview and `--replace` to update with a retained backup. It rejects symlinks requiring manual review, source-descendant destinations and unexpected arguments. If the target directory is missing, the installer creates it and the required parent directories. It verifies referenced files and copied bytes before promoting the staged copy.

To restore a replacement, close the host, move the current `glasspring` folder aside, and rename the printed `glasspring.backup-…` sibling to `glasspring`. Retain the current folder until restoration is checked. Backups are local and are not uploaded.

After installing, start a new host session in the project. Confirm the skill is listed, invoke it by name, and verify that it reads the intended installed file. Then run one small task and retain the output and transcript. Installation alone is not a discovery or triggering test.

| Host / environment | File-copy test | Fresh-session discovery | Task behavior |
|---|---|---|---|
| Codex and Claude Code directory layouts, Windows | Passed locally and in CI | Not run | Not run |
| Codex and Claude Code directory layouts, macOS and Linux | Passed in CI on the current published snapshot | Not run | Not run |
| Cursor, ZCode, and other hosts | Not run | Not run | Not run |

The CI matrix uses Windows, macOS, and Ubuntu runners with Python 3.12 and Node.js 22. The latest completed run for the published snapshot is [candidate checks](https://github.com/Rethymus/glasspring/actions/runs/40159018216). These checks cover the installer layout and file-copy integrity; they do not start a coding-agent host or verify discovery and model behavior.

Installed CLI versions were inspected only: Codex CLI 0.153.4 and Claude Code 2.1.39. No new host model calls were made. Do not convert their presence into a compatibility claim.

Official location references, checked during the audit:

- [Codex local skill locations](https://learn.chatgpt.com/docs/build-skills).
- [Claude Code skill locations](https://code.claude.com/docs/en/skills).
- [Agent Skills format](https://agentskills.io/specification).

Run `doctor.py --selftest` from the installed `scripts` directory to inspect tooling. Do not run a deliverable contract check against an empty project and describe it as installation verification. A meaningful contract check needs a generated run directory with its expected artifacts.

MCP registration is optional and manual. Use an absolute path to `mcp_server.py` and a Python executable available to that host. The audit tested the local stdio handshake through the server selftest; it did not test a production host MCP integration.
