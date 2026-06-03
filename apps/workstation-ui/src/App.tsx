import {
  BarChart3,
  BookOpen,
  Bot,
  BriefcaseBusiness,
  ChevronDown,
  ChevronRight,
  CircleEllipsis,
  Code2,
  Cpu,
  Folder,
  Filter,
  GraduationCap,
  Grid2X2,
  LayoutPanelLeft,
  Link2,
  Mail,
  Mic,
  MoreHorizontal,
  Palette,
  PanelLeft,
  Plus,
  Rocket,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  TimerReset
} from "lucide-react";
import {
  categoryChips,
  composerTools,
  leftNavItems,
  workspaceOptions
} from "./mockData";

const iconMap = {
  assistant: Bot,
  expert: GraduationCap,
  skills: BookOpen,
  connectors: Link2,
  automation: TimerReset,
  more: CircleEllipsis,
  docs: BookOpen,
  finance: BarChart3,
  data: Grid2X2,
  research: Search,
  product: Folder,
  slides: BriefcaseBusiness,
  design: Palette,
  email: Mail,
  craft: Sparkles,
  auto: Grid2X2,
  permission: ShieldCheck
};

function App() {
  return (
    <div className="app-shell">
      <Sidebar />
      <main className="home-screen">
        <header className="floating-header">
          <button className="plain-icon" type="button" aria-label="Toggle sidebar">
            <PanelLeft size={20} />
          </button>
          <button className="demo-pill" type="button">
            <Rocket size={18} />
            来完成比赛演示
            <ChevronRight size={18} />
          </button>
        </header>

        <section className="hero" aria-labelledby="hero-title">
          <AssistantGlyph />
          <h1 id="hero-title">MTBUDDY，我帮你</h1>
          <div className="work-mode" role="tablist" aria-label="工作模式">
            <button type="button" role="tab" aria-selected="false">
              <Code2 size={18} />
              代码开发
            </button>
            <button className="active" type="button" role="tab" aria-selected="true">
              <BriefcaseBusiness size={18} />
              日常办公
            </button>
          </div>
        </section>

        <section className="composer-zone" aria-label="任务输入">
          <div className="quick-chips" aria-label="常用任务">
            {categoryChips.map((chip) => {
              const Icon = iconMap[chip.icon];
              return (
                <button key={chip.label} className="quick-chip" type="button">
                  <Icon size={18} />
                  {chip.label}
                </button>
              );
            })}
            <button className="quick-chip icon-only" type="button" aria-label="更多任务类型">
              <ChevronRight size={18} />
            </button>
          </div>

          <div className="composer-card">
            <textarea placeholder="今天帮你做些什么？" aria-label="任务内容" />
            <div className="composer-footer">
              <div className="tool-row" aria-label="任务选项">
                {composerTools.map((tool) => {
                  const Icon = iconMap[tool.icon];
                  return (
                    <button key={tool.label} type="button">
                      <Icon size={18} />
                      {tool.label}
                      <ChevronDown size={16} />
                    </button>
                  );
                })}
              </div>
              <div className="send-row">
                <button className="round-button" type="button" aria-label="添加附件">
                  <Plus size={22} />
                </button>
                <button className="round-button" type="button" aria-label="语音输入">
                  <Mic size={21} />
                </button>
                <button className="send-button" type="button" aria-label="发送任务">
                  <Send size={22} />
                </button>
              </div>
            </div>
          </div>

          <button className="workspace-picker" type="button">
            <Folder size={20} />
            {workspaceOptions[0]}
            <ChevronDown size={17} />
          </button>
        </section>
      </main>
    </div>
  );
}

function Sidebar() {
  return (
    <aside className="sidebar" aria-label="MTBUDDY navigation">
      <div className="sidebar-topbar">
        <button className="sidebar-icon" type="button" aria-label="Collapse">
          <LayoutPanelLeft size={20} />
        </button>
        <button className="sidebar-icon" type="button" aria-label="Search">
          <Search size={21} />
        </button>
        <button className="sidebar-icon" type="button" aria-label="Filter">
          <Filter size={20} />
        </button>
      </div>

      <div className="brand-line">
        <strong>MTBUDDY</strong>
        <span>v0.1.0</span>
      </div>

      <nav className="nav-list" aria-label="Primary">
        <button className="new-task" type="button">
          <Plus size={18} />
          新建任务
        </button>
        {leftNavItems.map((item) => {
          const Icon = iconMap[item.icon];
          return (
            <button className="nav-item" key={item.label} type="button">
              <span>
                <Icon size={21} />
                {item.label}
              </span>
              <small>{item.meta}</small>
            </button>
          );
        })}
      </nav>

      <div className="empty-tasks">
        <strong>暂无任务</strong>
      </div>

      <div className="account-row">
        <div className="avatar" aria-hidden="true">
          <Cpu size={22} />
        </div>
        <strong>Aetronus</strong>
        <button className="sidebar-icon" type="button" aria-label="Account options">
          <MoreHorizontal size={19} />
        </button>
      </div>
    </aside>
  );
}

function AssistantGlyph() {
  return (
    <svg
      className="assistant-glyph"
      viewBox="0 0 210 176"
      role="img"
      aria-label="MTBUDDY assistant"
    >
      <defs>
        <pattern id="mesh" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="currentColor" strokeWidth="0.6" />
        </pattern>
      </defs>
      <g fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round">
        <path d="M63 42c3-19 14-31 29-34 3 17 1 31-6 42" />
        <path d="M147 42c-3-19-14-31-29-34-3 17-1 31 6 42" />
        <rect x="48" y="35" width="114" height="84" rx="42" fill="url(#mesh)" strokeWidth="2" />
        <rect x="35" y="55" width="26" height="48" rx="13" fill="url(#mesh)" strokeWidth="2" />
        <rect x="149" y="55" width="26" height="48" rx="13" fill="url(#mesh)" strokeWidth="2" />
        <path d="M86 68v26" strokeWidth="4" />
        <path d="M124 68v26" strokeWidth="4" />
        <path d="M76 119c-10 8-18 18-22 32" />
        <path d="M134 119c10 8 18 18 22 32" />
        <circle cx="72" cy="150" r="22" fill="url(#mesh)" strokeWidth="2" />
        <circle cx="138" cy="150" r="22" fill="url(#mesh)" strokeWidth="2" />
        <path d="M94 127h22" />
        <path d="M176 119c12 4 19 12 22 25" />
        <path d="M187 149l15 12" />
      </g>
    </svg>
  );
}

export default App;
