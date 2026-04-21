const path = require("path");
const PptxGenJS = require("pptxgenjs");

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "AgenticOps";
pptx.company = "AgenticOps";
pptx.subject = "运维开发工作中AI工作流改造";
pptx.title = "运维开发工作中AI工作流改造";
pptx.lang = "zh-CN";

const C = {
  dark: "1E2761",
  mid: "2F3C7E",
  light: "CADCFC",
  white: "FFFFFF",
  text: "1F2937",
  muted: "5B6478",
  card: "F5F7FF",
  accent: "00A896",
  warn: "F96167",
  gold: "F9E795",
};

const FONT_HEAD = "Microsoft YaHei UI";
const FONT_BODY = "Microsoft YaHei";

function darkSlide(slide) {
  slide.background = { color: C.dark };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.33,
    h: 1.0,
    fill: { color: C.mid, transparency: 40 },
    line: { color: C.mid, transparency: 100 },
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 11.95,
    y: 0.32,
    w: 0.75,
    h: 0.45,
    radius: 0.08,
    fill: { color: C.accent, transparency: 20 },
    line: { color: C.accent, transparency: 100 },
  });
  slide.addText("AI", {
    x: 12.16,
    y: 0.44,
    w: 0.34,
    h: 0.2,
    fontFace: FONT_HEAD,
    fontSize: 11,
    bold: true,
    color: C.white,
    align: "center",
    margin: 0,
  });
}

function lightSlide(slide) {
  slide.background = { color: C.white };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.33,
    h: 7.5,
    fill: { color: "F6F8FF" },
    line: { color: "F6F8FF" },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.33,
    h: 0.14,
    fill: { color: C.light },
    line: { color: C.light },
  });
}

function title(slide, text, dark = false, subtitle = "") {
  slide.addText(text, {
    x: 0.65,
    y: 0.45,
    w: 9.6,
    h: 0.9,
    fontFace: FONT_HEAD,
    bold: true,
    fontSize: 34,
    color: dark ? C.white : C.dark,
    margin: 0,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.67,
      y: 1.25,
      w: 10.8,
      h: 0.5,
      fontFace: FONT_BODY,
      italic: true,
      fontSize: 15,
      color: dark ? "EAF0FF" : C.muted,
      margin: 0,
    });
  }
}

// Slide 1 Cover
{
  const slide = pptx.addSlide();
  darkSlide(slide);
  title(slide, "运维开发工作中AI工作流改造", true, "从人工救火走向智能闭环，提升稳定性与交付效率");

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.65,
    y: 2.0,
    w: 7.1,
    h: 3.6,
    radius: 0.1,
    fill: { color: C.mid, transparency: 15 },
    line: { color: C.light, transparency: 75, pt: 1 },
  });

  const coverPoints = [
    "告警处理：从分钟级定位走向秒级推荐",
    "发布变更：从人工 checklist 走向策略自动执行",
    "故障复盘：从经验驱动走向知识持续积累",
  ];

  coverPoints.forEach((p, i) => {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: 1.0,
      y: 2.45 + i * 0.9,
      w: 0.28,
      h: 0.28,
      fill: { color: C.accent },
      line: { color: C.accent },
    });
    slide.addText(p, {
      x: 1.4,
      y: 2.38 + i * 0.9,
      w: 5.9,
      h: 0.45,
      fontFace: FONT_BODY,
      fontSize: 17,
      color: C.white,
      margin: 0,
    });
  });

  const stats = [
    ["MTTR", "-35%"],
    ["发布失败率", "-28%"],
    ["值班告警噪声", "-45%"],
  ];
  stats.forEach((s, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 8.25,
      y: 2.0 + i * 1.2,
      w: 4.35,
      h: 0.95,
      radius: 0.08,
      fill: { color: C.white, transparency: 8 },
      line: { color: C.white, transparency: 100 },
    });
    slide.addText(s[0], {
      x: 8.55,
      y: 2.25 + i * 1.2,
      w: 1.8,
      h: 0.35,
      fontFace: FONT_BODY,
      fontSize: 14,
      color: C.dark,
      bold: true,
      margin: 0,
    });
    slide.addText(s[1], {
      x: 10.3,
      y: 2.14 + i * 1.2,
      w: 2.0,
      h: 0.4,
      fontFace: FONT_HEAD,
      fontSize: 28,
      color: C.warn,
      bold: true,
      align: "right",
      margin: 0,
    });
  });

  slide.addText("汇报对象：运维平台 / SRE / DevOps 团队", {
    x: 0.67,
    y: 6.75,
    w: 6.5,
    h: 0.35,
    fontFace: FONT_BODY,
    fontSize: 12,
    color: C.light,
    margin: 0,
  });
}

