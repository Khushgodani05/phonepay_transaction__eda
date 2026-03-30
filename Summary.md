# ⚡ PhonePe Pulse — EDA Summary
> **Project Type:** Exploratory Data Analysis | **Domain:** Digital Payments & FinTech

---

## 🗂️ Dataset at a Glance

| Table | Rows | Columns | What It Covers |
|---|---|---|---|
| `aggregate_insurance` | 701 | 9 | Insurance policy counts & amounts by state/year/quarter |
| `aggregate_transaction` | 5,174 | 9 | Payment instrument breakdown across all geographies |
| `aggregate_users` | 7,326 | 8 | App opens & device brand usage data |

**Source:** PhonePe Pulse GitHub → ETL pipeline → MySQL (`phonepay` DB)

---

## 🎯 Business Objectives

- **Geo Insights** — Map payment trends at state & district level
- **Payment Performance** — Rank payment categories by popularity & value
- **User Engagement** — Track app activity to fuel retention strategy
- **Insurance Intelligence** — Decode insurance transaction patterns
- **Trend Analysis** — Spot time-based fluctuations in volume & value

---

## 📊 Key Insights — Chart by Chart

### 1. Transaction Count Distribution *(Histogram + KDE)*
- **Heavily right-skewed** — a small elite of states/quarters drive the bulk of transactions
- Long tail = massive untapped markets sitting idle
- 🎯 *Focus budgets on the high-volume tail; run awareness campaigns for the rest*

### 2. Transaction Type Frequency *(Horizontal Bar)*
- **Peer-to-peer payments dominate** by record count
- Niche types show low awareness or friction in UX
- 🎯 *Reward top types with cashback; fix UX on low-frequency types*

### 3. Records Per Year *(Bar Chart)*
- **YoY growth is real and consistent**
- 2020 shows a visible COVID-dip in record counts
- 🎯 *Sustained growth = invest more; any plateau = explore new verticals*

### 4. Insurance Amount Distribution *(Box Plot)*
- **Median is low; outliers are wild** — a tiny premium segment balloons the mean
- Majority are micro-policies with thin margins
- 🎯 *Nurture high-value outliers; rebalance product mix away from micro-only*

### 5. Top 10 Device Brands *(Bar Chart)*
- **Samsung & Xiaomi are kings** — India's mid-range Android dominance on full display
- OnePlus/iPhone = small but high-ARPU premium segment
- 🎯 *Optimise app for top Android brands; don't ignore premium segment revenue*

### 6. Total Transaction Amount Per Year *(Bar Chart)*
- **GMV on a rocket** — strong upward trajectory, post-2020 COVID-acceleration
- More users + higher ticket sizes = compounding growth
- 🎯 *Growing GMV = strong merchant partnership pitch; scale fraud systems proportionally*

### 7. Average Amount by Payment Type *(Horizontal Bar)*
- **Merchant payments > P2P** by average ticket size
- Recharge/bills are high-frequency but low-value
- 🎯 *Monetise high-ticket categories; don't over-invest in volume-only categories*

### 8. Insurance Count by Quarter *(Bar Chart)*
- **Q1 spikes** — tax-saving deadline rush before India's March 31 financial year-end
- Q3 dips suggest monsoon-season disengagement
- 🎯 *Front-load insurance campaigns to Q4 to catch pre-deadline buyers*

### 9. App Opens: Country vs State Level *(Box Plot)*
- **Maharashtra & Karnataka pull the national average up**
- Wide IQR at state level = massive engagement inequality between states
- 🎯 *Test new features in high-engagement states; run targeted onboarding in low ones*

### 10. Insurance Count vs Amount *(Scatter Plot)*
- **Positive correlation** — higher policy counts = higher premium totals
- Outliers: high-amount, low-count = corporate/term insurance deals
- 🎯 *Top-right states are prime cross-sell targets; bottom-right need premium upselling*

### 11. Device Users vs App Opens *(Regression Plot)*
- **More device users → more app opens** (positive slope, high variance)
- Device brand alone doesn't fully predict engagement
- 🎯 *Partner with top OEMs for pre-installation; investigate "installed but inactive" users*

### 12. Transaction Type Share by Quarter *(Stacked 100% Bar)*
- P2P shrinks proportionally in Q4 while merchant payments grow → **festive season effect**
- Stable mix in non-festive quarters = habitual user behaviour
- 🎯 *Festive quarter = merchant fee revenue opportunity; diversify mix year-round*

