# Installation and operational runbook

This is the entry point for operating a local Delegation Core installation.
It provides the supported sequence from installation through validation and
external ingestion. Detailed instructions remain in their canonical documents
to avoid duplication and drift.

Do not place personal paths, tokens, vault content, or customer information in
shared documentation, examples, issue reports, or prompts.

## 1. Install and complete setup

Use the platform installer from the repository root:

```powershell
# Windows
.\install.bat
```

```bash
# Linux or macOS
./install.sh
```

On macOS, `install.command` is the Finder-friendly wrapper for `install.sh`.
The installer creates the local runtime and launches `delegation-core setup`
for a new machine. Do not create the runtime `config.json` before this first
setup; the wizard owns initial configuration.

For prerequisites, installer behavior, manual/development installation, engine
modes, and local index architecture, use the [README](../README.md#install) as
the canonical reference.

## 2. Connect the MCP client

Delegation Core runs as one local HTTP daemon. The default endpoint is
`http://127.0.0.1:8797/mcp`; an existing installation may retain a different
port in its local configuration.

Register each client explicitly:

```bash
delegation-core clients --codex
delegation-core clients --claude-code
```

Use `--claude-desktop` or `--antigravity` when applicable. Use
`delegation-core clients --show` to inspect the local endpoint without changing
client configuration. Open a new client session after registration, a server
restart, or an endpoint change.

Do not add a competing stdio `delegation-core run` entry beside the HTTP daemon.
The [README MCP section](../README.md#using-it-as-an-mcp-server) is the
canonical client-registration reference.

## 3. Validate before use

Run the health checks after installation, update, service restart, or runtime
configuration change:

```bash
delegation-core status
delegation-core doctor
```

If the daemon is not running, use the installed per-user service controls:

```bash
delegation-core service start
delegation-core service restart
```

Then open a new MCP client session, confirm that Delegation Core tools are
listed, and perform a small read-only search for a known note. A valid vault or
client registration alone does not prove that the configured HTTP endpoint is
available.

New installations use SQLite. A healthy legacy installation can remain on
ChromaDB until it is deliberately migrated; see
[indice-sqlite.md](indice-sqlite.md) for the migration and rollback model.

## 4. Configure and validate external ingestion

Configure recurring, shared, or broad external sources only after initial
setup and before their first ingestion. The configuration is an allow-list:
sources, physical paths, recursion, and exclusions must be deliberate.

After a configuration change:

1. Wait for any active ingestion job to finish and back up `config.json`.
2. Edit and validate the strict JSON configuration.
3. Restart the daemon and open a new MCP client session.
4. Run the intended configured ingestion.
5. Search for a known document and confirm excluded content does not appear.

```bash
delegation-core ingest --configured project-reference
delegation-core ingest --configured
```

Use [INGEST_CONFIGURATION.md](INGEST_CONFIGURATION.md) as the canonical guide
for `path` versus `paths`, global and source-specific exclusions, safe edits,
source migration, and ingestion status.

## 5. Update safely

For a Git-based installation, review the update before applying it:

```bash
delegation-core update --check
delegation-core update
delegation-core status
delegation-core doctor
```

Do not bypass a dirty checkout with force options. The update and SQLite
migration procedures, including their rollback boundaries, are documented in
[ATUALIZAR.md](ATUALIZAR.md) and [indice-sqlite.md](indice-sqlite.md).

## Operational acceptance checklist

- [ ] `delegation-core status` completes successfully.
- [ ] `delegation-core doctor` reports no errors.
- [ ] The configured MCP endpoint is listening.
- [ ] A new MCP client session lists Delegation Core tools.
- [ ] A read-only search returns an expected known note.
- [ ] Broad or recurring sources are declared before ingestion.
- [ ] Exclusions are reviewed before the first ingestion.
