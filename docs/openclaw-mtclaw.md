# OpenClaw And MTClaw Integration

MTBUDDY uses OpenClaw as the agent runtime and MTClaw Function Router as the
required tool-routing layer for the competition track. The local executor stays
in the repo for deterministic tests and offline development.

## Runtime Shape

```text
MTBUDDY Tauri UI or CLI
  -> MTBUDDY core workspace/artifact/audit layer
  -> OpenClaw agent runtime
  -> MTClaw Function Router provider
  -> DeepSeek API now
  -> AIBOOK local OpenAI-compatible model endpoint later
```

## Local Verification Path

This path does not need OpenClaw, MTClaw, DeepSeek, or AIBOOK hardware:

```bash
python3 -m pip install -e ".[test]"
mtbuddy run --executor local --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
python3 -m pytest
```

## Competition Runtime Path

1. Install MTBUDDY locally.

```bash
python3 -m pip install -e .
```

2. Register MTBUDDY tools with MTClaw Function Router.

```bash
mkdir -p ~/.function-router/scripts
cat integrations/mtclaw/functions.jsonl >> ~/.function-router/functions.jsonl
cp integrations/mtclaw/scripts/*.sh ~/.function-router/scripts/
chmod +x ~/.function-router/scripts/mtbuddy_*.sh
```

3. Configure MTClaw routing and upstream providers to use DeepSeek while AIBOOK
   hardware is unavailable.

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

4. Configure OpenClaw to use the MTClaw Function Router provider and install
   the OpenClaw session bridge plugin recommended by MTClaw.

5. Smoke the agent path.

```bash
mtbuddy run --executor openclaw --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

The OpenClaw executor intentionally fails fast when the `openclaw` CLI is not
installed. Automated tests use `--executor local` so CI remains deterministic.
