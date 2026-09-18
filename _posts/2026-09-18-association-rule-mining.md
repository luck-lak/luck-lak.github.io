---
layout: post
title: "数据挖掘：关系规则挖掘"
lang: zh-CN
date: 2026-09-18 14:30:00 +0800
description: "从基本概念和两阶段框架出发，梳理 Apriori、FP-Growth 与关联规则生成的逻辑。"
---

<p class="post-lead">这是我数据挖掘课程的一份课堂笔记。我觉得这种挖掘数据的视角对于我来说挺新奇的，因为我以前对于数据挖掘的理解，一般都是像机器学习和深度学习那样，这种视角还是比较局限的。这一节关系规则挖掘通过先形式化一些概念，然后自然地推导出关系规则的一些挖掘算法。我这份笔记主要梳理了这一节的逻辑脉络；对于有些形式化定义，以及不同部分之间的中间衔接，由于课堂记录的原因，还是有所省略。课件可以在南大智科资源仓库中按课程找到，具体是<a href="https://github.com/NJUIS-Students/Resources/blob/main/%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/2025%E7%A7%8B/%E8%A2%81%E6%99%93%E5%BD%A4/%E8%AF%BE%E4%BB%B6/04-%E5%85%B3%E8%81%94%E8%A7%84%E5%88%99%E6%8C%96%E6%8E%98.pdf">数据挖掘的第四节</a>。</p>

<nav class="post-toc" aria-label="文章目录">
  <p class="post-toc-title">目录</p>
  <ol>
    <li><a href="#basic-concepts">基本概念与问题定义</a></li>
    <li><a href="#two-stage-problem">从关联规则到两阶段问题</a></li>
    <li><a href="#apriori">Apriori：利用先验原理剪枝</a></li>
    <li><a href="#fp-growth">FP-Growth：绕开候选项生成</a></li>
    <li><a href="#rule-generation">Rule Generation：从频繁项集产生规则</a></li>
    <li><a href="#supplement">补充定义与推导</a></li>
  </ol>
</nav>

## 一、基本概念与问题定义 {#basic-concepts}

### 基本概念

| 概念 | 说明 |
| --- | --- |
| 项（Item） | 数据中被关注的单个对象。 |
| 项集（Itemset） | 由若干个项组成的集合。 |
| 事务（Transaction） | 一次记录中同时出现的项的集合。 |
| 支持度计数（Support Count） | 包含某个项集的事务数量，常记为 `σ(X)`。 |
| 支持度（Support） | 包含某个项集的事务占全部事务的比例。 |
| 频繁项集（Frequent Itemset） | 支持度不小于最小支持度 `minsup` 的项集。 |
| 最大频繁项集（Maximal Frequent Itemset） | 自身频繁、但它的直接超集都不频繁的项集。 |
| 置信度（Confidence） | 衡量规则 `X → Y` 在前件 `X` 出现时，后件 `Y` 也出现的比例。 |

### 什么样的规则值得留下？

人为设定两个阈值：

- `minsup`：最小支持度；
- `minconf`：最小置信度。

课件对“关联规则挖掘问题”的正式定义就是：**找出同时满足最小支持度和最小置信度的所有规则。**

最终目标是寻找好的关联规则：

```text
X → Y
```

## 二、从关联规则到两阶段问题 {#two-stage-problem}

### 为什么要先找频繁项集？

如果一条规则的支持度不小于最小支持度，那么 `X ∪ Y` 必须是一个频繁项集，因为：

```text
support(X → Y) = support(X ∪ Y)
```

这是从“关联规则”过渡到“频繁项集挖掘”的关键。

### 关联规则挖掘的两个阶段

关联规则挖掘可以拆成两个阶段：

1. **Frequent Itemset Generation**

   找出所有满足 `support(X) ≥ minsup` 的项集 `X`。

2. **Rule Generation**

   从频繁项集中拆出 `X → Y`，检查其置信度；满足 `confidence(X → Y) ≥ minconf` 的就是强规则。

