# Task 3: Event Impact Modeling Methodology

## Objective
To model the quantitative relationships between transformation events (policies, product launches, infrastructure) and financial inclusion indicators (Access and Usage).

## 1. Event-Indicator Association Matrix
We represent event impacts as "shifters" on the baseline growth rate.
- **High Impact**: +5.0 percentage points (pp) potential.
- **Medium Impact**: +2.0 pp potential.
- **Low Impact**: +1.0 pp potential.

| Event | Indicator | Baseline Magnitude | Net-New Factor |
|---|---|---|---|
| Telebirr Launch | `ACC_OWNERSHIP` | 5.0 pp | 0.6 (due to multi-banking) |
| Telebirr Launch | `USG_DIGITAL_PAY` | 5.0 pp | 1.0 (primary driver) |
| M-Pesa entry | `ACC_OWNERSHIP` | 2.0 pp | 0.5 (high overlap with Telebirr) |
| Fayda Digital ID | `ACC_OWNERSHIP` | 5.0 pp | 0.8 (KYC enabler) |

## 2. Functional Form: The S-Curve (Logistic)
Events do not have immediate full impact. We use a logistic build-up function:
$$Impact(t) = \frac{L}{1 + e^{-k(t-x_0)}}$$
- **L**: Maximum impact magnitude (from matrix).
- **k**: Growth rate (0.2 - 0.5 depending on event speed).
- **x0**: Midpoint months (lag).

## 3. Validation: Telebirr (2021-2024)
- **Predicted**: ~4.99 pp gross impact.
- **Observed**: +3.0 pp net growth in survey data.
- **Conclusion**: The "Slowdown Paradox" identified in Task 2 is accounted for by applying a **0.6 Discount Factor** to raw impact weights for Access indicators. Usage indicators (Digital Payments) do not show this same stagnation and retain higher weights.

## 4. Assumptions & Limitations
- **Additivity**: We assume multiple event impacts are additive, which may overstate growth if market saturation is reached.
- **Lag Uncertainty**: Midpoint months (x0) are estimated based on literature (e.g., Kenya M-Pesa adoption speed).
- **Data Frequency**: The lack of annual Findex data makes it difficult to pinpoint the exact 'build-up' phase of recent events.
