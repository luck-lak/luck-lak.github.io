---
layout: post
title: "Feature Engineering：算法学习笔记"
lang: zh-CN
date: 2026-09-18 17:58:00 +0800
description: "这是我学习 Feature Engineering 的一些笔记，主要从算法方面学习，很多代码实现刻意跳过了。"
math: true
---

<p class="post-lead">这是我学习Feature Engineering的一些笔记，但是主要是从算法方面学习，很多代码实现我刻意跳过了，目的是降低学习负担，同时避免过快感到无聊。学习渠道是Codecademy平台的Feature Engineering Skill Path。总体学习下来感觉收获还是挺多的，一方面完善了知识地图，对于这个领域了解更多了；另一方面也了解了很多算法。</p>

## 前言
主要是自己的笔记整合在一起，不太适合直接阅读学习，建议看个目录知道有什么，如果感兴趣再自行探索

<nav class="post-toc" aria-label="文章目录">
  <p class="post-toc-title">目录</p>
  <ol>
    <li><a href="#numerical-transformation">Transforming Date into Features--Numerical Transformation</a></li>
    <li><a href="#categorical-transformation">Transforming Date into Features--Categorical Transformation</a></li>
    <li><a href="#feature-selection-methods">Feature Selection Methods--Filter Methods</a></li>
    <li><a href="#wrapper-methods">Feature Selection Methods--Wrapper Methods</a></li>
    <li><a href="#regularization">Regularization</a></li>
    <li><a href="#feature-importance">Feature Importance</a></li>
    <li><a href="#dimensionality-reduction">Dimensionality Reduction</a></li>
    <li><a href="#pca">PCA</a></li>
    <li><a href="#lda">LDA</a></li>
  </ol>
</nav>

<a id="numerical-transformation"></a>

## Numerical Transformation

### Standardization

```text
Standardization
    ↓
改变尺度
mean = 0, std = 1
```

### Min-Max

```text
Min-Max
    ↓
改变尺度
压到 [0, 1]
```

### Binning

```text
Binning
    ↓
降低精度
连续数值 → 区间类别
```

### Log Transformation

```text
Log Transformation
    ↓
压缩大值 / 长尾
绝对差异 → 更关注比例差异
```

---

<a id="categorical-transformation"></a>

## Categorical Transformation

Categorical Encoding 本质上是在为现实中的类别选择一种数学 representation，而你选择哪种 representation，就决定了模型如何“看待”这些类别，也会偷偷给模型加入某些假设。 Ordinal Encoding 假设类别存在顺序，One-Hot 假设类别彼此独立且地位对称，Binary/Hashing 用更紧凑的表示换取维度降低，但可能引入人为结构或信息碰撞，Target Encoding 则利用类别与预测目标的统计关系，同时带来数据泄漏和过拟合风险。

```text
我有一个 categorical feature
                │
                ▼
       类别本身有顺序吗？
          /                \
        Yes              No
        │                 │
        ▼                 ▼
     Ordinal           Nominal
     Encoding             │
                          ▼
                     类别多不多？
                         /       \
                      少         很多
                      │           │
                      ▼           ▼
                 One-Hot     考虑其他编码
                                     Binary 等
```

### 一个更完善的框架

