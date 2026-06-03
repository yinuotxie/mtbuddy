# MTBUDDY MTClaw Integration

This directory contains Function Router tool definitions and wrappers for
running MTBUDDY workspace operations through MTClaw.

MTBUDDY uses this stack for the competition demo:

```text
MTBUDDY workstation UI or CLI
  -> OpenClaw agent runtime
  -> MTClaw Function Router provider
  -> DeepSeek or AIBOOK local model endpoint
  -> MTBUDDY workspace tools
```

## Install Local Package

From the MTBUDDY repository:

```bash
python3 -m pip install -e .
```

## Register Tools With MTClaw

Copy or merge these files into the Function Router config directory:

```bash
mkdir -p ~/.function-router/scripts
cat integrations/mtclaw/functions.jsonl >> ~/.function-router/functions.jsonl
cp integrations/mtclaw/scripts/*.sh ~/.function-router/scripts/
chmod +x ~/.function-router/scripts/mtbuddy_*.sh
```

If MTBUDDY is installed in a virtualenv, point wrappers at that interpreter:

```bash
export MTBUDDY_PYTHON=/path/to/mtbuddy/.venv/bin/python
```

Restart MTClaw / Function Router after changing tool definitions:

```bash
function-router --config ~/.function-router/config.json
```

## DeepSeek Config Shape

Use DeepSeek as both routing and upstream while we do not have AIBOOK hardware:

```json
{
  "routing": {
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "api_key": "${DEEPSEEK_API_KEY}"
  },
  "upstream": {
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "api_key": "${DEEPSEEK_API_KEY}"
  }
}
```

The model/provider details live in Function Router config, not in these wrapper
scripts. The wrappers only expose deterministic local MTBUDDY tools.
