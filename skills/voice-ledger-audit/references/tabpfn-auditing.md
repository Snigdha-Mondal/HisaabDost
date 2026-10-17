# TabPFN Tabular Foundation Model Auditing Reference

This document outlines the tabular anomaly detection principles and mathematical foundations used by HisaabDost to identify wholesale price gouging.

---

## 1. Why TabPFN for Street Vendors?

Traditional anomaly detection methods (e.g. Isolation Forest, One-Class SVM, or static thresholding) fail in micro-retail scenarios because:
1. **Tiny Data Regimes**: A stall owner only buys 1 to 3 times a week per commodity, giving only 10–30 data points per month.
2. **Seasonal Variance**: Festival periods (Diwali, Eid, weddings) cause supply crunches that distort linear standard deviations.
3. **No Retraining Overhead**: TabPFN (Prior Labs) is a Transformer pre-trained on synthetic tabular tasks. It operates purely *in-context*, computing Bayesian predictive posteriors directly on a small prompt table without hyperparameter tuning or gradient steps.

---

## 2. In-Context Anomaly Scoring

Given a 30-day historical series of purchases for commodity $c$:
$$\mathcal{D}_c = \{(t_i, q_i, p_i, u_i)\}_{i=1}^N$$
where $t_i$ is transaction date, $q_i$ is quantity, $p_i$ is total amount, and $u_i = p_i / q_i$ is unit price.

### A. Baseline Statistics
- Baseline Mean: $\mu_{\text{baseline}} = \frac{1}{N} \sum_{i=1}^N u_i$
- Baseline Dispersion / StDev: $\sigma_{\text{baseline}} = \sqrt{\frac{1}{N-1} \sum_{i=1}^N (u_i - \mu_{\text{baseline}})^2}$

### B. Deviation Ratio
$$\Delta_{\text{rel}} = \frac{u_{\text{today}} - \mu_{\text{baseline}}}{\mu_{\text{baseline}}}$$

### C. Anomaly Decision Rule
An expense is classified as a price-gouging alert if:
$$\Delta_{\text{rel}} > 0.08 \quad (\text{8\% above recent mean})$$

The severity level is assigned as follows:
- $\Delta_{\text{rel}} \in (0.08, 0.15]$: **Moderate Warning** (Market fluctuation or supplier creep)
- $\Delta_{\text{rel}} > 0.15$: **Critical Gouging Alert** (High risk of wholesale exploitation)

---

## 3. Penny-Precise Rupee Loss Calculation

To give the vendor an exact, non-hallucinated number for negotiation:

$$\text{Overcharge Rate} = \max\left(0, \text{round}(u_{\text{today}} - \mu_{\text{baseline}}, 2)\right)$$
$$\text{Extra Rupee Cost} = \text{round}\left(\text{Overcharge Rate} \times q_{\text{today}}, 2\right)$$

### Example:
- **Commodity**: Cooking Oil (*Refined Tel*)
- **Baseline Average**: ₹130.00 / Liter
- **Today's Purchase**: 15 Liters @ ₹2,250 (Unit Price = ₹150.00 / Liter)
- **Deviation**: $+15.38\%$
- **Overcharge Rate**: ₹20.00 / Liter
- **Total Extra Cost**: ₹20.00 $\times$ 15 = ₹300.00
- **Spoken Advice**: *"Chacha, aaj refined tel 150 rupaye liter mila jabki pichle mahine 130 rupaye tha. Aapne lagbhag 300 rupaye zyada diye hain. Kal Mandi ke dusre dukaan se rate zaroor check karna."*
