import { useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  Bot,
  CheckCircle2,
  Cpu,
  Database,
  Download,
  Eye,
  FileText,
  FolderOpen,
  Gauge,
  HardDrive,
  History,
  Laptop,
  Layers3,
  ListChecks,
  LockKeyhole,
  Network,
  Play,
  RefreshCcw,
  ShieldCheck,
  SlidersHorizontal,
  SquareTerminal,
  Table2,
  Workflow,
  Wrench
} from "lucide-react";
import {
  actionRows,
  artifactIcons,
  artifacts,
  auditRows,
  metricCards,
  reportSections,
  runModes,
  skillPacks,
  statusIcon,
  timelineItems,
  workspace
} from "./mockData";
import type { Artifact, SkillPack, TimelineItem } from "./mockData";

const statusLabel = {
  active: "active",
  mock: "mock",
  planned: "planned"
};

function App() {
  const [mode, setMode] = useState(runModes[0].id);
  const [selectedArtifactId, setSelectedArtifactId] = useState(artifacts[0].id);

  const selectedArtifact = useMemo(
    () => artifacts.find((artifact) => artifact.id === selectedArtifactId) ?? artifacts[0],
    [selectedArtifactId]
  );

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Workspace">
        <Brand />
        <WorkspaceCard />
        <SkillRegistry />
        <BridgePanel mode={mode} />
      </aside>

      <main className="workbench">
        <header className="topbar">
          <div className="run-state">
            <span className="state-dot" />
            <span>Local-first mock</span>
          </div>
          <div className="topbar-actions" aria-label="Run controls">
            <button className="icon-button ghost" type="button" aria-label="Refresh mock data">
              <RefreshCcw size={17} />
            </button>
            <button className="icon-button ghost" type="button" aria-label="Tune execution settings">
              <SlidersHorizontal size={17} />
            </button>
            <button className="primary-action" type="button">
              <Play size={17} />
              Run
            </button>
          </div>
        </header>

        <section className="command-panel" aria-labelledby="request-label">
          <div className="command-copy">
            <span className="eyebrow" id="request-label">
              Task request
            </span>
            <h1>{workspace.request}</h1>
          </div>
          <div className="mode-switch" role="tablist" aria-label="Executor mode">
            {runModes.map((runMode) => (
              <button
                className={runMode.id === mode ? "mode-pill active" : "mode-pill"}
                key={runMode.id}
                type="button"
                role="tab"
                aria-selected={runMode.id === mode}
                onClick={() => setMode(runMode.id)}
              >
                <span>{runMode.label}</span>
                <small>{runMode.status}</small>
              </button>
            ))}
          </div>
        </section>

        <section className="metrics-grid" aria-label="Run metrics">
          {metricCards.map(({ label, value, caption, Icon }) => (
            <article className="metric-card" key={label}>
              <Icon size={18} />
              <div>
                <strong>{value}</strong>
                <span>{label}</span>
              </div>
              <small>{caption}</small>
            </article>
          ))}
        </section>

        <section className="run-grid">
          <TimelinePanel />
          <ArtifactPreview artifact={selectedArtifact} />
        </section>
      </main>

      <aside className="artifact-rail" aria-label="Artifacts">
        <ArtifactList selectedArtifactId={selectedArtifactId} onSelect={setSelectedArtifactId} />
        <AuditPanel />
      </aside>
    </div>
  );
}

function Brand() {
  return (
    <div className="brand-block">
      <div className="brand-mark" aria-hidden="true">
        <Laptop size={22} />
      </div>
      <div>
        <p>MTBUDDY</p>
        <span>AIBOOK workstation</span>
      </div>
    </div>
  );
}

