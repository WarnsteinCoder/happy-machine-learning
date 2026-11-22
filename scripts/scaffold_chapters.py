"""Scaffold chapter folders from the table of contents of Li Hang's book."""

from __future__ import annotations

import argparse
from pathlib import Path


# Chapter number, Chinese title, and stable ASCII directory slug.
CHAPTERS = (
    (1, "机器学习简介", "machine_learning_intro"),
    (2, "监督学习简介", "supervised_learning_intro"),
    (3, "线性回归", "linear_regression"),
    (4, "感知机", "perceptron"),
    (5, "k近邻法", "knn"),
    (6, "朴素贝叶斯法", "naive_bayes"),
    (7, "决策树", "decision_tree"),
    (8, "逻辑斯谛回归和最大熵模型", "logistic_regression_max_entropy"),
    (9, "支持向量机", "support_vector_machine"),
    (10, "提升方法", "boosting"),
    (11, "隐马尔可夫模型", "hidden_markov_model"),
    (12, "条件随机场", "conditional_random_field"),
    (13, "监督学习方法总结", "supervised_learning_summary"),
    (14, "无监督学习简介", "unsupervised_learning_intro"),
    (15, "聚类方法", "clustering"),
    (16, "奇异值分解", "singular_value_decomposition"),
    (17, "主成分分析", "principal_component_analysis"),
    (18, "EM算法和变分EM算法", "em_and_variational_em"),
    (19, "马尔可夫链蒙特卡罗法", "markov_chain_monte_carlo"),
    (20, "潜在语义分析和非负矩阵分解", "latent_semantic_analysis_nmf"),
    (21, "概率潜在语义分析", "probabilistic_latent_semantic_analysis"),
    (22, "潜在狄利克雷分配", "latent_dirichlet_allocation"),
    (23, "无监督学习方法总结", "unsupervised_learning_summary"),
    (24, "深度学习简介", "deep_learning_intro"),
    (25, "前馈神经网络", "feedforward_neural_network"),
    (26, "卷积神经网络", "convolutional_neural_network"),
    (27, "循环神经网络", "recurrent_neural_network"),
    (28, "Transformer", "transformer"),
    (29, "GPT和BERT", "gpt_and_bert"),
    (30, "变分自编码器", "variational_autoencoder"),
    (31, "生成对抗网络", "generative_adversarial_network"),
    (32, "扩散模型", "diffusion_model"),
    (33, "深度学习方法总结", "deep_learning_summary"),
    (34, "强化学习简介", "reinforcement_learning_intro"),
    (35, "马尔可夫决策过程", "markov_decision_process"),
    (36, "多臂老虎机", "multi_armed_bandit"),
    (37, "基于价值的方法", "value_based_methods"),
    (38, "深度Q网络", "deep_q_network"),
    (39, "基于策略的方法", "policy_based_methods"),
    (40, "近端策略优化PPO", "proximal_policy_optimization"),
    (41, "强化学习方法总结", "reinforcement_learning_summary"),
)


def module_for(chapter_number: int) -> str:
    if chapter_number <= 13:
        return "01_supervised"
    if chapter_number <= 23:
        return "02_unsupervised"
    if chapter_number <= 33:
        return "03_deep_learning"
    return "04_reinforcement_learning"


def chapter_files(number: int, title: str, slug: str, module: str) -> dict[str, str]:
    chapter_id = f"ch{number:02d}_{slug}"
    prefix = f"{module}/ch{number:02d}_{slug}"
    notes = f"""---
id: {chapter_id}
module: {module}
title: {title}
prereqs: []
status:
  derivation: 0
  params: 0
  code: 0
last_reviewed: null
---

# 第{number}章 {title}

## 学习目标

- 

## 核心概念

待结合本章 PDF 整理。

## 公式推导

待结合本章 PDF 整理。

## 参数意义

待结合本章 PDF 整理。

## 代码实践

按需实现；代码骨架见 [impl.py](impl.py)，验证骨架见 [test_verify.py](test_verify.py)。

## 来源与复习记录

- 书籍版本：待补充
- 对应书上页码 / PDF 页码：待补充
- 本章 PDF：`materials/source.pdf`
- 面试题：[interview_questions.md](interview_questions.md)
- 复习记录：
"""
    interview = f"""# 第{number}章 {title}：面试题

> 来源：书名与版本待填写；对应页码待填写。

## 概念题

### 问题

待结合本章 PDF 整理。

**参考答案要点：**

- 

**来源：** 第 __ 页

## 推导题

### 问题

待结合本章 PDF 整理。

**参考答案要点：**

- 

**来源：** 第 __ 页

## 算法与参数题

### 问题

待结合本章 PDF 整理。

**参考答案要点：**

- 

**来源：** 第 __ 页

## 追问与易错点

- 追问：
- 易错点：
"""
    materials = f"""# 第{number}章 {title}：学习材料

将本章对应的 PDF 放在本目录并命名为 `source.pdf`。本目录只放这一章的 PDF 和相关页面摘录，不放整篇或整本 PDF。

学习后告诉 AI 本章重点或希望整理的问题。AI 输出应更新本章的 `notes.md` 与 `interview_questions.md`，并标注书上页码；若 PDF 页码与书上页码不同，两者都记录。
"""
    return {
        f"{prefix}/notes.md": notes,
        f"{prefix}/interview_questions.md": interview,
        f"{prefix}/impl.py": '"""User-owned implementation scaffold for this chapter."""\n',
        f"{prefix}/test_verify.py": '"""User-owned verification scaffold for this chapter."""\n',
        f"{prefix}/materials/README.md": materials,
    }


def toc_markdown() -> str:
    parts = (
        ("01_supervised", "第一篇 监督学习", 1, 13),
        ("02_unsupervised", "第二篇 无监督学习", 14, 23),
        ("03_deep_learning", "第三篇 深度学习", 24, 33),
        ("04_reinforcement_learning", "第四篇 强化学习", 34, 41),
    )
    lines = ["# 李航《机器学习方法》目录", "", "按章学习。每章 PDF 放在对应章节目录的 `materials/source.pdf`。", ""]
    for module, title, start, end in parts:
        lines.extend((f"## {title}", ""))
        for number, chapter_title, slug in CHAPTERS[start - 1:end]:
            path = f"{module}/ch{number:02d}_{slug}/notes.md"
            lines.append(f"- 第{number}章 [{chapter_title}]({path})")
        lines.append("")
    lines.extend(("## 附录", "", "目录 PDF 还列有附录 A-G。当前章节框架按四篇、41 章建立；需要学习附录时再补充到 `00_math_foundations/appendices/`。", ""))
    return "\n".join(lines)


def scaffold(root: Path) -> tuple[int, int]:
    root = Path(root).resolve()
    created = 0
    existing = 0
    for number, title, slug in CHAPTERS:
        module = module_for(number)
        for relative_path, content in chapter_files(number, title, slug, module).items():
            path = root / relative_path
            if path.exists():
                existing += 1
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
            created += 1

    toc_path = root / "Book_TOC.md"
    if toc_path.exists():
        existing += 1
    else:
        toc_path.write_text(toc_markdown(), encoding="utf-8", newline="\n")
        created += 1
    return created, existing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    args = parser.parse_args()
    created, existing = scaffold(args.root)
    print(f"Scaffold complete: {created} files created, {existing} existing files preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