// Slide 2 Why change
{
  const slide = pptx.addSlide();
  lightSlide(slide);
  title(slide, "为什么要改造：现有工作流的三类瓶颈", false, "告警、变更、复盘链路中仍有大量手工判断与重复动作");

  const cards = [
    ["告警风暴", "同类事件重复触发，值班人员在噪声中定位根因"],
    ["变更不稳", "上线前检查依赖个人经验，回滚策略执行不一致"],
    ["知识断层", "故障复盘沉淀在文档，难以复用到下一次处置"],
  ];

  cards.forEach((c, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 0.75,
      y: 2.0 + i * 1.45,
      w: 6.95,
      h: 1.15,
      radius: 0.08,
      fill: { color: C.card },
      line: { color: C.light, pt: 1 },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: 1.0,
      y: 2.35 + i * 1.45,
      w: 0.3,
      h: 0.3,
      fill: { color: C.warn },
      line: { color: C.warn },
    });
    slide.addText(c[0], {
      x: 1.45,
      y: 2.2 + i * 1.45,
      w: 1.9,
      h: 0.35,
      fontFace: FONT_HEAD,
      bold: true,
      fontSize: 19,
      color: C.dark,
      margin: 0,
    });
    slide.addText(c[1], {
      x: 3.25,
      y: 2.22 + i * 1.45,
      w: 4.2,
      h: 0.6,
      fontFace: FONT_BODY,
      fontSize: 14,
      color: C.text,
      margin: 0,
    });
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 8.15,
    y: 2.0,
    w: 4.4,
    h: 4.55,
    radius: 0.08,
    fill: { color: C.white },
    line: { color: C.light, pt: 1 },
  });
  slide.addText("当前工作时间分布", {
    x: 8.45,
    y: 2.3,
    w: 3.8,
    h: 0.4,
    fontFace: FONT_BODY,
    bold: true,
    fontSize: 15,
    color: C.dark,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.donut, {
    x: 8.85,
    y: 2.95,
    w: 2.2,
    h: 2.2,
    fill: { color: C.light },
    line: { color: C.light },
  });
  slide.addShape(pptx.ShapeType.arc, {
    x: 8.85,
    y: 2.95,
    w: 2.2,
    h: 2.2,
    line: { color: C.warn, pt: 8, transparency: 0, beginArrowType: "none", endArrowType: "none" },
  });
  slide.addText("68%", {
    x: 9.35,
    y: 3.72,
    w: 1.2,
    h: 0.45,
    fontFace: FONT_HEAD,
    fontSize: 28,
    bold: true,
    color: C.warn,
    align: "center",
    margin: 0,
  });
  slide.addText("用于人工排查与重复操作", {
    x: 8.55,
    y: 5.45,
    w: 3.6,
    h: 0.35,
    fontFace: FONT_BODY,
    fontSize: 12,
    color: C.muted,
    align: "center",
    margin: 0,
  });
}

