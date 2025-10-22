## Reproduction Results
In this project, I chose to reproduce the Figure1 in the paper. The overall trend looks similar: BH procedure performs better, the other two methods sometimes produce very similar power control; as the distribution of the alternative means changes from decreasing to increasing(i.e. more alternative means are away from 0), all the methods showed an improvement.

The paper mentioned that they picked the signal strength(parameterized by $L$) at two levels, 5 and 10, but did not specify which one they used. According to the original figure, I supposed they pick $L=5$. Under this setting, the major difference is when the total number of hypotheses is small, e.g., $m=4$ or $m=8$, the average power is lower than that in the original figure. Thus, the figure I reproduced does not consistently show a monotone decreasing power through all the configurations.

This situation mainly appears in the decreasing configuration of the alternative means, while not that apparent in equal or increasing case. In the decreasing configuration, the alternatives are more similar to the null hypothesis, along with the fact that such small $m$ might not be a good setting for multiple testing, leading to this difference. If we set a higher signal strength $L = 10$, all the methods perform better, and there is no such sharp drops in the lines.

Additionally, the paper states "m independent normally distributed random variables" tested by "z-tests" but doesn't specify:
- Single observations (current implementation)
- Sample means
which could also lead to the difference.

---

## The Original Simulation Design

The original study took multiple scenarios for alternative mean distributions, different choices of hypotheses and enough replications, which are the good aspects. However, I think the following 2 facts could make the simulation unfair.
**1. Different Error Rates**

The methods actually control different quantities:

| Method | Controls |
|--------|----------|
| Bonferroni, Hochberg | $\text{FWER} = P(V \geq 1) ≤ \alpha$, probability of any false rejection |
| BH | $\text{FDR} = \mathbb{E}(V/R) ≤ q^{*}$ ,expected proportion of false discoveries |

When $m_0\text{true nulls} < m$, FDR < FWER by construction, and in this simulation setting, they chose $\alpha = q^{*}$. Thus, BH is natually allowed to make more rejections than FWER methods. Thus, BH will be more likely to gain more power.

**2. Independence Assumption**
In the proof of BH's theoretical guarantee, they assumed the p-values are independent. In the simulation design, they also kept this independence setting. However, FWER methods (Bonferroni, Hochberg) become too conservative under independence, which definitely favors BH procedure.

Besides, this simple setting does not align with most real applications, where dependence across the data is very common.

---

## Possible Changes of the Simulation

**1. More fair comparison**
- Set $q^{*} = \frac{m_0}{m} \alpha$, then compare the power
- Compare all methods at levels chosen to achieve the same empirical FDR
- Compare both FDR and power

**2. More complext data structure**
- Introduce data dependence
- Introduce more distributions, or mixed distributions

---

## Visualizations

This project created some additional plots than the original:

1. Heatmap of power gain - Shows where BH advantage is largest
2. FDR diagnostic plot - Verifies actual FDR control
3. Power curves (reproduction)

In the FDR diagnostic plot, we can interpret that all methods achieved excellent FDR control, and the two FWER actually all got lower FDR than BH method.

---

## Unexpected Results

1. Sharp drop at m=8 in the reproduction plot: possibly a mean allocation issue?

2. FDR control: actually all the methods controls FDR, the two FWER methods control well below the target level.

---

## Challeging Parts
I think it is applying the variace reduction trick in data generation. At first I did not notice this trick (although I guess it is commonly used), and I just generate iid data for every configuration and drafted all the simulation code. Afterwards I realized that the generation mechanism was not correct, and it took me a while to completely rebuild the data generation and simulation structure. Other parts were relatively straight forward.

I think I am moderately confident of the results, because I checked the methods many times. However, there are some differences in the reproduction plot compared to the figure in the paper.