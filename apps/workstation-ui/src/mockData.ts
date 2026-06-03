export type IconKey =
  | "assistant"
  | "expert"
  | "skills"
  | "connectors"
  | "automation"
  | "more"
  | "docs"
  | "finance"
  | "data"
  | "research"
  | "product"
  | "slides"
  | "design"
  | "email"
  | "craft"
  | "auto"
  | "permission";

export type LabelItem = {
  label: string;
  icon: IconKey;
  meta?: string;
};

export const leftNavItems: LabelItem[] = [
  { label: "助理", meta: "Claw", icon: "assistant" },
  { label: "专家", meta: "领域顾问", icon: "expert" },
  { label: "技能", meta: "能力扩展", icon: "skills" },
  { label: "连接器", meta: "服务接入", icon: "connectors" },
  { label: "自动化", meta: "定时任务", icon: "automation" },
  { label: "更多", meta: "资料库 · 灵感", icon: "more" }
];

export const categoryChips: LabelItem[] = [
  { label: "文档处理", icon: "docs" },
  { label: "金融服务", icon: "finance" },
  { label: "数据分析及可视化", icon: "data" },
  { label: "深度研究", icon: "research" },
  { label: "产品管理", icon: "product" },
  { label: "幻灯片", icon: "slides" },
  { label: "设计", icon: "design" },
  { label: "邮件编写", icon: "email" }
];

export const composerTools: LabelItem[] = [
  { label: "Craft", icon: "craft" },
  { label: "Auto", icon: "auto" },
  { label: "技能", icon: "skills" },
  { label: "连接器", icon: "connectors" },
  { label: "默认权限", icon: "permission" }
];

export const workspaceOptions = ["选择工作空间"];