// Slide 3 Target workflow
{
  const slide = pptx.addSlide();
  darkSlide(slide);
  title(slide, "目标状态：AI驱动的运维工作流闭环", true, "感知 -> 理解 -> 决策 -> 执行 -> 复盘 五段式协同");

  const stages = ["事件感知", "语义归因", "策略决策", "自动执行", "知识回写"];
  stages.forEach((name, i) => {
    const x = 0.78 + i * 2.48;
    slide.addShape(pptx.ShapeType.chevron, {
      x,
      y: 2.3,
      w: 2.28,
      h: 1.55,
      fill: { color: i % 2 === 0 ? C.white : C.light, transparency: i === 4 ? 0 : 6 },
      line: { color: C.white, transparency: 80 },
    });
    slide.addText(`${i + 1}`, {
      x: x + 0.18,
      y: 2.52,
      w: 0.35,
      h: 0.3,
      fontFace: FONT_HEAD,
      bold: true,
      fontSize: 14,
      color: C.dark,
      margin: 0,
    });
    slide.addText(name, {
      x: x + 0.55,
      y: 2.48,
      w: 1.5,
      h: 0.5,
      fontFace: FONT_BODY,
      bold: true,
      fontSize: 16,
      color: C.dark,
      margin: 0,
    });
  });

  const labels = [
    ["输入", "监控告警、日志、CMDB、工单"],
    ["输出", "推荐动作、自动脚本、风险评分、复盘知识"],
  ];
  labels.forEach((r, idx) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 0.9,
      y: 4.5 + idx * 1.0,
      w: 11.55,
      h: 0.78,
      radius: 0.06,
      fill: { color: C.mid, transparency: 28 },
      line: { color: C.light, transparency: 70 },
    });
    slide.addText(r[0], {
      x: 1.15,
      y: 4.73 + idx * 1.0,
      w: 1.1,
      h: 0.3,
      fontFace: FONT_HEAD,
      fontSize: 15,
      bold: true,
      color: C.accent,
      margin: 0,
    });
    slide.addText(r[1], {
      x: 2.2,
      y: 4.72 + idx * 1.0,
      w: 9.8,
      h: 0.35,
      fontFace: FONT_BODY,
      fontSize: 14,
      color: C.white,
      margin: 0,
    });
  });
}

// Slide 4 Alert scenario
{
  const slide = pptx.addSlide();
  lightSlide(slide);
  title(slide, "场景一：告警处置工作流改造", false, "将“人找信息”转为“信息找人并给出下一步动作”");

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.72,
    y: 1.95,
    w: 5.95,
    h: 4.95,
    radius: 0.08,
    fill: { color: C.white },
    line: { color: C.light, pt: 1 },
  });
  slide.addText("改造前（人工）", {
    x: 1.02,
    y: 2.2,
    w: 2.2,
    h: 0.35,
    fontFace: FONT_HEAD,
    fontSize: 17,
    bold: true,
    color: C.warn,
    margin: 0,
  });
  const before = ["接收告警并手动查日志", "手工关联最近发布变更", "群内同步 + 经验判断处置"]; 
  before.forEach((t, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 1.02,
      y: 2.75 + i * 1.22,
      w: 5.25,
      h: 0.85,
      radius: 0.05,
      fill: { color: "FFF3F2" },
      line: { color: "FFD1CC" },
    });
    slide.addText(t, {
      x: 1.25,
      y: 2.97 + i * 1.22,
      w: 4.85,
      h: 0.35,
      fontFace: FONT_BODY,
      fontSize: 13,
      color: C.text,
      margin: 0,
    });
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 6.9,
    y: 1.95,
    w: 5.7,
    h: 4.95,
    radius: 0.08,
    fill: { color: C.white },
    line: { color: C.accent, pt: 1.2 },
  });
  slide.addText("改造后（AI协同）", {
    x: 7.2,
    y: 2.2,
    w: 2.8,
    h: 0.35,
    fontFace: FONT_HEAD,
    fontSize: 17,
    bold: true,
    color: C.accent,
    margin: 0,
  });
  const after = [
    "AI 汇聚指标 + 日志 + Trace，自动聚类同源告警",
    "结合 CMDB 与最近变更记录，给出根因 Top3",
    "自动生成 SOP 处置建议，支持一键执行并回写工单",
  ];
  after.forEach((t, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 7.2,
      y: 2.75 + i * 1.22,
      w: 5.1,
      h: 0.85,
      radius: 0.05,
      fill: { color: "EFFFFB" },
      line: { color: "B8F0E1" },
    });
    slide.addText(t, {
      x: 7.42,
      y: 2.87 + i * 1.22,
      w: 4.75,
      h: 0.52,
      fontFace: FONT_BODY,
      fontSize: 12.5,
      color: C.text,
      margin: 0,
    });
  });

  slide.addText("平均定位时间 40 min -> 12 min", {
    x: 7.2,
    y: 6.15,
    w: 5.0,
    h: 0.35,
    fontFace: FONT_HEAD,
    bold: true,
    fontSize: 16,
    color: C.dark,
    margin: 0,
  });
}