> 关联规则挖掘 = 频繁项集产生 + 规则产生。先产生满足 `minsup` 的频繁项集，再从中产生满足 `minconf` 的关联规则。

真正困难的是第一阶段：可能的项集数量会随 Item 数量指数增长，暴力枚举的代价很高。但这里存在一个重要性质：

```text
X ⊆ Y  ⇒  support(Y) ≤ support(X)
```

因此，如果一个项集已经不频繁，那么它的所有超集也一定不频繁，可以全部剪掉。

核心问题于是变成：**如何利用这个性质，大量减少需要检查的候选项集？** 这就是 Apriori 算法的出发点。

这一段的逻辑可以概括为：

```text
定义“什么是好规则”
        ↓
好规则必然建立在频繁项集上
        ↓
先挖掘频繁项集
        ↓
暴力枚举会导致组合爆炸
        ↓
利用支持度的包含关系进行剪枝
        ↓
Apriori
```

## 三、Apriori：利用先验原理剪枝 {#apriori}

### 理论基础

如果 `X ⊆ Y`，那么：

```text
support(Y) ≤ support(X)
```

背后的直觉是：向项集中加入更多 Item 后，能同时包含所有这些 Item 的事务只会变少，不会变多。

由此可以推出 Apriori 先验原理的两个等价方向：

- 如果一个项集是频繁的，它的所有子集一定频繁；
- 如果一个项集不频繁，它的所有超集一定不频繁。

算法真正利用得最多的是第二个方向，因为它可以用来剪枝。

### 每一轮做什么？

Apriori 的每一轮主要做两件事：

1. 利用上一层的频繁项集和 Apriori 原理，生成并剪枝得到候选项集 `C_k`；
2. 扫描数据库，计算 `C_k` 中各项集的支持度，筛选得到频繁项集 `L_k`。

这里还有一个难点：怎样从 `L_{k-1}` 生成 `C_k`？

#### Step 1：Join

将 `L_{k-1}` 中满足连接条件的频繁项集进行连接，产生大小为 `k` 的候选项集。

#### Step 2：Prune

对于生成的候选项集 `X`，检查它所有大小为 `k-1` 的子集。只有当这些子集都在 `L_{k-1}` 中时，`X` 才能进入 `C_k`。

> **Apriori 候选生成 = Join + Prune。** Join 保证候选可以由两个频繁的 `(k-1)` 项集连接得到；Prune 再检查候选的所有 `(k-1)` 项子集。只要有一个子集不频繁，就根据 Apriori 原理直接删除该候选。