function WorkspaceCard() {
  return (
    <section className="panel workspace-card" aria-labelledby="workspace-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Workspace</span>
          <h2 id="workspace-title">{workspace.name}</h2>
        </div>
        <FolderOpen size={18} />
      </div>
      <code>{workspace.path}</code>
      <div className="file-stack">
        {workspace.files.map((file) => (
          <div className="file-row" key={file}>
            <FileText size={15} />
            <span>{file}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function SkillRegistry() {
  return (
    <section className="panel skill-panel" aria-labelledby="skill-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Skill registry</span>
          <h2 id="skill-title">Local tools</h2>
        </div>
        <Wrench size={18} />
      </div>
      <div className="skill-list">
        {skillPacks.map((skill) => (
          <SkillRow key={skill.id} skill={skill} />
        ))}
      </div>
    </section>
  );
}

function SkillRow({ skill }: { skill: SkillPack }) {
  return (
    <div className="skill-row">
      <div className={`skill-status ${skill.status}`} />
      <div>
        <strong>{skill.label}</strong>
        <span>{skill.description}</span>
      </div>
      <small>{statusLabel[skill.status]}</small>
    </div>
  );
}

function BridgePanel({ mode }: { mode: string }) {
  const activeMode = runModes.find((runMode) => runMode.id === mode) ?? runModes[0];

  return (
    <section className="panel bridge-panel" aria-labelledby="bridge-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Agent bridge</span>
          <h2 id="bridge-title">{activeMode.label}</h2>
        </div>
        <Network size={18} />
      </div>
      <div className="bridge-route">
        <span>MTBUDDY Core</span>
        <ArrowRight size={15} />
        <span>{mode === "local" ? "LocalExecutor" : "MTClaw"}</span>
        <ArrowRight size={15} />
        <span>{mode === "openclaw" ? "OpenClaw" : "OpenAI API"}</span>
      </div>
      <div className="trust-strip">
        <span>
          <LockKeyhole size={14} />
          local-first
        </span>
        <span>
          <ShieldCheck size={14} />
          audited
        </span>
      </div>
    </section>
  );
}

function TimelinePanel() {
  return (
    <section className="panel timeline-panel" aria-labelledby="timeline-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Execution</span>
          <h2 id="timeline-title">Run timeline</h2>
        </div>
        <Activity size={18} />
      </div>
      <div className="timeline-list">
        {timelineItems.map((item) => (
          <TimelineRow key={item.id} item={item} />
        ))}
      </div>
    </section>
  );
}

function TimelineRow({ item }: { item: TimelineItem }) {
  const Icon = statusIcon[item.status];

  return (
    <div className={`timeline-row ${item.status}`}>
      <div className="timeline-icon">
        <Icon size={16} />
      </div>
      <div className="timeline-main">
        <strong>{item.label}</strong>
        <span>{item.skill}</span>
      </div>
      <code>{item.evidence}</code>
      <small>{item.duration}</small>
    </div>
  );
}

function ArtifactList({
  selectedArtifactId,
  onSelect
}: {
  selectedArtifactId: string;
  onSelect: (artifactId: string) => void;
}) {
  return (
    <section className="panel artifact-list-panel" aria-labelledby="artifact-list-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Artifacts</span>
          <h2 id="artifact-list-title">Workspace output</h2>
        </div>
        <Database size={18} />
      </div>
      <div className="artifact-list">
        {artifacts.map((artifact) => {
          const Icon = artifactIcons[artifact.kind];
          const isSelected = artifact.id === selectedArtifactId;

          return (
            <button
              className={isSelected ? "artifact-item selected" : "artifact-item"}
              key={artifact.id}
              type="button"
              onClick={() => onSelect(artifact.id)}
            >
              <Icon size={18} />
              <span>
                <strong>{artifact.name}</strong>
                <small>{artifact.path}</small>
              </span>
              <CheckCircle2 size={16} />
            </button>
          );
        })}
      </div>
    </section>
  );
}

function ArtifactPreview({ artifact }: { artifact: Artifact }) {
  const Icon = artifactIcons[artifact.kind];

  return (
    <section className="panel preview-panel" aria-labelledby="preview-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Preview</span>
          <h2 id="preview-title">{artifact.name}</h2>
        </div>
        <div className="preview-actions">
          <button className="icon-button ghost" type="button" aria-label="View artifact">
            <Eye size={16} />
          </button>
          <button className="icon-button ghost" type="button" aria-label="Download artifact">
            <Download size={16} />
          </button>
        </div>
      </div>
      <div className={`artifact-preview ${artifact.kind}`}>
        <div className="preview-title">
          <Icon size={23} />
          <div>
            <strong>{artifact.detail}</strong>
            <span>{artifact.path}</span>
          </div>
        </div>
        {artifact.kind === "markdown" && <ReportPreview />}
        {artifact.kind === "csv" && <CsvPreview />}
        {artifact.kind === "pptx" && <DeckPreview />}
        {artifact.kind === "jsonl" && <JsonlPreview />}
      </div>
    </section>
  );
}

function ReportPreview() {
  return (
    <div className="report-preview">
      {reportSections.map((section, index) => (
        <div className="section-line" key={section}>
          <span>{String(index + 1).padStart(2, "0")}</span>
          <strong>{section}</strong>
        </div>
      ))}
    </div>
  );
}

function CsvPreview() {
  return (
    <div className="csv-preview">
      <div className="csv-header">
        <span>Owner</span>
        <span>Action</span>
        <span>Status</span>
      </div>
      {actionRows.map((row) => (
        <div className="csv-row" key={`${row.owner}-${row.task}`}>
          <span>{row.owner}</span>
          <span>{row.task}</span>
          <strong>{row.state}</strong>
        </div>
      ))}
    </div>
  );
}

function DeckPreview() {
  return (
    <div className="deck-preview">
      <div className="slide-card title-slide">
        <span>01</span>
        <strong>MTBUDDY</strong>
        <small>Local-first personal AI workstation</small>
      </div>
      <div className="slide-grid">
        <div className="slide-card">
          <Layers3 size={17} />
          <strong>Skills</strong>
        </div>
        <div className="slide-card">
          <Workflow size={17} />
          <strong>MTClaw</strong>
        </div>
        <div className="slide-card">
          <Gauge size={17} />
          <strong>Evals</strong>
        </div>
      </div>
    </div>
  );
}

function JsonlPreview() {
  return (
    <div className="jsonl-preview">
      {auditRows.map((row, index) => (
        <code key={row}>
          {`{"seq":${index + 1},"operation":"${row}","status":"ok"}`}
        </code>
      ))}
    </div>
  );
}

function AuditPanel() {
  return (
    <section className="panel audit-panel" aria-labelledby="audit-title">
      <div className="panel-heading">
        <div>
          <span className="eyebrow">Evidence</span>
          <h2 id="audit-title">Run ledger</h2>
        </div>
        <History size={18} />
      </div>
      <div className="ledger-grid">
        <div>
          <SquareTerminal size={17} />
          <span>CLI</span>
          <strong>pytest pass</strong>
        </div>
        <div>
          <Bot size={17} />
          <span>Agent</span>
          <strong>OpenAI-compatible</strong>
        </div>
        <div>
          <Cpu size={17} />
          <span>AIBOOK</span>
          <strong>adapter ready</strong>
        </div>
        <div>
          <HardDrive size={17} />
          <span>Storage</span>
          <strong>workspace local</strong>
        </div>
      </div>
      <div className="audit-command">
        <ListChecks size={16} />
        <code>mtbuddy run --workspace ./workspaces/demo</code>
      </div>
    </section>
  );
}

export default App;