// Slide 5 Change release scenario
{
  const slide = pptx.addSlide();
  lightSlide(slide);
  title(slide, "场景二：发布变更工作流改造", false, "从“清单检查”升级为“风险自适应”的发布体系");

  const nodes = [
    ["代码合并", "解析变更范围与影响服务"],
    ["风险评估", "AI 结合历史事故给出风险分"],
    ["灰度策略", "按风险等级自动选择灰度比例"],
    ["健康门禁", "实时观测 SLI，异常自动暂停"],
    ["自动回滚", "触发阈值后执行回滚脚本"],
  ];

  nodes.forEach((n, i) => {
    const x = 0.82 + i * 2.45;
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 2.45,
      w: 2.2,
      h: 2.55,
      radius: 0.08,
      fill: { color: C.white },
      line: { color: C.light, pt: 1 },
    });
    slide.addShape(pptx.ShapeType.ellipse, {
      x: x + 0.78,
      y: 2.7,
      w: 0.62,
      h: 0.62,
      fill: { color: i === 1 || i === 3 ? C.gold : C.light },
      line: { color: C.light },
    });
    slide.addText(String(i + 1), {
      x: x + 0.98,
      y: 2.88,
      w: 0.22,
      h: 0.22,
      fontFace: FONT_HEAD,
      bold: true,
      fontSize: 13,
      color: C.dark,
      align: "center",
      margin: 0,
    });
    slide.addText(n[0], {
      x: x + 0.22,
      y: 3.47,
      w: 1.8,
      h: 0.35,
      fontFace: FONT_HEAD,
      bold: true,
      fontSize: 15,
      color: C.dark,
      align: "center",
      margin: 0,
    });
    slide.addText(n[1], {
      x: x + 0.2,
      y: 3.9,
      w: 1.82,
      h: 0.85,
      fontFace: FONT_BODY,
      fontSize: 11.5,
      color: C.text,
      align: "left",
      margin: 0,
    });
    if (i < nodes.length - 1) {
      slide.addShape(pptx.ShapeType.chevron, {
        x: x + 2.2,
        y: 3.45,
        w: 0.28,
        h: 0.4,
        fill: { color: C.accent },
        line: { color: C.accent },
      });
    }
  });

  slide.addText("结果：发布成功率 +18%，回滚耗时 -60%，夜间人工介入次数显著下降", {
    x: 0.84,
    y: 5.65,
    w: 12.0,
    h: 0.45,
    fontFace: FONT_BODY,
    italic: true,
    fontSize: 14,
    color: C.muted,
    margin: 0,
  });
}

// Slide 6 Incident review scenario
{
  const slide = pptx.addSlide();
  lightSlide(slide);
  title(slide, "场景三：故障复盘成为可复用的知识引擎", false, "让每次事故都反哺检测规则、应急脚本和发布策略");

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.75,
    y: 2.0,
    w: 12.0,
    h: 4.8,
    radius: 0.1,
    fill: { color: C.white },
    line: { color: C.light, pt: 1 },
  });

  const loop = [
    ["事故时间线", 0.88, 3.15],
    ["根因归类", 2.85, 3.15],
    ["改进建议", 4.82, 3.15],
    ["脚本固化", 6.79, 3.15],
    ["规则更新", 8.76, 3.15],
    ["知识回写", 10.73, 3.15],
  ];

  loop.forEach((n, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: n[1],
      y: n[2],
      w: 1.75,
      h: 0.78,
      radius: 0.05,
      fill: { color: i % 2 === 0 ? "EDF3FF" : "EFFFFB" },
      line: { color: C.light },
    });
    slide.addText(n[0], {
      x: n[1] + 0.1,
      y: n[2] + 0.25,
      w: 1.55,
      h: 0.3,
      fontFace: FONT_BODY,
      fontSize: 12,
      color: C.dark,
      align: "center",
      bold: true,
      margin: 0,
    });
  });

  const arrows = [
    [2.67, 3.42, 0.16, 0.22],
    [4.64, 3.42, 0.16, 0.22],
    [6.61, 3.42, 0.16, 0.22],
    [8.58, 3.42, 0.16, 0.22],
    [10.55, 3.42, 0.16, 0.22],
  ];
  arrows.forEach((a) => {
    slide.addShape(pptx.ShapeType.chevron, {
      x: a[0],
      y: a[1],
      w: a[2],
      h: a[3],
      fill: { color: C.accent },
      line: { color: C.accent },
    });
  });

  slide.addText("AI 自动生成复盘草稿，并将结论回写：SOP / 告警阈值 / 巡检策略", {
    x: 1.1,
    y: 6.1,
    w: 11.2,
    h: 0.35,
    fontFace: FONT_BODY,
    italic: true,
    fontSize: 14,
    color: C.muted,
    align: "center",
    margin: 0,
  });
}

