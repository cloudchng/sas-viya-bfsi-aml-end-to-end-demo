# SAS Viya 4 AML Demo: Professional End-to-End Walkthrough Guide

This guide provides a granular, click-by-click script for demonstrating the **Multi-Layered Shield** AML solution. Use this guide to deliver a compelling narrative that balances technical depth with business impact.

---

## 🚀 Pre-Flight Checklist
*Ensure these are ready before you start the demo:*
1.  **Data**: Verify `Public.AML_ABT` and your decision output tables are loaded in CAS.
2.  **Models**: Ensure the **Gradient Boosting/Logistic Regression** model is published to the MAS destination.
3.  **Decisions**: Ensure `AML_Shield_Orchestration` is active and a recent scoring test has been run.
4.  **Reports**: Open the **AML Compliance Command Center** in SAS Visual Analytics.

---

## 📍 Phase 1: Interactive Discovery (Visual Analytics)
**Goal**: Identify a complex anomaly (The 'High-Risk Student') that traditional rules would miss.

1.  **Dashboard Entry**: Open the **AML Compliance Command Center** report.
    - **Talk Track**: *"Welcome to our AML Command Center. Unlike legacy systems that flood you with alerts, our 'Multi-Layered Shield' uses five distinct stages to filter noise. Out of 100,000 transactions, we've distilled the risk down to precisely 3 urgent cases."*
2.  **Stage 1 Proof Point**: Point to the **Frequency Count (3)** at the top.
    - **Action**: Point to the large red '3' on the dashboard.
    - **Talk Track**: *"Look at this focus. By the time we reach Stage 5, we have moved from a sea of data to just 3 high-impact anomalies that require immediate attention."*
3.  **Anatomy of an Alert**:
    - **Action**: In the **Profession** list filter on the left, select **'Student'**.
    - **Interaction**: Observe the **Network Diagram** and the **Global Alert Value** bar chart updating.
    - **Talk Track**: *"Look at this specific cluster. We have a student who, historically, should have low transactional activity. Suddenly, our system has assigned them a Global Alert Value of 100. Why?"*
4.  **Network Context**: 
    - **Action**: Hover over the largest bubble in the **Network Diagram** (e.g., Account `ACC_01198`).
    - **Visual Outcome**: Pop-up shows `Global_Alert_Value: 100` and an amount of approximately `$454,198`.
    - **Talk Track**: *"Take a look at Account ACC_01198. It has been assigned a perfect risk score of 100. It's not just the $454k amount; our system has cross-referenced its high-velocity behavior and geopolitical risk in real-time."*

---

## 🔬 Phase 2: AI-Driven Investigation (Model Studio)
**Goal**: Explain the 'intelligence' behind the alert using Model Interpretability.

1.  **The Pipeline**: Switch to **SAS Model Studio** and open the **AML_Model_Triage** project.
2.  **Comparison View**: Click on the **Pipeline Comparison** tab.
    - **Action**: Highlight the gap between the **Logistic Regression (Champion)** and the **Gradient Boosting (Challenger)**.
    - **Talk Track**: *"Our legacy rules engine missed this. Even our Champion Logistic model was borderline. But our AI 'Challenger' caught the 'Smurfing' pattern—a series of deposits designed to fly just under the radar."*
3.  **Explaining the 'Why'**: 
    - **Action**: Right-click the **Gradient Boosting/Logistic Regression** node -> **Results**.
    - **Action**: Navigate to **Node** -> **Variable Importance**.
    - **Visual Cue**: See `Turnover_Ratio` and `Velocity_7D` at the top of the chart.
    - **Talk Track**: *"This isn't a black box. The model tells us exactly why it's suspicious: it’s the inconsistency between the student's stated income and their 7-day velocity."*

---

## 🛡️ Phase 3: The Multi-Layered Shield (Intelligent Decisioning)
**Goal**: Show the orchestration logic and the **Decision Path**.

1.  **Logic Flow**: Open **SAS Intelligent Decisioning** -> **AML_Shield_Orchestration**.
    - **Action**: View the **Decision Flow** tab. Point out the Python node, Model node, and Rule Set.
    - **Talk Track**: *"This is our 'Shield' in code. It orchestrates real-time velocity calculations, our AI model scores, and regulatory lookups into one unified decision flow."*
2.  **The 'Magic' Visualizer (Decision Path Tracking)**:
    - **Action**: Click the **Scoring** tab -> Click on your latest **Test** -> Click the **Execution Results** (graph) icon.
    - **Action**: In the left sidebar, expand **Decision Path Tracking** -> Click **Analysis and Plot**.
    - **Action**: In the table that appears, select a row with a **High Global Alert Value** (this represents our 'Student' anomaly).
    - **Visual Outcome**: The entire flow diagram on the right will highlight in color, showing exactly which nodes were triggered.
    - **Talk Track**: *"I can show you exactly why this alert was generated. Look at the highlighted path: It hit our DS2 velocity threshold, was scored by the model, and finally, Stage 5's rule set pushed it to 'URGENT'. Total transparency for regulators."*

---

## 🏁 Phase 4: Final Disposition
**Goal**: Move from insight to evidence-based filing.

1.  **Return to VA**: Open the **Alert Disposition** tab.
    - **Action**: Click the checkbox for the **Urgent Student Alert**.
    - **Action**: Click the **"File SAR"** (Suspicious Activity Report) button simulation.
    - **Talk Track**: *"We've gone from raw transactional data to a high-confidence, evidence-backed SAR filing in minutes. All in a single, unified environment on SAS Viya."*

---

## 💡 Demo Pro-Tips
- **Anchor to Persona**: Always refer back to "The Student" throughout the flow to keep the audience grounded in the story.
- **The "Magic" Moment**: Spend extra time on the **Decision Path**. It is usually the "Wow" moment for compliance executives who are used to black-box systems.
- **The Slider Moment**: Use the **Global Alert Value Slider** in VA to show how you can "dial down the noise" in real-time.

