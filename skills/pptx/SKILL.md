---
name: mtbuddy-pptx
description: "Use when a MTBUDDY task needs to create, inspect, or reason over PowerPoint .pptx artifacts through MTClaw-callable tools."
---

# MTBUDDY PPTX Skill

This skill pack exposes concrete PPTX tools while keeping final task planning up
to the agent and user.

## Tools

| Tool | Use |
|------|-----|
| `mtbuddy_pptx_create_from_outline` | Create a `.pptx` artifact from a Markdown or text outline. |
| `mtbuddy_pptx_read_text` | Extract slide text from an existing `.pptx` artifact for content QA or summarization. |

## Creation Guidance

Use `mtbuddy_pptx_create_from_outline` when the user asks for a deck,
presentation, or slides and already has an outline/report/notes file. The tool
expects:

```json
{
  "workspace": "./workspaces/demo",
  "outline_path": "presentation-outline.md",
  "output_name": "presentation.pptx"
}
```

The outline format is intentionally simple:

```markdown
# Deck title

## Slide title
- Bullet
- Bullet
```

## QA Guidance

After creating a deck, call `mtbuddy_pptx_read_text` on the generated artifact
to verify that expected titles and bullets are present. Visual render QA should
be added as a separate future tool when LibreOffice/Poppler are available in
the target runtime.

## Boundaries

- Do not overwrite source files.
- Write generated decks under the workspace `artifacts/` directory.
- Treat template editing, visual rendering, and screenshot QA as follow-up tools,
  not as hidden behavior inside deck creation.