// Slide 7 Architecture
{
  const slide = pptx.addSlide();
  darkSlide(slide);
  title(slide, "落地架构：四层能力编排", true, "统一接入、统一决策、统一执行、统一审计");

  const layers = [
    ["应用层", "告警处置 / 发布门禁 / 巡检 / 容量预测"],
    ["AI决策层", "检索增强(RAG)、策略引擎、风险评分、Action Planner"],
    ["执行层", "Ansible / Argo / Jenkins / K8s API / 工单系统"],
    ["数据层", "监控指标、日志、Trace、CMDB、知识库、历史工单"],
  ];
  layers.forEach((l, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 1.15,
      y: 1.95 + i * 1.18,
      w: 11.0,
      h: 0.95,
      radius: 0.07,
      fill: { color: i % 2 === 0 ? C.white : C.light, transparency: i === 0 ? 6 : 10 },
      line: { color: C.white, transparency: 80 },
    });
    slide.addText(l[0], {
      x: 1.45,
      y: 2.25 + i * 1.18,
      w: 1.8,
      h: 0.3,
      fontFace: FONT_HEAD,
      fontSize: 15,
      bold: true,
      color: C.dark,
      margin: 0,
    });
    slide.addText(l[1], {
      x: 3.15,
      y: 2.24 + i * 1.18,
      w: 8.65,
      h: 0.35,
      fontFace: FONT_BODY,
      fontSize: 13.5,
      color: C.dark,
      margin: 0,
    });
  });

  slide.addText("关键约束：所有自动执行动作必须具备审批、回滚与审计链路", {
    x: 1.2,
    y: 6.58,
    w: 11,
    h: 0.35,
    fontFace: FONT_BODY,
    fontSize: 12,
    color: C.light,
    margin: 0,
  });
}

// Slide 8 Capability matrix
{
  const slide = pptx.addSlide();
  lightSlide(slide);
  title(slide, "工具与能力矩阵：先集成，再替换", false, "优先复用现有平台资产，避免一次性重构风险");

  const headers = ["能力域", "现有工具", "AI改造动作", "阶段目标"];
  const colX = [0.8, 2.8, 5.6, 9.15];
  const colW = [1.8, 2.65, 3.45, 3.35];

  headers.forEach((h, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: colX[i],
      y: 2.05,
      w: colW[i],
      h: 0.6,
      radius: 0.04,
      fill: { color: C.dark },
      line: { color: C.dark },
    });
    slide.addText(h, {
      x: colX[i] + 0.12,
      y: 2.22,
      w: colW[i] - 0.24,
      h: 0.28,
      fontFace: FONT_BODY,
      bold: true,
      fontSize: 13,
      color: C.white,
      align: "center",
      margin: 0,
    });
  });

  const rows = [
    ["监控", "Prometheus/Grafana", "告警聚类 + 根因摘要", "告警降噪"],
    ["发布", "Jenkins/ArgoCD", "风险评分 + 自动门禁", "稳定交付"],
    ["工单", "Jira/禅道", "AI生成处置建议", "缩短响应"],
    ["知识", "Confluence/Wiki", "复盘自动结构化", "经验复用"],
  ];

  rows.forEach((r, i) => {
    const y = 2.85 + i * 0.95;
    const fill = i % 2 === 0 ? "FFFFFF" : "EFF3FF";
    colX.forEach((x, k) => {
      slide.addShape(pptx.ShapeType.roundRect, {
        x,
        y,
        w: colW[k],
        h: 0.82,
        radius: 0.03,
        fill: { color: fill },
        line: { color: C.light, pt: 0.7 },
      });
      slide.addText(r[k], {
        x: x + 0.1,
        y: y + 0.24,
        w: colW[k] - 0.2,
        h: 0.34,
        fontFace: FONT_BODY,
        fontSize: 12.5,
        color: C.text,
        align: k === 0 ? "center" : "left",
        margin: 0,
      });
    });
  });
}

