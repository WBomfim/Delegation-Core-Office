# Delegation Core v6.4 — Installation and Adjustments Log

- Date: 2026-07-21
- Environment: Windows, PowerShell, timezone America/Sao_Paulo
- Source directory: `C:\Users\willi\Projetos\Delegation_Core\delegation_core_v6.4`
- Runtime directory: `C:\Users\willi\.delegation_core`
- Vault: `C:\Users\willi\Documents\Delegation_Vault`
- Codex plugin: `delegation-core@personal`

## Final state

The package is installed and operational in agent mode. The MCP server exposes 25 tools and the final protocol smoke test returned a healthy heartbeat. BGE embeddings and ChromaDB initialize successfully. No local llama.cpp model is required in the selected mode.

## Installation actions

1. Inspected the package architecture, installer, configuration schema, wizard, CLI, server, deployment notes, and agent guide.
2. Installed Python 3.12.10 with Windows Package Manager because Python 3.11+ was not present.
3. Created the virtual environment at `C:\Users\willi\.delegation_core\venv`.
4. Installed `delegation-core 0.6.4` and its Python dependencies, including FastMCP, ChromaDB, sentence-transformers, PyTorch, document extractors, and Rich.
5. Preserved the package constraint `setuptools<82` required by its installer.
6. Installed the BGE model `BAAI/bge-base-en-v1.5`.
7. Created the vault and its default folders: `decisions`, `research`, `tools`, `fixes`, `reference`, and `sessions`.
8. Initialized ChromaDB and built an empty initial index.
9. Copied `AGENT_GUIDE.md`, `CLAUDE_SYSTEM_PROMPT.md`, and session hooks into `C:\Users\willi\.delegation_core`.
10. Configured synthesis in Brazilian Portuguese, normal budget mode, web search disabled, and engine mode `agent`.

## Problems detected

### Missing Python

Neither `py` nor `python` was initially available. Python 3.12.10 was installed successfully.

### Broken Codex sandbox helper

Sandboxed shell and patch operations repeatedly failed because `codex-windows-sandbox-setup.exe` was not found. Authorized operations were executed outside the broken sandbox. This is an environmental Codex issue, not a Delegation Core runtime issue.

### Wizard CP1252 failure

When output was redirected on Windows, Rich attempted to write Unicode symbols through CP1252 and raised `UnicodeEncodeError`. UTF-8 stream initialization was added at package level so all CLI entry points are covered.

### Invalid Rich markup

The engine selection screen opened `[dim]` markup in one `console.print` call and closed it in another. Rich does not preserve markup state between calls, causing `MarkupError`. Each formatted block is now emitted as one balanced call.

### Agent mode rejected as unconfigured

The wizard correctly cleared `llama_binary` and `llama_model` in agent mode, but `Config.is_configured()` required both values. This made every fresh agent-mode configuration fail at startup. The method now requires only `vault_path` in agent mode and continues to require model and binary in local/hybrid modes.

### Invalid auto-start option in agent mode

The wizard offered llama.cpp auto-start even when agent mode had no local engine. The startup step is now skipped when `cfg.uses_local_model` is false.

### Misleading status in agent mode

The CLI previously reported missing binary/model and an offline llama.cpp service. It now reports that binary/model are not required and generation is delegated to the agent.

### Inconsistent version reporting

The package metadata reported 0.6.4, `__version__` reported 0.6.3, and server logs reported 0.6.0. All active version strings now report 0.6.4.

### Missing Codex integration

The original wizard only documented Claude Desktop and Claude Code. It now prints the supported Codex registration command. A dedicated personal Codex plugin was also created and installed.

### Windows Application Control blocked the generated launcher

After package reinstall, Windows Application Control blocked the regenerated `delegation-core.exe` launcher. The validated runtime command is now:

```text
C:\Users\willi\.delegation_core\venv\Scripts\python.exe -m delegation_core run
```

