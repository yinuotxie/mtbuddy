# OpenAI-Compatible Agents And MTClaw Integration

MTBUDDY exposes its local tools through MTClaw Function Router so any
OpenAI-compatible agent/client can call them. OpenClaw is the flagship
competition demo client because it has agents, sessions, plugins, and a
MTClaw session bridge, but MTBUDDY is not locked to OpenClaw.

The local executor stays in the repo for deterministic tests and offline
development.

## Runtime Shape

```text
MTBUDDY Tauri UI or CLI
  -> MTBUDDY core workspace/artifact/audit layer
  -> OpenAI-compatible agent client
       -> OpenClawAgentClient
       -> FunctionRouterAgentClient
       -> Hermes / OpenCode / Codex-like clients through MTClaw
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

4. Configure an OpenAI-compatible agent/client to use the MTClaw Function Router
   provider.

   OpenClaw is the richest demo path. Configure OpenClaw to use the MTClaw
   provider and install the OpenClaw session bridge plugin recommended by MTClaw.
   Other clients can point their OpenAI-compatible base URL at Function Router:

```text
base_url = http://127.0.0.1:18790/v1
model = function_router/function-router
```

5. Smoke the agent path.

```bash
mtbuddy run --executor openclaw --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

Or call MTClaw directly through the generic OpenAI-compatible client:

```bash
export MTBUDDY_FUNCTION_ROUTER_BASE_URL=http://127.0.0.1:18790/v1
export MTBUDDY_FUNCTION_ROUTER_MODEL=function_router/function-router
mtbuddy run --executor function-router --workspace ./workspaces/demo \
  "Summarize these files and create an action list"
```

The OpenClaw client intentionally fails fast when the `openclaw` CLI is not
installed. The Function Router client intentionally fails fast when
`MTBUDDY_FUNCTION_ROUTER_BASE_URL` is missing. Automated tests use
`--executor local` so CI remains deterministic.