// Slide 9 Roadmap
{
  const slide = pptx.addSlide();
  lightSlide(slide);
  title(slide, "90天推进路线图", false, "分阶段试点，先拿到可量化收益，再扩大到全链路");

  const phases = [
    ["0-30天", "数据打底", ["统一告警与日志字段", "梳理TOP20高频故障", "建立处置SOP模板"]],
    ["31-60天", "AI协同试点", ["告警归因助手上线", "发布风险评分接入流水线", "值班机器人联动工单"]],
    ["61-90天", "规模化推广", ["自动执行动作灰度放开", "故障复盘自动沉淀知识库", "按业务线复制流程模板"]],
  ];

  phases.forEach((p, i) => {
    const x = 0.85 + i * 4.18;
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 2.2,
      w: 3.9,
      h: 4.45,
      radius: 0.09,
      fill: { color: i === 1 ? "E9FFF8" : "FFFFFF" },
      line: { color: i === 1 ? C.accent : C.light, pt: 1 },
    });
    slide.addText(p[0], {
      x: x + 0.2,
      y: 2.47,
      w: 1.4,
      h: 0.32,
      fontFace: FONT_HEAD,
      bold: true,
      fontSize: 16,
      color: C.dark,
      margin: 0,
    });
    slide.addText(p[1], {
      x: x + 2.15,
      y: 2.47,
      w: 1.5,
      h: 0.32,
      fontFace: FONT_BODY,
      italic: true,
      fontSize: 13,
      color: C.muted,
      align: "right",
      margin: 0,
    });

    p[2].forEach((item, idx) => {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: x + 0.25,
        y: 3.1 + idx * 1.02,
        w: 0.24,
        h: 0.24,
        fill: { color: C.accent },
        line: { color: C.accent },
      });
      slide.addText(item, {
        x: x + 0.58,
        y: 3.04 + idx * 1.02,
        w: 3.1,
        h: 0.42,
        fontFace: FONT_BODY,
        fontSize: 12.5,
        color: C.text,
        margin: 0,
      });
    });

    if (i < phases.length - 1) {
      slide.addShape(pptx.ShapeType.chevron, {
        x: x + 4.03,
        y: 4.15,
        w: 0.14,
        h: 0.36,
        fill: { color: C.warn },
        line: { color: C.warn },
      });
    }
  });
}

// Slide 10 KPI and close
{
  const slide = pptx.addSlide();
  darkSlide(slide);
  title(slide, "治理与度量：确保AI可控、可信、可持续", true, "先做“可解释+可审计”，再做“全自动”");

  const kpis = [
    ["稳定性", "MTTR、告警降噪率、SLA达成率"],
    ["效率", "发布频次、变更失败率、自动化执行占比"],
    ["治理", "误操作数、回滚成功率、审计闭环率"],
  ];
  kpis.forEach((k, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: 0.95 + i * 4.15,
      y: 2.2,
      w: 3.8,
      h: 2.35,
      radius: 0.08,
      fill: { color: C.white, transparency: 8 },
      line: { color: C.light, transparency: 70 },
    });
    slide.addText(k[0], {
      x: 1.2 + i * 4.15,
      y: 2.55,
      w: 3.2,
      h: 0.4,
      fontFace: FONT_HEAD,
      fontSize: 22,
      bold: true,
      color: C.dark,
      align: "center",
      margin: 0,
    });
    slide.addText(k[1], {
      x: 1.2 + i * 4.15,
      y: 3.2,
      w: 3.2,
      h: 0.9,
      fontFace: FONT_BODY,
      fontSize: 13,
      color: C.text,
      align: "center",
      valign: "mid",
      margin: 0,
    });
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 1.5,
    y: 5.2,
    w: 10.3,
    h: 1.15,
    radius: 0.1,
    fill: { color: C.accent, transparency: 6 },
    line: { color: C.accent, transparency: 100 },
  });
  slide.addText("建议决策：以“告警处置 + 发布门禁”作为首批试点，8周内拿到可量化ROI", {
    x: 1.8,
    y: 5.6,
    w: 9.8,
    h: 0.42,
    fontFace: FONT_HEAD,
    fontSize: 17,
    bold: true,
    color: C.white,
    align: "center",
    margin: 0,
  });
}

const output = path.resolve("deliverables", "运维开发AI工作流改造方案.pptx");
pptx.writeFile({ fileName: output }).then(() => {
  console.log(`Created: ${output}`);
});