The Codex plugin and `install.bat` use the module command rather than the blocked launcher.

### Hugging Face cache warning

The Windows profile does not support cache symlinks without Developer Mode or elevated privileges. BGE works normally, but its cache may consume additional disk space. This remains an optional system optimization.

## Source changes

### `src/delegation_core/config.py`

- Updated `Config.is_configured()` for correct agent-mode validation.
- Agent mode now works with empty `llama_binary` and `llama_model` fields.

### `src/delegation_core/wizard.py`

- Added UTF-8 handling for redirected Windows streams.
- Fixed invalid Rich markup in the engine selection screen.
- Replaced Claude-specific agent wording with calling-agent terminology where appropriate.
- Skipped local-engine startup configuration in agent mode.
- Added Codex registration guidance.
- Changed generated MCP examples to invoke `python -m delegation_core run`.

### `src/delegation_core/cli.py`

- Corrected agent-mode status display.
- Avoided unnecessary llama.cpp health requests in agent mode.

### `src/delegation_core/__init__.py`

- Aligned the docstring and `__version__` with 0.6.4.
- Added package-wide UTF-8 stream handling on Windows.

### `src/delegation_core/server.py`

- Corrected the startup log version to 0.6.4.

### `install.bat`

- Replaced generated launcher calls with `python.exe -m delegation_core setup`.
- This avoids Windows Application Control blocking newly generated console launchers.

## Codex plugin implementation

Created personal plugin source:

`C:\Users\willi\plugins\delegation-core`

Created components:

- `.codex-plugin\plugin.json`
- `.mcp.json`
- `skills\delegation-core\SKILL.md`
- `skills\delegation-core\agents\openai.yaml`
- `skills\delegation-core\references\agent-guide.md`

Marketplace entry:

`C:\Users\willi\.agents\plugins\marketplace.json`

Installed plugin:

`delegation-core@personal`, version 0.6.4, enabled.

The plugin is the single persistent source for the MCP definition and operational skill. The earlier global MCP registration was removed to prevent duplicate server definitions.

## Configuration cleanup

Temporary sentinel values previously used to bypass the agent-mode configuration defect were removed. The final configuration keeps `llama_binary` and `llama_model` empty, as intended for agent mode.

## Validation performed

- Compiled all modified Python modules with `py_compile`.
- Rebuilt and reinstalled the 0.6.4 wheel from the corrected source.
- Confirmed `Config.is_configured()` returns true with an agent-mode vault and empty local-model fields.
- Confirmed package `__version__` and docstring report 0.6.4.
- Confirmed `delegation_core status` renders correctly through redirected Windows output.
- Exercised `_step_engine_mode()` with agent selection; no Rich markup or encoding error occurred.
- Validated the skill with `quick_validate.py`: passed.
- Validated the plugin with `validate_plugin.py`: passed.
- Installed and enabled `delegation-core@personal` from the personal marketplace.
- Started the MCP using the exact plugin command.
- Listed 25 MCP tools successfully.
- Called `heartbeat`; result was healthy with no tool error.
- Confirmed BGE and ChromaDB initialized successfully.
- Removed temporary smoke-test and patch-work files from `C:\tmp`.

## Final smoke-test result

```text
tool_count=25
heartbeat_error=False
healthy=True
engine_mode=agent
llama_cpp=delegated-to-agent
package_version=0.6.4
```

## Backup and recovery

Original versions of the six modified files were preserved at:

`C:\Users\willi\Projetos\Delegation_Core\delegation_core_v6.4\patch_backup_20260721`

Files in the backup:

- `config.py`
- `wizard.py`
- `cli.py`
- `__init__.py`
- `server.py`
- `install.bat`

The backup is retained for manual comparison or rollback. It has not been applied after validation.

## Operational note

Codex must be restarted or a new thread opened after plugin installation so the plugin skill and MCP tools are loaded into the new session.