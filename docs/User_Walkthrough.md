# SAS Viya 4 AML Demo: High-Fidelity Walkthrough Guide

This guide provides a professional "script and screen" walkthrough for the **Multi-Layered Shield** AML demonstration.

---

## 🎭 Scenario Setup
**Presenter Persona**: Senior Compliance Strategist.
**The Story**: We are investigating a sudden surge in suspicious transactional "velocity" across our retail portfolio.

---

## 📍 Phase 1: Interactive Discovery (Visual Analytics)
*Goal: Identify the 'High-Risk Student' anomaly.*

1. **Dashboard Home**: Open the **AML Compliance Command Center**.
2. **The Funnel (Visual Cue)**: Point to the **Stage-by-Stage Funnel Chart**.
   - **Talk Track**: *"Notice our 'Multi-Layered Shield' in action. Out of 100,000 transactions, Stage 1 exclusions instantly removed 2,000 entities we trust, like government payrolls, freeing up our analysts for real threats."*
3. **The Deep Dive**:
   - **Click**: On the **Profession** list filter, select **'Student'**.
   - **Visual Outcome**: The network diagram and line charts will filter instantly.
   - **Talk Track**: *"Look at this specific cluster. We have a student moving $500,000 USD in a single week. To our old rules engine, this might just look like a high-value transaction. To our Multi-Layered Shield, it's a red flag."*
4. **Counterparty Risk**: Hover over the counterparty link in the **Network Diagram**.
   - **Visual Cue**: See the connection to "Oligarch Holdings".
   - **Talk Track**: *"By Stage 4, our system has already flagged the counterparty as a known high-risk entity in a sanctioned jurisdiction."*

---

## 🔬 Phase 2: AI-Driven Investigation (Model Studio)
*Goal: Show why the AI (Challenger) caught what the Heuristics (Champion) missed.*

1. **The Pipeline**: Switch to **SAS Model Studio** -> Pipeline tab.
2. **Comparison (Visual Cue)**: Point to the **Model Comparison** node results.
   - **Talk Track**: *"While our standard Logistic Regression caught the obvious outliers, our XGBoost Challenger detected the 'Smurfing' pattern—small deposits that stay just below the regulatory $10k limit but total to massive sums."*
3. **Interpretability**: Click on the **XGBoost** node -> **Results** -> **Variable Importance**.
   - **Visual Outcome**: `Turnover_Ratio` and `Velocity_7D` are at the top.
   - **Talk Track**: *"The system isn't a black box. It tells us clearly: this alert was triggered primarily because the income doesn't match the profession."*

---

## 🛡️ Phase 3: The Multi-Layered Shield (Intelligent Decisioning)
*Goal: Explain the orchestration logic.*

1. **The Decision Flow**: Open **AML_Shield_Orchestration** in **SAS Intelligent Decisioning**.
2. **Stage 4 Detail**: Click on the **Lookup node** for `aml_country_risk`.
   - **Visual Cue**: Table showing 'North Korea (KP)' with a risk score of 98.
   - **Talk Track**: *"In Stage 4, we apply a high-risk jurisdiction multiplier. Because this transaction involved a connection to North Korea, the Global Alert Value was pushed into the 'URGENT' category automatically."*
3. **Decision Outcome**: Show the final **Rule Set** node.
   - **Talk Track**: *"Finally, in Stage 5, we assign a priority. This student didn't just get an alert; they got an URGENT priority, ensuring they are at the top of the analyst's queue this morning."*

---

## 🏁 Phase 4: Final Disposition
*Goal: File the SAR (Suspicious Activity Report).*

1. **Return to VA**: Open the **Alert Triage** tab in the dashboard.
2. **Disposition**: Click the "Urgent" row for the Student customer.
   - **Talk Track**: *"With the model's evidence, the PEP match, and the velocity data, we have a complete audit trail. We can now submit this SAR with 100% confidence, backed by SAS Viya's integrated intelligence."*

---
## 💡 Top 3 Takeaways for the Audience
1. **Reduce Noise**: Stage 1 Exclusions save thousands of analyst hours.
2. **See the Unseen**: AI Challengers find complex patterns (Smurfing/Velocity) that rules miss.
3. **Unified Platform**: We moved from raw data to a filed SAR in one integrated environment.
