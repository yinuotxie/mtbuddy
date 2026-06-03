import {
  CheckCircle2,
  Clock3,
  FileText,
  FolderOpen,
  ListChecks,
  Presentation,
  ShieldCheck,
  Table2,
  Wrench
} from "lucide-react";

export type ArtifactKind = "markdown" | "csv" | "pptx" | "jsonl";

export type Artifact = {
  id: string;
  name: string;
  kind: ArtifactKind;
  path: string;
  status: "ready" | "queued" | "draft";
  detail: string;
};

export type TimelineItem = {
  id: string;
  label: string;
  skill: string;
  status: "done" | "running" | "queued";
  duration: string;
  evidence: string;
};

export type SkillPack = {
  id: string;
  label: string;
  description: string;
  permissions: string;
  status: "active" | "mock" | "planned";
};

export const workspace = {
  name: "Demo workspace",
  path: "./workspaces/demo",
  files: [
    "meeting-notes.md",
    "research-notes.txt",
    "metrics.csv",
    "presentation-outline.md"
  ],
  request: "Summarize these files and create an action list"
};

export const runModes = [
  {
    id: "local",
    label: "LocalExecutor",
    status: "deterministic",
    detail: "No model required"
  },
  {
    id: "mtclaw",
    label: "MTClaw",
    status: "provider bridge",
    detail: "OpenAI-compatible"
  },
  {
    id: "openclaw",
    label: "OpenClaw",
    status: "competition path",
    detail: "Flagship agent"
  }
];

export const skillPacks: SkillPack[] = [
  {
    id: "file",
    label: "File",
    description: "List and read allowed workspace files.",
    permissions: "read workspace",
    status: "active"
  },
  {
    id: "doc",
    label: "Doc",
    description: "Create Markdown reports from local sources.",
    permissions: "write artifacts",
    status: "active"
  },
  {
    id: "sheet",
    label: "Sheet",
    description: "Write action lists and tabular evidence.",
    permissions: "write CSV",
    status: "active"
  },
  {
    id: "pptx",
    label: "PPTX",
    description: "Generate slide decks from outlines.",
    permissions: "write PPTX",
    status: "active"
  },
  {
    id: "rag",
    label: "RAG",
    description: "Local retrieval with source citations.",
    permissions: "planned",
    status: "planned"
  }
];

export const timelineItems: TimelineItem[] = [
  {
    id: "plan",
    label: "Plan created",
    skill: "Core",
    status: "done",
    duration: "00:01",
    evidence: "request.accepted"
  },
  {
    id: "list",
    label: "Workspace files scanned",
    skill: "file_skill",
    status: "done",
    duration: "00:02",
    evidence: "file.list"
  },
  {
    id: "read",
    label: "Notes and CSV read",
    skill: "file_skill",
    status: "done",
    duration: "00:04",
    evidence: "file.read"
  },
  {
    id: "report",
    label: "Summary report generated",
    skill: "doc_skill",
    status: "done",
    duration: "00:02",
    evidence: "artifact.write report.md"
  },
  {
    id: "actions",
    label: "Action CSV generated",
    skill: "sheet_skill",
    status: "done",
    duration: "00:02",
    evidence: "artifact.write action-items.csv"
  },
  {
    id: "deck",
    label: "Competition deck staged",
    skill: "pptx_skill",
    status: "done",
    duration: "00:03",
    evidence: "artifact.write competition-demo.pptx"
  },
  {
    id: "audit",
    label: "Audit log sealed",
    skill: "Core",
    status: "done",
    duration: "00:01",
    evidence: "audit.jsonl"
  }
];

export const artifacts: Artifact[] = [
  {
    id: "report",
    name: "report.md",
    kind: "markdown",
    path: "artifacts/report.md",
    status: "ready",
    detail: "Summary, key decisions, risks, and next actions."
  },
  {
    id: "actions",
    name: "action-items.csv",
    kind: "csv",
    path: "artifacts/action-items.csv",
    status: "ready",
    detail: "Owner, task, source, and due signal columns."
  },
  {
    id: "deck",
    name: "competition-demo.pptx",
    kind: "pptx",
    path: "artifacts/competition-demo.pptx",
    status: "ready",
    detail: "MTBUDDY competition story deck."
  },
  {
    id: "audit",
    name: "audit.jsonl",
    kind: "jsonl",
    path: "artifacts/audit.jsonl",
    status: "ready",
    detail: "Append-only operation record."
  }
];

export const reportSections = [
  "Executive Summary",
  "Key Decisions",
  "Action Items",
  "Open Risks",
  "Source Coverage"
];

export const actionRows = [
  {
    owner: "Product",
    task: "Tighten competition demo narrative around MTClaw routing.",
    source: "meeting-notes.md",
    state: "next"
  },
  {
    owner: "Engineering",
    task: "Keep LocalExecutor deterministic while agent path matures.",
    source: "research-notes.txt",
    state: "active"
  },
  {
    owner: "Design",
    task: "Turn artifact and audit evidence into first-screen UI signals.",
    source: "presentation-outline.md",
    state: "active"
  }
];

export const auditRows = [
  "run.start",
  "file.list",
  "file.read",
  "doc.generate",
  "sheet.generate",
  "pptx.generate",
  "run.complete"
];

export const metricCards = [
  {
    label: "Artifacts",
    value: "4",
    caption: "ready",
    Icon: FolderOpen
  },
  {
    label: "Skills",
    value: "5",
    caption: "registered",
    Icon: Wrench
  },
  {
    label: "Audit",
    value: "7",
    caption: "events",
    Icon: ShieldCheck
  },
  {
    label: "Eval",
    value: "pass",
    caption: "CLI slice",
    Icon: CheckCircle2
  }
];

export const artifactIcons = {
  markdown: FileText,
  csv: Table2,
  pptx: Presentation,
  jsonl: ListChecks
};

export const statusIcon = {
  done: CheckCircle2,
  running: Clock3,
  queued: Clock3
};