```text
我有一个 Categorical Feature
│
├── ① 类别本身存在真实顺序吗？
│
│     ├── Yes → Ordinal
│     │          │
│     │          └── Ordinal Encoding
│     │
│     │              small < medium < large
│     │                  ↓       ↓       ↓
│     │                  0       1       2
│     │
│     │          保留：顺序关系
│     │          注意：数字间距未必有真实意义
│     │
│     └── No → Nominal
│              │
│              ├── ② 类别数量（Cardinality）较少
│              │
│              │      └── One-Hot Encoding
│              │          red   → [1, 0, 0]
│              │          blue  → [0, 1, 0]
│              │          green → [0, 0, 1]
│              │
│              │          优点：
│              │          · 不引入人为大小顺序
│              │          · 表示简单、可解释
│              │
│              │          缺点：
│              │          · K 个类别 ≈ K 个特征
│              │          · High Cardinality 时维度爆炸
│              │
│              └── ③ 类别数量很多（High Cardinality）
│                     │
│                     ├── Binary Encoding
│                     │
│                     │     Category → ID → Binary
│                     │     A → 0 → 00
│                     │     B → 1 → 01
│                     │     C → 2 → 10
│                     │     D → 3 → 11
│                     │
│                     │     维度：约 log₂(K)
│                     │     优点：大幅降低维度
│                     │     缺点：引入人为 bit 结构
│                     │
│                     ├── Hash Encoding
│                     │
│                     │     Category
│                     │         ↓ hash()
│                     │     固定数量的 buckets
│                     │
│                     │     优点：
│                     │     · 最终维度可以预先固定
│                     │     · 适合海量类别
│                     │
│                     │     缺点：
│                     │     · Hash Collision
│                     │     · 不同类别可能撞进同一 bucket
│                     │
│                     └── Target Encoding
│                           │
│                           │   Category
│                           │      ↓
│                           │   与 Target 的统计关系
│                           │
│                           │   A → mean(y | A)
│                           │   B → mean(y | B)
│                           │
│                           │   优点：
│                           │   · 低维
│                           │   · 直接利用类别与目标的关系
│                           │
│                           │   风险：
│                           │   · Data Leakage
│                           │   · Overfitting
│                           │
│                           └── 必须特别注意训练/验证数据隔离
│
├── ④ 如果只是需要给 Category 一个 ID
│
│     └── Label Encoding
│
│         A → 0
│         B → 1
│         C → 2
│
│         本质：Category → ID
│
│         ⚠ 对无序输入特征要谨慎：
│           某些模型可能把 0,1,2 当成
│           大小/距离关系
│
└── ⑤ 如果 Category 实际上来自 Date-Time
      │
      └── Date-Time Feature Extraction
          │
          ├── year
          ├── month
          ├── weekday
          ├── hour
          ├── is_weekend
          └── ...

          对周期变量进一步考虑：

          hour → sin(2π·hour/24)
               → cos(2π·hour/24)

          从而保留：
          23:00 ≈ 00:00 ≈ 01:00
```

---

<a id="feature-selection-methods"></a>

## Feature Selection Methods

### Filter Methods

在训练模型之前，单独看每个特征本身，或者它与目标变量之间的统计关系，然后决定哪些特征值得保留。

- Variance：这个特征自己有没有变化？
- Pearson correlation：这个特征和目标之间有没有线性关系？
- 注：Pearson correlation有优美的几何解释，本质是“两个向量的夹角”
- F-statistic / p-value：这个线性关系从统计意义上看够不够强？
- Mutual Information：这个特征和目标之间有没有任意形式的依赖关系，不局限于线性？
- 注：这三个统计量的数学定义我还没看明白（感觉涉及的数学知识还挺多）

#### variance thresholds

#### correlation（Pearson correlation coefficient）

2 main ways of using correlation for feature selection:

- to detect correlation between features
- to detect correlation between a feature and the target variable

（F-Statistic和p-value分别是什么，然后这里也没有说Pearson correlation coefficient的定义）

#### mutual information

### 这一节笔记总体梳理

#### Filter Methods

核心：

在训练模型之前，根据 feature 本身或 feature-target 的统计关系筛选特征。

#### 1. Variance Threshold

```text
Var(X)

方差太小：
X 几乎不变化
→ 几乎不提供信息
→ remove
```

#### 2. Pearson Correlation

$$
r = \frac{Cov(X,Y)}{std(X)std(Y)}
$$

范围：

$$
-1 \le r \le 1
$$

本质：

衡量线性关系，也可以理解为中心化后的两个向量的 cosine similarity。

