# 学习仪表盘

## 板块进度

```dataviewjs
const modules = [
  ["00_math_foundations", "数学基础"],
  ["01_supervised", "监督学习"],
  ["02_unsupervised", "无监督学习"],
  ["03_deep_learning", "深度学习"],
  ["04_reinforcement_learning", "强化学习"],
];
const pages = dv.pages().where(p => modules.some(([folder]) =>
  p.file.folder === folder || p.file.folder.startsWith(folder + "/")
));
const rows = modules.map(([folder, label]) => {
  const section = pages.where(p => p.file.folder === folder || p.file.folder.startsWith(folder + "/"));
  const count = section.length;
  const complete = section.array().reduce((sum, p) => sum +
    [p.status?.derivation, p.status?.params, p.status?.code]
      .filter(value => Number.isInteger(value)).reduce((a, value) => a + value, 0), 0);
  const percent = count ? Math.round(complete / (count * 6) * 100) : 0;
  return [label, count, `${percent}%`];
});
dv.table(["板块", "章节数", "综合进度"], rows);
```

## 三维状态

```dataviewjs
const modules = ["00_math_foundations", "01_supervised", "02_unsupervised", "03_deep_learning", "04_reinforcement_learning"];
const pages = dv.pages().where(p => modules.some(folder =>
  p.file.folder === folder || p.file.folder.startsWith(folder + "/")
)).sort(p => p.module).sort(p => p.title);
const label = value => ({0: "未开始", 1: "进行中", 2: "已掌握"})[value] ?? "缺失";
dv.table(["章节", "公式推导", "参数意义", "代码实现"],
  pages.map(p => [p.title, label(p.status?.derivation), label(p.status?.params), label(p.status?.code)])
);
```

## 待复习（超过 14 天）

```dataviewjs
const modules = ["00_math_foundations", "01_supervised", "02_unsupervised", "03_deep_learning", "04_reinforcement_learning"];
const cutoff = dv.date("today").minus({days: 14});
const pages = dv.pages().where(p => modules.some(folder =>
  p.file.folder === folder || p.file.folder.startsWith(folder + "/")
)).where(p => {
  if (!p.last_reviewed) return false;
  const reviewed = dv.date(p.last_reviewed);
  return reviewed && reviewed < cutoff;
}).sort(p => p.last_reviewed, "asc");
dv.table(["章节", "上次复习"], pages.map(p => [p.title, p.last_reviewed]));
```
