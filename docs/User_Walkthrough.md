# SAS Viya 4 AML Demo: User Walkthrough Guide

Welcome to the **End-to-End AML Intelligence** demo. This guide is designed for users who wish to explore how SAS Viya 4 solves complex financial crime challenges using a **Multi-Layered Shield** decisioning architecture.

## Scenario: Professional Compliance Lifecycle
In this demo, we follow the story of a **Compliance Officer** managing a regional portfolio during a period of high volatility.

---

### Phase 1: Interactive Discovery (Visual Analytics)
*Goal: Detect anomalies at the speed of business.*

1. **Dashboard Home**: Open the "AML Investigator Portal" in **SAS Visual Analytics**.
2. **The 5-Stage Overview**: Look at the "Alert Funnel". 
   - Observe how 100,000 transactions were processed.
   - Stage 1 (Exclusions) removed 2,000 "Trusted" transactions.
   - Stage 5 (Orchestration) narrowed down 50 "URGENT" alerts from a pool of 1,000 potential risks.
3. **The 'Occupation Mismatch' Alert**: Filter by **Profession = 'Student'**.
   - *Anomaly*: You will see a "Student" with a **Turnover Ratio > 20**.
   - *Insight*: This student has moved over $500,000 USD in a single week—a clear indicator of "mule" activity.
4. **Network Visualization**: Select this customer. The network diagram instantly shows their connections to **Oligarch Holdings** (Stage 4 PEP/Country Risk Match).

---

### Phase 2: AI-Driven Investigation (Model Studio)
*Goal: Compare the Human Rule vs. the AI Model.*

1. **The 'Champion vs Challenger' View**: Switch to **SAS Model Studio**.
2. **The Battle of Models**:
   - **Logistic Regression (Champion)**: Show how it caught the standard cases.
   - **XGBoost (Challenger)**: Show how this model caught the **"Rapid Velocity"** patterns (Stage 2 Features) that the regression missed. 
3. **Interpretability**: Use the **LIME/Feature Importance** plots to show exactly why the Student was flagged (High velocity + Counterparty country).

---

### Phase 3: The Multi-Layered Shield (Intelligent Decisioning)
*Goal: Transparency in the 'Black Box'.*

1. **The Live Pipeline**: Open the **"AML_Shield_Orchestration"** flow in **SAS Intelligent Decisioning**.
2. **Step Through the Layers**:
   - **Stage 1 (Exclusions)**: Point to the "White List" filter. "We saved our analysts from reviewing 2,000 government-backed transactions here."
   - **Stage 2 (Real-time Features)**: Show the Python node calculating the 7-day velocity.
   - **Stage 4 (Regulatory Overlay)**: Open the Lookup table for `aml_country_risk`. "Notice how transactions from High-Risk jurisdictions automatically receive a risk weight bump."
3. **The 'Global Alert Value'**: Show how the final score is a weighted average of Model, Country, and PEP risk. 

---

### Phase 4: Final Disposition
*Goal: Closing the Loop.*

1. Return to the **Visual Analytics Alert Dashboard**.
2. **Resolution**: Present the evidence to the audience. "We have high-confidence detection (XGBoost) combined with Regulatory context (Country Risk). We can now file a SAR with complete confidence."

---

## Key Business Takeaways
- **Precision**: Reducing false positives by 40% through Champion/Challenger testing.
- **Explainability**: Moving from "Black Box" detection to a multi-layered, auditable shield.
- **Agility**: Changing reporting thresholds via Lookups (Stage 4) without writing a single line of code.
- **Efficiency**: Filtering out low-risk throughput in Stage 1 to focus on real threats.
