# Installation and host verification

Use a disposable project first. No user-level installation or global configuration changes are required for these checks.

```sh
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host codex
node skills/glasspring/scripts/install.mjs --target "PATH_TO_PROJECT" --host claude
```

Replace `PATH_TO_PROJECT` with a path valid for your shell, such as `C:\work\project` in PowerShell or `/home/me/project` on macOS and Linux.

The installer copies only the checked-out `skills/glasspring/` directory to the host's project-level directory. The installed folder carries its scoped third-party notice; repository-level provenance and rights-review documents are not copied. For a repeatable install, record the source commit with `git rev-parse HEAD`; the installer does not pin a revision or track later changes. Use `--dry-run` to preview and `--replace` to update with a retained backup. It rejects symlinks requiring manual review, source-descendant destinations and unexpected arguments. If the target directory is missing, the installer creates it and the required parent directories. It verifies referenced files and copied bytes before promoting the staged copy.

The repository's MIT license does not grant rights to retained third-party material. Its redistribution rights review remains open; read the [third-party notices](THIRD_PARTY_NOTICES.md) before sharing an installed copy.

To restore a replacement, close the host, move the current `glasspring` folder aside, and rename the printed `glasspring.backup-…` sibling to `glasspring`. Retain the current folder until restoration is checked. Backups are local and are not uploaded.

## Remove a project installation

The installer has no uninstall command. Close the host first, then review and preserve any local changes made inside the installed folder. Remove only the matching `glasspring` directory:

- Codex or generic Agent Skills install: `<PROJECT>/.agents/skills/glasspring`
- Claude Code install: `<PROJECT>/.claude/skills/glasspring`

Leave the parent `skills` directory in place because it may contain other skills. A replacement backup is a separate sibling named `glasspring.backup-…`; review and remove it separately only after you no longer need it for restoration.

After installing, start a new host session in the project. Confirm the skill is listed, invoke it by name, and verify that it reads the intended installed file. Then run one small task and retain the output and transcript. Installation alone is not a discovery or triggering test.

| Host / environment | File-copy test | Fresh-session discovery | Task behavior |
|---|---|---|---|
| Codex project, Windows, one isolated fresh session | Passed | `PASS`: skill metadata appeared in the host list | `UNKNOWN`: a local execution policy blocked reading the installed skill file; no task output was produced |
| Claude Code project, Windows | Passed locally and in CI | `NOT_RUN`: no authenticated fresh session | `NOT_RUN` |
| Codex and Claude Code directory layouts, macOS and Linux | Passed in CI on the current published snapshot | `NOT_RUN` | `NOT_RUN` |
| Cursor, ZCode, and other hosts | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

The CI matrix uses Windows, macOS, and Ubuntu runners with Python 3.12 and Node.js 22. The latest completed run for the published snapshot as of 2026-10-25 is [candidate checks](https://github.com/Rethymus/glasspring/actions/runs/40198893762). These checks cover the installer layout and file-copy integrity; they do not start a coding-agent host or verify discovery and model behavior.

During the 2026-10-25 audit, installed CLI versions were inspected only: Codex CLI 0.153.4 and Claude Code 2.1.39. The single Codex fresh-session check established metadata visibility only; it did not run a model task. No Claude Code session was authenticated. Do not convert these limited observations into a general compatibility claim.

Official location references, checked during the audit:

- [Codex local skill locations](https://learn.chatgpt.com/docs/build-skills).
- [Claude Code skill locations](https://code.claude.com/docs/en/skills).
- [Agent Skills format](https://agentskills.io/specification).

Run `doctor.py --selftest` from the installed `scripts` directory to inspect tooling. Do not run a deliverable contract check against an empty project and describe it as installation verification. A meaningful contract check needs a generated run directory with its expected artifacts.

MCP registration is optional and manual. Use an absolute path to `mcp_server.py` and a Python executable available to that host. The audit tested the local stdio handshake through the server selftest; it did not test a production host MCP integration.