两种用途：

- feature-feature：检测冗余特征
- feature-target：检测对 target 的线性预测能力

缺陷：

- 只能检测线性关系
- r = 0 不代表 X,Y 独立

#### 3. F-statistic

在线性回归中：

$$
H_0: beta = 0
$$

$$
F \approx \frac{explained\ variance}{unexplained\ variance}
$$

F 越大：

feature 与 target 的线性关系越强。

单特征回归：

$$
F = \frac{r^2}{1-r^2} \times (n-2)
$$

#### 4. p-value

假设 H0 为真时，得到当前这么极端甚至更极端统计量的概率。

p 越小：

数据与 H0 越不一致。

注意：

p-value 小 != effect size 大

#### 5. Mutual Information

$$
I(X;Y) = H(Y) - H(Y|X)
$$

含义：

知道 X 后，Y 的不确定性减少了多少。

另一种定义：

$$
I(X;Y) = \sum p(x,y) \log\frac{p(x,y)}{p(x)p(y)}
$$

等价于：

$$
I(X;Y) = KL(P(X,Y)\;||\;P(X)P(Y))
$$

如果独立：

$$
I(X;Y) = 0
$$

优点：

- 可以检测 nonlinear dependence
- 可以处理 discrete variables

相比 Pearson：

```text
Pearson → linear dependence
MI      → general dependence
```

- Wrapper Methods
- Embedded Methods

---

<a id="wrapper-methods"></a>

## Wrapper Methods

This lesson will explain five different wrapper methods:

- Sequential forward selection
- Sequential backward selection
- Sequential forward floating selection
- Sequential backward floating selection
- Recursive feature elimination

### Sequential Forward Selection（SFS）

Sequential Forward Selection 是一种 Wrapper Method，用模型性能来选择特征。

基本流程：

1. 从空特征集开始。
2. 每一轮尝试加入一个尚未选择的特征。
3. 分别训练并评估模型。
4. 选择使模型表现最好的那个特征加入当前特征集。
5. 重复以上过程，直到达到指定的特征数量。

例如：

初始特征：

`age, height, weight, blood_pressure, resting_heart_rate`

若第一轮 `age` 表现最好，则下一轮测试：

```text
{age, height}
{age, weight}
{age, blood_pressure}
{age, resting_heart_rate}
```

SFS 属于贪心算法（Greedy Algorithm）：

- 每一步都选择“当前最好”的特征。
- 优点：比暴力枚举所有特征组合快很多。
- 缺点：不能保证最终得到全局最优的特征组合。

核心思想：

```text
当前特征集 + 每个未选择特征 → 比较模型性能 → 保留最佳组合
```

### 总结;

#### Wrapper Methods

Wrapper methods 通过实际训练 ML model 来评价 feature subset，目标是在大量可能的特征组合中寻找性能较好的子集。

#### SFS（Sequential Forward Selection）

从空集开始，每次加入使模型性能提升最大的 feature。

Greedy，已加入的特征不能删除。

#### SBS（Sequential Backward Selection）

从所有 features 开始，每次删除后模型表现最好的 feature。

Greedy，已删除的特征不能恢复。

#### SFFS / SBFS（Floating Selection）

在 Forward / Backward Selection 基础上允许有限“反悔”：加入后可以删除，删除后可以重新加入。

可以修正部分早期 greedy decision，但计算量更高。

#### RFE（Recursive Feature Elimination）

训练模型 → 根据 feature importance 排名 → 删除最弱 feature → 重新训练 → 重复。

与 Sequential Methods 不同，RFE 主要利用模型本身给出的 feature importance。

核心：

$$
\text{Feature Selection} = \text{搜索 feature subset} + \text{评价 model performance}
$$

Wrapper Methods 通常比 Filter Methods 计算成本更高，但考虑了具体模型与特征之间的关系。

---

<a id="regularization"></a>

## Regularization