### 13. Top 10 States by Transaction Count *(Horizontal Bar)*
- **Maharashtra, Karnataka, Telangana** lead the pack — urban, tech-savvy populations
- North-eastern states are underrepresented despite growth potential
- 🎯 *Premium features first in top states; vernacular UI to unlock the rest*

### 14. Insurance Market Share *(Pie Chart)*
- **One type dominates (TOTAL)** — limited product diversity
- Near-monopoly = single point of failure risk
- 🎯 *Bundle dominant product for retention; diversify insurance catalogue urgently*

### 15. Transaction Amount — Year × Quarter *(Grouped Bar)*
- **Q4 consistently peaks** — festive season Diwali/New Year spending
- YoY Q1 growth confirms strong new-year user activation
- 🎯 *Launch campaigns end-Q3 to ride the Q4 wave*

### 16. Top 15 States × Year Heatmap
- **Dark cells in recent years** confirm accelerating digital adoption
- Consistently light-celled states = structural barriers (connectivity, literacy)
- 🎯 *Replicate winning playbooks; partner with telecoms in laggard states*

### 17. Quarter-wise Trend by Year *(Multi-line)*
- **All years trending up** — network effects compounding
- Q2 dips across multiple years = academic-year slowdown pattern
- 🎯 *Narrowing YoY gap = watch for growth deceleration; activate new user strategies*

### 18. Insurance Trend — Top 5 States *(Line Chart)*
- **Maharashtra & Karnataka steepest climb** — financial literacy + disposable income
- Flat-line states have hit saturation
- 🎯 *Partner with LIC/HDFC Life in growth states; launch health micro-insurance in flat ones*

### 19. App Opens by Device Brand — Year *(Grouped Bar)*
- Samsung/Xiaomi hold the fort; **Vivo/Oppo rising fast** = new demographics entering
- Share dynamics shifting toward budget-tier newer OEMs
- 🎯 *Pre-installation deals with rising OEMs = first-mover advantage at device purchase*

### 20. Correlation Matrix *(Heatmap)*
- **Count ↔ Amount: high correlation (>0.7)** — volume markets are also value markets
- One segmentation strategy can hit both KPIs simultaneously
- 🎯 *Target for volume = target for value; no need to split campaigns*

### 21. Faceted Bar — Top 4 States by Quarter
- **Q1 spikes in most states** = tax-saving insurance intent is universal
- States with flat distributions have organic, non-seasonal demand
- 🎯 *Push Section 80C educational content in-app for states with no Q1 spike*

### 22. Transaction Amount by Quarter *(Violin Plot)*
- **Q4 violins are widest** — more extreme high-value transactions in festive season
- Q2 thin violins = consistent but small-ticket behaviour
- 🎯 *Premium product promos belong in Q4; mid-year needs targeted value campaigns*

### 23. State Bubble Chart — Count vs Amount
- **"Star" markets** (top-right, large bubble): Maharashtra, Karnataka → premium products first
- **"Volume-Heavy" markets** (large bubble, low Y): high ops cost, low revenue return
- 🎯 *Stars get PhonePe loans/mutual funds/IPO access first; volume-heavy need monetisation rethink*

---

## 💡 Business Recommendations (TL;DR)

| Priority | Action |
|---|---|
| 🔥 **Immediate** | Double down on Maharashtra, Karnataka, Telangana with premium product rollouts |
| 🔥 **Immediate** | Launch festive Q4 campaigns end-Q3 — the data says the wave is real |
| ⚡ **Short-term** | OEM pre-installation partnerships with Xiaomi, Vivo, Oppo |
| ⚡ **Short-term** | Vernacular UI to unlock North-eastern & low-engagement states |
| 📅 **Medium-term** | Diversify insurance product catalogue beyond the single dominant type |
| 📅 **Medium-term** | In-app Section 80C education to convert Q2/Q3 flatliners into Q1 buyers |
| 🔭 **Long-term** | Telecom partnerships in structurally underserved states |
| 🔭 **Long-term** | Scale fraud detection & infra proportionally to GMV growth |

---

## ✅ Conclusion

PhonePe's data tells one clear story: **a platform firing on all cylinders with pockets of gold still unmined.** Transaction volume and value are both climbing. A handful of states carry the weight, Samsung and Xiaomi own the hardware, and festive quarters are where the real money moves. The opportunity is in the edges — untapped states, rising OEM demographics, diversified insurance products, and mid-year engagement tactics. Fix those, and the growth story writes itself.

---
*EDA by: Individual Contributor | Dataset: PhonePe Pulse (Aggregated) | Stack: Python · Pandas · Seaborn · Matplotlib · MySQL*v