Join 为什么不会漏掉真正的频繁 `k` 项集，放在文末的[补充推导](#why-join-works)中说明。

## 四、FP-Growth：绕开候选项生成 {#fp-growth}

Apriori 有几个明显的缺点：

- 需要多次扫描数据库；
- 候选项规模可能非常庞大；
- 支持度计算的开销很大。

所以一个很自然的问题出现了：

> **能不能干脆不要 Candidate Generation？**

这就是 FP-Growth 的重要出发点。

### 核心思想

FP-Growth 是 Frequent Pattern Growth 的缩写。它不再像 Apriori 那样不断生成 `C_1, C_2, C_3, ...`，而是先把整个事务数据库压缩进一棵 FP-tree，然后直接从树中挖掘频繁模式。

### 第一次扫描：清洗并统一事务顺序

第一次扫描数据库时：

1. 统计每个 Item 的 Support Count；
2. 删除不频繁的 Item；
3. 按照全局 Support Count 的降序排列 Item；
4. 按照这一统一顺序重排每条 Transaction。

最终得到一个经过“清洗 + 排序”的事务数据库。

### 第二次扫描：构建 FP-tree

逐条插入排序后的事务：

- 如果新事务与已有路径共享祖先节点，就增加对应节点的计数；
- 如果没有对应节点，就创建新节点。

同时维护 Header Table（项头表）：将 FP-tree 中表示同一个 Item 的节点通过 Node Link 连接起来，方便之后快速找到某个 Item 在树中的所有位置。

到这里，FP-tree 就构建完成了。

### 怎样从 FP-tree 中挖掘频繁项集？

课件给出的路线是：

```text
选择一个 Item 作为后缀
        ↓
寻找所有通向它的前缀路径
        ↓
得到条件模式基（CPB）
        ↓
在 CPB 中重新统计频率
        ↓
得到包含该后缀的频繁项集
        ↓
递归
```

## 五、Rule Generation：从频繁项集产生规则 {#rule-generation}

到这里，Apriori 和 FP-Growth 已经解决了第一阶段：Frequent Itemset Generation。现在进入第二阶段：Rule Generation。

为了避免和规则右侧的 `Y` 混淆，下面把一个已经找到的频繁项集记作 `F`。枚举 `F` 的所有非空真子集 `X`，可以产生：

```text
X → F - X
```

例如，给定 `F = {A, B, C}`，可以产生：

```text
AB → C
AC → B
BC → A
A  → BC
B  → AC
C  → AB
```

由于 `F` 已经是频繁项集：

```text
support(F) ≥ minsup
```

而且：

```text
support(X → F-X) = support(F)
```

所以这些候选规则天然满足 `minsup`，第二阶段只需要检查：

```text
confidence ≥ minconf
```

对于一个包含 `k` 个 Item 的频繁项集：

```text
候选规则数量 = 2^k - 2
```

因此，规则产生本身也可能出现组合爆炸。

### Rule Generation 的剪枝

一般情况下，Confidence 不具有普通的反单调性。但是，对于从同一个频繁项集 `F = {A, B, C, D}` 产生的规则：

```text
ABC → D
AB  → CD
A   → BCD
```

有：

```text
confidence(ABC → D)
    ≥ confidence(AB → CD)
    ≥ confidence(A → BCD)
```

原因是这些规则的 Confidence 分子都是 `support(ABCD)`，而前件越来越小，前件的 Support 越来越大，因此 Confidence 越来越小。

所以，如果某条规则已经低于 `minconf`，继续把 Item 从前件移动到后件得到的规则，也可以直接剪掉。

## 六、补充定义与推导 {#supplement}

### Confidence 的定义 {#confidence}

对于关联规则 `X → Y`：

```text
confidence(X → Y)
    = support(X ∪ Y) / support(X)
    = σ(X ∪ Y) / σ(X)
```

它表示：在所有包含 `X` 的事务中，同时也包含 `Y` 的事务所占的比例。也可以把它理解为条件概率：

```text
confidence(X → Y) = P(Y | X)
```

例如，`A` 出现在 6 条事务中，`A` 和 `B` 同时出现在 4 条事务中，那么：

```text
confidence(A → B) = 4 / 6 = 2/3
```

需要注意，Confidence 是有方向的：

```text
confidence(A → B) 不一定等于 confidence(B → A)
```

因为两者的分母分别是 `support(A)` 和 `support(B)`。

### Join 为什么不会漏掉真正的频繁 k 项集？ {#why-join-works}

如果一个 `k` 项集 `X` 真的是频繁的，根据 Apriori 原理，它的所有 `(k-1)` 项子集一定都在 `L_{k-1}` 中。

因此，按照固定的 Item 顺序，其中一定存在两个可以通过 Join 重新产生 `X` 的 `(k-1)` 项子集。

所以，**Join + Prune 不会剪掉真正的频繁项集。**

### CPB：Conditional Pattern Base {#cpb}

对于一个固定后缀 `X`，收集 FP-tree 中所有通向 `X` 的前缀路径，就得到了 `X` 的 Conditional Pattern Base（条件模式基）。

直觉上，`CPB(X)` 可以理解为：**只研究包含 `X` 的模式时，所需要的局部小数据库。**

例如：

```text
CPB(E) = {ACD: 1, AD: 1, BC: 1}
```