### Why Regularize? 为什么需要正则化

因为有overfitting。

然后看The Loss Function，只优化 Loss 有风险 → 改变优化目标，加入正则项。

“拼命降低训练误差”可能导致参数变大？

我目前的理解是：我还不知道会不会导致，但是因为可能会有这种现象，然后这种现象又确实会容易导致过拟合，所以我就加一个正则项来惩罚这种大参数的行为。

### L1 / Lasso Regularization

正则项老是把参数往0拉，起到了一个feature selectio的作用。

- L1笔记链接：[https://chatgpt.com/s/t_6aace677fee081919b368316dbac23d9](https://chatgpt.com/s/t_6aace677fee081919b368316dbac23d9)
- 精简版链接：[https://chatgpt.com/s/t_6aace68f64708191a14a69ec6cda6a6d](https://chatgpt.com/s/t_6aace68f64708191a14a69ec6cda6a6d)

L1 regularization 在原始 loss 上增加参数绝对值之和作为惩罚。它并不是单纯追求参数变小，而是在“拟合训练数据”和“使用较简单参数”之间权衡。L1 的一个特殊性质是能够使部分参数精确变成 0，因此可以产生稀疏模型，并起到 embedded feature selection 的作用。

### L2 / Ridge Regularization

[https://chatgpt.com/s/t_6aace81b03548191a519575d71eede05](https://chatgpt.com/s/t_6aace81b03548191a519575d71eede05)

定义：

$$
J(w) = L(w) + \lambda\sum w_j^2 = L(w) + \lambda||w||_2^2
$$

注意：

真正的 L2 norm 是：

$$
||w||_2 = \sqrt{\sum w_j^2}
$$

L2 regularization 常用的是 squared L2 norm。

参数更新：

$$
w \leftarrow w - \eta\left(\frac{\partial L}{\partial w} + 2\lambda w\right)
$$

直觉：

- 参数越大，惩罚越强
- 参数越接近 0，L2 的拉力也越弱
- 因此通常只是把参数缩小，不容易直接压成 0

作用：

- 限制大参数
- 降低模型敏感性
- 缓解过拟合
- 通常保留所有特征

几何直觉：

L2 约束：

$$
w_1^2 + w_2^2 \le t
$$

二维是圆，没有尖角，所以最优点通常不会落在坐标轴上。

对比：

- L1：容易产生 wj = 0 → sparse model / feature selection
- L2：让 wj 变小 → shrink / weight decay

L1 和 L2 对比的这里还是很好理解的，但是关于几何视角和很多更深度的视角，我暂时接触不到（我知道有，AI 给我列出了很多），反正其实这里的数学理论可以很深。

但是我不是想强调数学，而是想强调理解的视角有很多。

### Hyperfinetuing

Cross Validation

最常见：K-Fold Cross Validation

### Bias-Variance Tradeoff

```text
模型太复杂
    ↓
容易 overfitting
    ↓
High Variance
    ↓
加入 Regularization
    ↓
限制参数
    ↓
模型更简单
    ↓
Variance 降低
但 Bias 会升高
    ↓
通过 Validation / CV
选择合适的 λ
```

### 整节脉络

#### Regularization

Goal:

```text
reduce overfitting by controlling model complexity.
```

General objective:

$$
J(\theta) = L(\theta) + \lambda R(\theta)
$$

where:

- L(θ): original loss
- R(θ): complexity penalty
- λ: regularization strength

```text
λ ↑:
    model simpler
    bias ↑
    variance ↓

λ ↓:
    model more flexible
    bias ↓
    variance ↑
```

#### L1 / Lasso

$$
J(w) = L(w) + \lambda \sum|w_j|
$$

Effects:

- shrink coefficients
- some coefficients become exactly 0
- sparse model
- implicit feature selection

#### L2 / Ridge

$$
J(w) = L(w) + \lambda \sum w_j^2
$$

Effects:

- shrink coefficients toward 0
- usually not exactly 0
- stabilizes model
- useful for correlated features

Before L1/L2:

```text
usually standardize features.
```

Hyperparameter tuning:

$$
\lambda^* = \operatorname*{argmin}_{\lambda} ValidationLoss(\lambda)
$$

usually using:

- validation set
- or cross-validation

Bias-Variance:

```text
Expected Error
    ≈ Bias² + Variance + Noise

regularization:
    increases bias
    decreases variance
```

#### Regularization Terms

- L1
- L2
- Elastic Net
- Group Lasso
- ...

#### Other Regularization Methods

- Dropout
- Early Stopping
- Data Augmentation
- Weight Decay

### 总结

其实这里大部分概念，我都见过，但感觉总体下来还是有收获的，一方面是把整个正则化的脉络梳理了一遍，然后其次是对于想L1，L2 有了一些更深入的理解，原来看这两个名字都不知道是什么，然后也知道了选择不同的正则项对于模型参数的影响，比如L1倾向使得sparse model，而L2倾向于使得weight decay。同时还知道了，对于这些正则项的理解有很多不同的视角，理论确实能指导实践。

比如：

- 选 L1（Lasso）：你怀疑很多特征其实没用，想让模型自动做一点 feature selection，得到稀疏模型。
- 选 L2（Ridge）：你觉得大部分特征都有点用，只是不希望某些权重特别大；或者特征之间相关性比较强。通常 L2 更稳定，也更常作为默认选择。
- 拿不准：先试 L2，或者用 CV 比较 L1/L2 在验证集上的表现。

当然，还有很多别的正则项或者正则方法，都是需要慢慢学习的。

---

<a id="feature-importance"></a>

## Feature Importance

### 为什么要看 Feature Importance？

- Feature Selection：删除不重要的特征，降低维度
- Model Interpretation：理解模型主要依赖哪些特征进行预测

核心认识：

Feature Importance 没有唯一的定义。

不同模型、不同方法，对“重要”的定义不同。

例如：

- Gini importance：这个 feature 帮决策树降低了多少 impurity？
- Permutation importance：破坏这个 feature 后，模型性能下降多少？
- Coefficient importance：标准化后，这个 feature 的系数绝对值有多大？

### 1. Tree-based Feature Importance

决策树的基本过程：

```text
当前节点
↓
尝试不同 feature / threshold 的 split
↓
计算 split 后 impurity 降低了多少
↓
选择 impurity decrease 最大的 split
↓
对子节点继续重复
```

因此决策树是 greedy algorithm：

每一步选“当前最好的 split”，不保证整棵树是全局最优。

#### Gini Impurity

用于衡量一个节点中的类别有多“混乱”。

公式：

$$
Gini = 1 - \sum p_k^2
$$

其中：

pk = 当前节点中第 k 类样本所占的比例

```text
Gini 越小 → 节点越纯
Gini = 0 → 节点中的样本全部属于同一类
```

例：

节点 A 中有 8 个人：

```text
录取：4
不录取：4
```

那么：

```text
p(录取) = 4/8 = 0.5
p(不录取) = 4/8 = 0.5
```

$$
Gini(A) = 1 - (0.5^2 + 0.5^2) = 0.5
$$

现在按照 feature B 进行 split：

```text
        A
       / \
      C   D
```

C：

```text
录取 : 不录取 = 3 : 1
```

D：

```text
录取 : 不录取 = 1 : 3
```

分别计算两个子节点：

$$
Gini(C) = 1 - [(3/4)^2 + (1/4)^2] = 0.375
$$

$$
Gini(D) = 1 - [(1/4)^2 + (3/4)^2] = 0.375
$$

注意：

split 后不能只看某一个子节点，需要计算所有子节点的加权平均 impurity。

```text
Gini_after
= (4/8) × Gini(C)

* (4/8) × Gini(D)

= 0.5 × 0.375 + 0.5 × 0.375
= 0.375
```

因此这次 split 带来的 Gini Gain：

```text
Gini Gain
= Gini_before - Gini_after

= 0.5 - 0.375
= 0.125
```

所以：

```text
父节点 Gini：
Gini(A) = 0.5

子节点自己的 Gini：
Gini(C) = 0.375
Gini(D) = 0.375

split 后整体的 Gini：
Gini_after = 0.375

这个 split 的贡献：
Gini Gain = 0.125
```

### 2. Split 顺序是怎么决定的？

在每一个节点，决策树都会尝试候选 split。

例如：

```text
按 feature A 分：
Gini Gain = 0.12

按 feature B 分：
Gini Gain = 0.30
```

那么选择：

```text
feature B
```

因为它能让 impurity 降得更多。

对于连续特征，还要同时选择 threshold：

```text
age < 20 ?
age < 25 ?
age < 30 ?
...
```

本质上选择：

```text
feature + threshold
```

中 Gini Gain 最大的组合。

因此：

```text
换几个训练样本
↓
各个候选 split 的 Gini Gain 可能改变
↓
split 顺序可能改变
↓
整棵树结构改变
↓
Feature Importance 也可能变化很大
```

这是单棵决策树 Feature Importance 不太稳定的重要原因。

### 3. 一棵决策树的 Feature Importance 怎么算？

![Feature Importance](/assets/images/blog/feature-engineering-gini-importance.png)

某个 feature 的 importance，不只是看它第一次 split 的贡献。

而是：

```text
把这个 feature 在整棵树中所有 split 的 impurity decrease 累积起来。
```

例如：

```text
根节点：
feature A
contribution = 0.30

左边某节点：
feature B
contribution = 0.10

右边某节点：
feature A
contribution = 0.05
```

那么：

```text
Raw Importance(A)
= 0.30 + 0.05
= 0.35

Raw Importance(B)
= 0.10
```

实际计算中还要考虑：这个节点包含多少样本。

因为：

```text
根节点影响大量样本
>
树底部只影响几个样本的小节点
```

因此节点贡献可以理解为：

```text
节点覆盖的样本比例
×
这个 split 降低的 impurity
```

最后把同一 feature 在所有节点上的贡献相加，并进行归一化。

例如：

```text
A 的总贡献 = 0.35
B 的总贡献 = 0.10

总贡献：
0.45
```

归一化后：

```text
Importance(A)
= 0.35 / 0.45
≈ 0.778

Importance(B)
= 0.10 / 0.45
≈ 0.222
```

最终：

```text
A : 0.778
B : 0.222
```

通常所有 feature importance 加起来：

$$
\sum Importance(feature) = 1
$$

一句话：

```text
Decision Tree Feature Importance
= 某个 feature 在整棵树中累计帮助降低了多少 impurity
```

### 4. Random Forest

Random Forest：很多棵带有随机性的 Decision Tree 组合起来。

例如：

```text
Tree 1
Tree 2
Tree 3
...
Tree 100
```

为什么要很多棵树？

```text
单棵树：

训练样本稍微改变
↓
最优 split 可能改变
↓
后续整棵树都可能改变
↓
Feature Importance 不稳定
```

Random Forest 通过建立很多不同的树，降低这种偶然性。

Random Forest 中的随机性主要来自：

1. 每棵树使用随机抽取的训练样本
2. 每次 split 通常只从随机选择的一部分 features 中寻找最佳 split

所以不同树可能长得很不一样。

每棵树都可以得到自己的 importance：

```text
Tree 1:
A = 0.6
B = 0.3
C = 0.1

Tree 2:
A = 0.4
B = 0.5
C = 0.1

Tree 3:
A = 0.5
B = 0.2
C = 0.3
```

Random Forest 再综合这些结果。

例如 A：

```text
Importance(A)
≈ (0.6 + 0.4 + 0.5) / 3
= 0.5
```

因此：

```text
Random Forest Feature Importance
≈ 多棵 Decision Tree Feature Importance 的综合
```

优点：比单棵树更加稳定、robust。

### 5. Gini Importance 的局限

#### 1. 单棵树不稳定

```text
少量数据改变
→ split 顺序改变
→ importance 可能明显改变
```

#### 2. 高度相关的 features 会“抢功劳”

例如：

```text
x1 = 年龄
x2 = 出生年份
```

两者几乎表达相同的信息。

如果树先选择 x1：

```text
x1 importance 很高
x2 importance 可能很低
```

但不能因此认为 x2 本身没有预测信息。

所以：

```text
Feature Importance
≠ feature 本身的绝对价值
```

更准确：

```text
当前模型实际利用这个 feature 的程度
```

### 6. Permutation Importance

核心思想：

```text
打乱某个 feature
↓
破坏它与 target / 其他样本的对应关系
↓
再看模型性能下降多少
```

例如：

```text
原模型 accuracy：
90%

打乱 age 后：
65%
```

说明 age 很重要。

如果：

```text
原模型：
90%

打乱某 feature：
89.8%
```

说明模型几乎不依赖这个 feature。

所以：

```text
Permutation Importance
= 打乱一个 feature 后造成的模型性能下降
```

特点：

- 几乎可以用于任何模型
- 不局限于 Decision Tree
- 直觉比较容易解释

### 7. Coefficient Importance

对于 Linear Regression / Logistic Regression：

```text
y ≈ w1*x1 + w2*x2 + ...
```

如果 features 已经标准化，可以比较：

```text
|w1|, |w2|, ...
```

通常：

```text
|wj| 越大
→ feature j 对模型预测影响越大
```

例如：

```text
y = 0.2*x1 + 3.1*x2 - 0.5*x3
```

标准化后：

```text
|3.1| 最大
```

因此 x2 的影响更大。

注意：如果不同 feature 的尺度不同，不能直接比较 coefficient。

所以通常先进行标准化。

### 最终框架

```text
Feature Importance
│
├── Tree-based
│   └── Gini Importance
│       ├── Gini 衡量节点 impurity
│       ├── split 选择 Gini Gain 最大的方案
│       ├── 累计每个 feature 带来的 impurity decrease
│       └── 得到 feature_importances_
│
├── Random Forest
│   ├── 建很多不同的 Decision Trees
│   └── 综合多棵树的 importance，更稳定
│
├── Permutation Importance
│   └── 打乱 feature，看模型性能下降多少
│
└── Coefficient Importance
    └── 标准化后比较 |coefficient|
```

核心认识：

Feature Importance 没有唯一的定义。

- Gini Importance：这个 feature 帮树降低了多少 impurity？
- Permutation Importance：如果破坏这个 feature，模型会损失多少预测能力？
- Coefficient Importance：在输入尺度可比较的情况下，这个 feature 的 coefficient 有多大？

---

<a id="dimensionality-reduction"></a>

## Dimensionality Reduction

```text
Dimensionality Reduction
│
├── 为什么要降维？
│   └── Curse of Dimensionality
│       ├── Data Sparsity
│       └── Distance Concentration
│
├── 方法 1：Feature Selection
│   └── 保留原来的部分特征
│
└── 方法 2：Feature Extraction / Transformation
    ├── PCA
    │   └── 保留尽可能多的 variance
    │
    ├── LDA
    │   └── 让不同 class 尽可能分开
    │
    └── t-SNE
        └── 保留局部邻域结构，用于 2D / 3D 可视化
```

### 广义上

Feature Selection确实属于：Dimensionality Reduction

因为：

```text
100 features → 20 features
维度降低了。
```

但机器学习里经常会把它们区分为：

```text
Feature Selection
    保留原 feature

Feature Extraction
    创造新的 feature
```

### Dimensionality Reduction

High dimensionality problems:

#### 1. Data sparsity

```text
dimension ↑
→ feature space grows extremely fast
→ fixed amount of data becomes sparse
→ generalization becomes harder
```

#### 2. Distance concentration

```text
dimension ↑
→ pairwise distances become increasingly similar
→ "nearest" neighbor becomes less meaningful
→ hurts KNN / clustering / distance-based methods
```

Two ways to reduce dimensions:

#### 1. Feature Selection

Keep a subset of original features.

#### 2. Feature Extraction

Transform original features into fewer new features.

#### PCA

```text
unsupervised
linear transformation
maximize preserved variance
```

#### LDA

```text
supervised
linear transformation
maximize separation between classes
```

#### t-SNE

```text
unsupervised
nonlinear
preserve local neighborhood structure
mainly used for 2D/3D visualization
```

---

<a id="pca"></a>

## PCA（Principal Component Analysis）

```text
PCA
│
├── 1. 为什么要 PCA
│   └── 高维 → 冗余、稀疏、距离失效
│
├── 2. PCA 到底想找什么
│   └── 找“数据变化最大”的方向
│
├── 3. 怎么找这些方向
│   ├── 数据中心化
│   ├── 协方差矩阵
│   ├── 求特征值 / 特征向量
│   └── 按特征值大小排序
│
├── 4. 怎么降维
│   └── 把数据投影到前 k 个主成分
│
├── 5. 怎么判断保留几个主成分
│   └── explained variance
│
└── 6. PCA 能干什么
    ├── 降维
    ├── 可视化
    ├── 去冗余
    ├── 作为模型输入
    └── 图像压缩
```

具体的算法推导我大致理解了，但是感觉自己还没能完全独立推导出来，很多数学细节我不是很熟悉，所以对于我的理解/推导起到了一些阻碍作用。后续可能会补充算法具体推导。

### 总体

PCA = 寻找数据方差最大的正交方向。

eigenvector 决定方向，eigenvalue 表示该方向能解释多少 variance。

降维就是把数据投影到前几个 principal components，并丢掉低方差方向。

更几何化的版本：

PCA 本质上是在找一个更适合数据的坐标系，然后只保留最重要的坐标轴。

### AI 版，自己还没推

现在是每一行一个样本。

#### PCA

Why:

```text
Reduce dimensionality while preserving important variation.
```

Core idea:

```text
PCA finds orthogonal directions with maximum variance.
```

Geometric view:

```text
Find a better coordinate system for the data,
then discard less important axes.
```

Algorithm（each row is one sample）：

Input:

$$
X \in R^{n \times d}
$$

#### 1. Center

$$
X_c = X - mean(X)
$$

#### 2. Covariance matrix

$$
\Sigma = \frac{1}{n-1}X_c^T X_c
$$

#### 3. Eigendecomposition

$$
\Sigma v_i = \lambda_i v_i
$$

```text
vi → principal direction
λi → variance along vi
```

#### 4. Sort

$$
\lambda_1 \ge \lambda_2 \ge ... \ge \lambda_d
$$

#### 5. Select first k eigenvectors

$$
W = [v_1, ..., v_k]
$$

$$
W \in R^{d \times k}
$$

#### 6. Project

$$
Z = X_c W
$$

$$
Z \in R^{n \times k}
$$

#### Explained variance

$$
\frac{\lambda_i}{\sum \lambda_j}
$$

Choose k according to cumulative explained variance.

#### Key distinction

```text
Feature Selection:
    choose original features

PCA:
    construct new features as linear combinations
    of original features
```

#### Limitations

- linear
- unsupervised
- ignores target labels
- lower interpretability

---

<a id="lda"></a>

## LDA

最后一节是LDA，先不学了，大脑要过载了。

ChatGPT：[https://chatgpt.com/s/t_6aad05c153508191a48f145438601d99](https://chatgpt.com/s/t_6aad05c153508191a48f145438601d99)
