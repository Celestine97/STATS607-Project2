## Simulation Design (ADEMP Framework)

### Aims
Compare power of BH procedure against FWER-controlling methods like Bonferroni and Hochberg(1988), and verify FDR control.

#### Hypothesis to be tested
- **null hypothesis** data follows N(0, 1)
- **alternative hypothesis** data follows N($\mu$, 1), where $\mu \neq 0$.

---

### Data-Generating Mechanisms
- **m** (total number of hypotheses) = 4, 8, 16, 32, 64
- **m₀/m** (percentage of true null hypotheses) = 0%, 25%, 50%, 75%
- **data generation** for data satisfy the true nul hypothesis, generate $x \sim N(0, 1)$; otherwise, generate $x \sim N(\mu, 1)$, where $\mu = \frac{L}{4}, \frac{L}{2}, \frac{3L}{4}, L$. These four groups of non-zero expectations are place in the following three ways:
    1. lnearly decreasing (D) number of hypotheses away from 0 in each group;
    2. equal (E) number of hypotheses in each group;
    3. linearly increasing (I) number of hypotheses away from 0 in each group.
- **L** (signal strength) = 5(by default), 10 
- **variance reduction**
    1. **Common Random Numbers**: Same base random data used across all configurations with same m
    2. **Monotonically Related Alternatives**: Alternative means are sorted to create positive correlation

---

### Estimands
- Power: Proportion of false nulls correctly rejected
- FDR control: Proportion of false discoveries

---

### Methods
We compare three multiple testing correction procedures:

#### 1. Bonferroni Correction
**Type**: Single-step procedure  
**Controls**: Familywise Error Rate (FWER) at level $\alpha$ (by default, $\alpha = 0.05$)

**Procedure**:
Given m hypothesis tests with p-values $p_1, p_2, ..., p_m$
- Compare each p-value to the adjusted threshold $\frac{\alpha}{m}$
- Reject hypothesis $H_i$ if  $p_i \leq \frac{\alpha}{m}$

#### 2. Hochberg's Procedure (1988)
**Type**: Step-down procedure  
**Controls**: Familywise Error Rate (FWER) at level  $\alpha$

**Procedure**:
Given m hypothesis tests with ordered p-values $p_{(1)}, p_{(2)}, ..., p_{(m)}$:

1. Start with the largest p-value $p_{(m)}$
2. Find the largest index i for which $p_{(i)} \leq \frac{\alpha}{m+1-i}$
3. If such i exists, reject all $H_{(1)}, H_{(2)}, ..., H_{(i)}$ (ordered)
4. Otherwise, reject none

#### 3. Benjamini-Hochberg (BH) Procedure
**Type**: Step-up procedure  
**Controls**: False Discovery Rate (FDR) at level $q$, in this simulation, we take $q = \alpha$ as the paper suggested

**Procedure**:
Given m hypothesis tests with ordered p-values $p_{(1)}, p_{(2)}, ..., p_{(m)}$:

1. Start with the smallest p-value $p_{(1)}$
2. Find the largest index k for which: $$p_{(k)} \leq \frac{k}{m} \times q$$
3. If such k exists, reject all H₍₁₎, H₍₂₎, ..., H₍ₖ₎
4. Otherwise, reject none
---


### Performance Measures
- Average power across replications (the measure used in the paper)
- Empirical FDR (diagositic plot)
- Power gain (BH/Bonferroni) (diagositic plot)


## Simulation Design Matrix

### Design Table

The simulation explores 60 configurations defined by the full factorial combination of:

| Factor | Levels | Description |
|--------|--------|-------------|
| **m** | 5 | Number of hypotheses: {4, 8, 16, 32, 64} |
| **Null proportion** | 4 | Proportion of true nulls: {0%, 25%, 50%, 75%} |
| **Distribution** | 3 | Alternative signal distribution: {D, E, I} |

**Total configurations**: $5 \times 4 \times 3 = 60$

**Replications per configuration**: $n_{rep} = 20,000$ (follow the setting in the paper)


---

### Additional Illustration on Alternative Signal Distribution Patterns

The $m_1$ alternative hypotheses have means distributed across four signal strength levels: $\{\frac{L}{4}, \frac{L}{2}, \frac{3L}{4}, L\}$.

The count at each level differs by distribution type:

| Distribution | Level 1 ($\frac{L}{4}$) | Level 2 ($\frac{L}{2}$) | Level 3 ($\frac{3L}{4}$) | Level 4 ($L$) | 
|--------------|----------|----------|----------|----------|
| **D** (Decreasing) | 40% | 30% | 20% | 10% | 
| **E** (Equal) | 25% | 25% | 25% | 25% | 
| **I** (Increasing) | 10% | 20% | 30% | 40% |


*Note: Means are sorted in ascending order to ensure monotonic relationship across distributions*

---

## Description for Reproducing the Simulation 

### Data Generating Process
1. Generate Base Random Data
    For each $m$, generate once:
    $$\mathbf{\varepsilon}^{(m)} = \{\varepsilon_{r,i}\}_{r=1,\ldots,20000}^{i=1,\ldots,m} \quad \text{where} \quad \varepsilon_{r,i} \sim N(0, 1)$$
2. Specify Null and Alternative Hypotheses
3. Generate Mean Vector $\boldsymbol{\mu} = (\mu_1, \mu_2, \ldots, \mu_m)^\top$
4. Generate Data for Replication $r$
    $$\mathbf{X}_r = \boldsymbol{\mu} + \boldsymbol{\varepsilon}_r$$

### Statistical Analysis
1. Compute Test Statistics and P-values
2. Apply Multiple Testing Procedures
3. Compute Performance Metrics

### Visualization