# 报童问题newsboy、newsvendor problem

## CASE：报摊每天都卖人民日报，需要决策向供应商拿多少份报纸？报纸拿多了（采购过多），造成积压（积压损失，第二天报纸不值钱），拿少了（采购过少），有顾客却没报纸，浪费了盈利机会（缺货损失）


## 分析：

设**决策变量**为$Q$，报纸实际需求为$D$（不确定的，属于**随机变量**），报纸售价a元，采购成本b元，退货成本c元，设利润为$R$（**目标函数**），则每份报纸赚$a-b$元，积压一份亏$b-c$元，有两种情况——

1）当$Q>D$，即采购过多，则利润$R=(a-b)*D+(b-c)*(Q-D)$

2）当$Q \le D$，即缺货，则利润$R=(a-b)*Q$

求解：总利润Z受决策变量$Q$与需求$D$的影响，有$R=R(Q,D)$，因需求$D$为随机变量，**则求Z最大值等价于求Z的数学期望$E(Z)$最大——**

设$G(Q)=R(Z)$，$p(D)$是需求$D$的离散概率，有

$$G(Q)=\sum_{D=1}^Q [(a-b)D+(c-b)(Q-D)]p(D) +\sum_{D=Q+1}^\infty (a-b)Qp(D)$$

## 问题：$G(Q)$如何求最大值，如何求导？函数$G(Q)$连续么？

## 概率知识回顾：

* $分布函数F(x)，概率密度函数f(x)，有F'(x)=f(x)$，$F(x)=\int_{-\infty}^x f(t) dt$
* 变上限积分求导：$[\int_{-\infty}^x H(t) dt]'=H(x)$
* $0 \le F(x) \le 1，F(\infty)=1，\int_{-\infty}^\infty f(x) dx=1，f(x) \ge 0$
* 数学期望$E(x)=\int_{-\infty}^\infty xf(x) dx$
* 若$y=g(x)，则E(y)=E(g(x))=\int_{-\infty}^\infty g(x)f(x) dx$

## 问题转换:

设$Q、D$为连续变量，$a、b、c$转化为**缺货成本$C_u$与积压成本$C_o$**，**决策变量**为$Q$，需求为$D$（**随机变量**），**成本**为$Z=Z(Q,D)$，现求最优解$Q^*$，使得$G(Q^*)=E(Z)$取**最小值**，则1）当$Q>D$，$Z=C_o(Q-D)$；2）当$Q \le D$，$Z=C_u(D-Q)$，有

$$G(Q)=E(Z)=E(Z(D))=\int_{-\infty}^\infty Zf(D) dD \\ 
=C_o\int_{-\infty}^Q (Q-D)f(D) dD + C_u\int_Q^\infty (D-Q)f(D) dD \\ 
=C_o\int_{-\infty}^Q (Q-x)f(x) dx + C_u\int_Q^\infty (x-Q)f(x) dx \\
=C_o \int_0^Q (Q-x)f(x) dx + C_u\int_Q^\infty (x-Q)f(x) dx$$

$$G(Q)=C_o Q \int_0^Q f(x) dx - C_o \int_0^Q xf(x) dx + C_u \int_Q^\infty xf(x) dx - C_u Q \int_Q^\infty f(x) dx $$

$$ \frac {\partial G}{\partial Q} = C_o Qf(Q) + C_o \int_0^Q f(x) dx - C_o Qf(Q) - C_u Qf(Q) +  C_u Qf(Q) -  C_u \int_Q^\infty f(x) dx \\
= C_o \int_0^Q f(x) dx - C_u \int_Q^\infty f(x) dx \\
= C_o \int_{-\infty}^Q f(x) dx - C_u \int_Q^\infty f(x) dx $$

$$ \frac {\partial ^2G}{\partial Q^2} = C_o f(Q) + C_u F(Q) \ge 0 $$
### 故有最优解$Q^*$，使$G(Q^*)$即$E(Z(Q^*,D))$取最小值

### 令$ \frac {\partial G}{\partial Q} = 0$，有

$$ \frac {\partial G}{\partial Q} = C_o F(Q) + C_u (1-F(Q)) \\
= (C_o + C_u)F(Q) - C_u = 0 $$

$$ F(Q^*) = \frac {C_u}{C_0 + C_u}$$

**需要根据需求$D$的分布函数$F(x)$，如正态分布、均匀分布、泊松分布等，反查分布函数求解$Q^*$值** 

## 思考：
1. 上述求解方法，属于什么思路？如何通过软件工具求解？
2. 能否通过excel求解？
3. 能否进行仿真实验？如何实现？


