# Beyond Simple Rules: Building a Multi-Layered Shield for AML on SAS Viya 4

### A Technical Deep-Dive for Data Scientists and Analytics Engineers

In the world of Anti-Money Laundering (AML), we are fighting a war of attrition. Traditional rules-based systems are drowning compliance teams in a sea of false positives, with some institutions reporting that over 95% of alerts are "noise." For the modern Data Scientist, the challenge isn't just about building a better model; it's about building a better *decisioning lifecycle*.

This article breaks down a high-fidelity end-to-end AML demonstration built on the **SAS Viya 4** platform. We move away from siloed detection and toward what we call the **"Multi-Layered Shield"**—a 5-stage orchestration flow that integrates real-time feature engineering, hybrid AI modeling, and weighted risk scoring.

---

## 🏗️ The Architecture: Cloud-Native Analytics at Scale

To replicate this demo, it's essential to understand the underlying engine: **SAS Cloud Analytic Services (CAS)**. CAS is a distributed, in-memory engine that allows us to perform massive joins and scoring without the I/O bottlenecks of legacy systems.

Our architecture leverages:
- **SAS Intelligent Decisioning**: For logic orchestration.
- **SAS Model Studio**: For automated Champion/Challenger model pipelines.
- **SAS Visual Analytics**: For the investigator’s "Command Center" dashboard.

---

## 🛡️ The 5-Stage Multi-Layered Shield

### Stage 1: Pre-qualification (Exclusions)
Efficiency starts with knowing whom *not* to investigate. We implement a "First Pass" exclusion set using trusted entity lists (e.g., government payrolls, internal utility transfers). By filtering these out first, we instantly reduce the downstream load on both our models and our analysts.

### Stage 2: In-Memory Feature Engineering (FedSQL)
In AML, behavioral context is everything. We don't just look at a transaction in isolation; we need to know its relationship to the customer's historical behavior. Using **FedSQL**, we join 75,000+ synthetic transactions with customer metadata in real-time.

```sas
/* FedSQL: Joining transactions with Customer Metadata in CAS */
proc fedsql sessref=mysess;
   create table Public.AML_ABT {options replace=true} as
   select 
      t.*, 
      c.name, c.segment, c.kyc_risk_rating, c.profession, c.expected_monthly_turnover,
      (t.amount / c.expected_monthly_turnover) as turnover_ratio
   from Public.aml_transactions as t
   left join Public.aml_accounts as a on t.account_id = a.account_id
   left join Public.aml_customers as c on a.customer_id = c.customer_id;
quit;
```
*Note: The `turnover_ratio` created here becomes a powerful signal for our Gradient Boosting model.*

### Stage 3: Advanced Detection (Champion vs. Challenger)
We move beyond static rules into **Hybrid Detection**. In this demo, we pit a traditional **Logistic Regression** (Champion) against a high-performance **Gradient Boosting** (Challenger) model. 

While the Logistic model is excellent for catching obvious outliers, the Gradient Boosting model excels at detecting **"Smurfing"**—the practice of breaking large sums of money into smaller transactions to evade the $10,000 reporting threshold.

### Stage 4: Regulatory Enrichment (DS2 & Lookups)
Complex risk requires complex logic. We use **DS2**, a SAS-native high-performance language, to calculate behavioral flags like "Velocity surges" during the decision flow.

```ds2
/* DS2 Logic: Real-time Velocity Flagging */
package "${PACKAGE_NAME}" /inline;
    method execute(double turnover_ratio, in_out double velocity_flag);
        /* Identify if transaction exceeds 70% of expected monthly turnover */
        if (turnover_ratio > 0.7) then velocity_flag = 1;
        else velocity_flag = 0;
    end;
endpackage;
```
We then cross-reference the customer against high-risk jurisdiction lookups and PEP (Politically Exposed Person) lists to add a "Regulatory Overlay."

### Stage 5: Risk Contextualization (Weighted Scoring)
Final triage is handled by calculating a `Global_Alert_Value`. We don't just alert; we prioritize. A transaction that is flagged by the AI *and* connects to a high-risk jurisdiction is automatically assigned an **URGENT** priority, ensuring it hits the top of the analyst queue immediately.

---

## 🕵️ Narrative: The "High-Risk Student" Anomaly

To see the system in action, look at the "Student" typology in our demo data. 
- **The Pattern**: A customer with the profession "Student" and a low KYC risk rating suddenly starts moving $500,000 USD via high-velocity transactions.
- **The Detection**: 
    1. **Stage 2** flags the turnover ratio as extreme.
    2. **Stage 3** (The Gradient Boosting model) identifies the "Income Inconsistency."
    3. **Stage 4** finds a connection to a sanctioned jurisdiction ("Oligarch Holdings").
- **The Result**: The `Global_Alert_Value` hits 100 on Account `ACC_01198` ($454k transaction), and the case is filed with a complete audit trail. In fact, our system distilled over 100,000 transactions down to just **3 urgent alerts**—allowing the analyst to focus on the highest probability risks immediately.

---

## 🚀 Deployment: From Insight to Action

In SAS Viya, the transition from dev to prod is seamless. We publish our decision flow to the **SAS Micro Analytic Service (MAS)**, exposing it as a REST endpoint that can be called by banking core systems in sub-second response times.

The final results are visualized in a **Visual Analytics Investigator Dashboard**, featuring a Network Diagram that exposes hidden links between customers and high-risk counterparties.

---

## 🏁 Conclusion: The Shift to Decisioning-as-Code

The **Multi-Layered Shield** represents a paradigm shift from reactive rules to proactive, AI-driven orchestration. By integrating feature engineering and regulatory logic directly into the decision flow, we reduce noise, enhance detection, and ultimately protect the financial system more effectively.

### 🔗 Explore the Repository
Ready to replicate this? All synthetic data, SAS code, and guides are available here:
[**SAS Viya BFSI AML End-to-End Demo**](https://github.com/cloudchng/sas-viya-bfsi-aml-end-to-end-demo)