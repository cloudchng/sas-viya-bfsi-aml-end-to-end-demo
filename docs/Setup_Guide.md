# SAS Viya 4 BFSI AML Demo: Setup Guide

This guide provides step-by-step instructions to implement a modern Anti-Money Laundering (AML) demonstration on the latest **SAS Viya 4** platform.

## Prerequisites
- **SAS Viya 4** (Latest Release)
- **Licensed Components**: SAS Visual Analytics, SAS Model Studio (VDMML), SAS Intelligent Decisioning.
- *Note: This demo is designed for environments without SAS Visual Investigator.*

---

## Step 1: Data Ingestion & Reference Assets
The synthetic data is located in the `/data` directory. We use a combination of transactional data and regulatory reference tables.

1. **Upload CSVs**: Log in to SAS Viya and open **SAS Drive**.
2. **Import to CAS**:
   - Go to **Manage Data** (SAS Data Explorer).
   - Import the following core files into the `Public` Caslib:
     - `aml_customers.csv`
     - `aml_accounts.csv`
     - `aml_transactions.csv`
     - `aml_watchlist.csv`
     - `aml_risk_history.csv`
   - **Import Reference Data** (for the Multi-Layered Shield):
     - `aml_exclusions.csv`: Trusted entities to skip screening.
     - `aml_country_risk.csv`: High-risk jurisdiction mapping (Risk Scores 0-100).
     - `aml_pep_list.csv`: Politically Exposed Persons (PEPs).

---

## Step 2: Data Preparation (SAS Studio)
To build a high-quality model, we need a flattened Analytic Base Table (ABT) that includes behavioral features.

1. Open **SAS Studio**.
2. **Join Core Tables**:
   ```sas
   /* Example SAS Code for Enhanced ABT */
   data Public.AML_ABT;
     merge Public.aml_transactions(in=a) 
           Public.aml_accounts(in=b rename=(customer_id=acc_cust_id))
           Public.aml_customers(in=c);
     by account_id;
     
     /* Feature Engineering for Peer Comparison */
     turnover_ratio = amount / expected_monthly_turnover;
     if a;
   run;
   ```

---

## Step 3: Advanced Modeling (Model Studio)
Implement a **Champion/Challenger** strategy to show the evolution from basic heuristics to advanced AI.

1. **Create the Champion Model**:
   - Build a **Logistic Regression** node (Standard, interpretable method).
   - Set as "Champion".
2. **Create the Challenger Model**:
   - Build an **XGBoost** or **Gradient Boosting** node.
   - Fine-tune to detect "Velocity Abuse" and "Income Inconsistency" typologies.
3. **Compare & Publish**:
   - Use the **Model Comparison** node.
   - Publish the winning model to the **SAS Micro Analytic Service (MAS)** or **CAS Pipeline**.

---

## Step 4: The 5-Stage "Multi-Layered Shield" (SAS Intelligent Decisioning)
This is the core of the demo. Construct a decision named `AML_Shield_Orchestration`.

### Stage 1: Pre-qualification (Exclusions)
- **Node**: Rule Set or Filter.
- **Logic**: Check `account_id` or `customer_id` against `aml_exclusions.csv`.
- **Action**: If matched, set `Alert_Status = 'SKIP'` and terminate flow.

### Stage 2: Real-time Feature Engineering
- **Node**: Python or DS2 Code Node.
- **Logic**: Calculate 24-hour velocity or 7-day average spend within the decision flow (simulating streaming capabilities).

### Stage 3: Hybrid Detection (AI + Rules)
- **Model Node**: Invoke the **Champion/Challenger** model from Stage 3.
- **Rule Set Node**: Heuristics for "Low Amount Smurfing" (e.g., `amount between 9000 and 9999`).

### Stage 4: Regulatory Overlay (Lookups)
- **Lookup Node 1**: Check `country_code` in `aml_country_risk`. Get `Country_Risk_Score`.
- **Lookup Node 2**: Check `FullName` in `aml_pep_list`. Get `PEP_Risk_Multiplier`.

### Stage 5: Weighted Orchestration
- **Node**: Rule Set.
- **Logic**: Calculate `Global_Alert_Value`.
  - `Global_Alert_Value = (Model_Score * 0.5) + (Country_Risk_Score * 0.3) + (PEP_Multiplier * 0.2)`.
- **Threshold**: `IF Global_Alert_Value > 70 THEN Alert_Priority = 'URGENT'`.

---

## Step 5: Dashboarding (SAS Visual Analytics)
Create the "Investigator Portal" to close the loop.

1. **Visuals**:
   - **Key Value**: Count of 'URGENT' alerts.
   - **Network Diagram**: Visualize `customer_id` connections to PEPs or High-Risk countries.
   - **Scenario Analysis**: A slider to adjust the `Global_Alert_Value` threshold and see how many "Normal" customers would be flagged.

---
**Setup Complete!** You can now proceed to the [User Walkthrough Guide](./User_Walkthrough.md).
