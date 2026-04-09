# SAS Viya 4 BFSI AML Demo: Advanced Setup Guide

This guide provides deep-dive, click-by-click instructions to implement the **Multi-Layered Shield** AML demonstration.

## 🛠️ Step 1: Data Ingestion (SAS Data Explorer)
*Goal: Load core banking and regulatory reference tables into memory (CAS).*

1. **Navigate**: Click the **Applications Menu** (hamburger icon, top-left) -> **Manage Data**.
2. **Import Core Data**:
   - Click the **Import** tab.
   - Select **Local files** -> **Microsoft Excel/CSV**.
   - Upload the core files: `aml_customers.csv`, `aml_accounts.csv`, `aml_transactions.csv`, `aml_watchlist.csv`, `aml_risk_history.csv`.
   - **Target Location**: Select `Public` as the Caslib.
   - Click **Import Item** for each file.
3. **Import Reference Data**:
   - Repeat for: `aml_exclusions.csv`, `aml_country_risk.csv`, `aml_pep_list.csv`.
4. **Validation**: Click the **Available** tab. Search for "aml_". You should see all 8 tables with a green checkmark indicating they are loaded in memory.

---

## 🏗️ Step 2: ABT Engineering (SAS Studio)
*Goal: Join relational tables into a single Analytic Base Table (ABT).*

1. **Navigate**: Click **Applications Menu** -> **Develop SAS Code** (SAS Studio).
2. **Setup**:
   - Expand **Libraries** -> **Public** in the left pane.
   - Right-click the `Public` library -> **New Program**.
3. **Action**: Paste the following script and click the **Run** icon (Running Man):
   ```sas
   data Public.AML_ABT;
     merge Public.aml_transactions(in=a) 
           Public.aml_accounts(in=b rename=(customer_id=acc_cust_id))
           Public.aml_customers(in=c);
     by account_id;
     turnover_ratio = amount / expected_monthly_turnover;
     if a;
   run;
   ```
4. **Validation**: Check the **Log** tab for "NOTE: The data set PUBLIC.AML_ABT has 75000 observations".

---

## 🧠 Step 3: Champion/Challenger Strategy (Model Studio)
*Goal: Train multiple models to detect complex "Smurfing" and "Velocity" patterns.*

1. **Navigate**: Click **Applications Menu** -> **Build Models** (Model Studio).
2. **Create Project**:
   - Click **New Project**.
   - **Data**: Click **Browse** -> Select `Public.AML_ABT`.
   - **Target**: Set `suspicious_flag` as the Target variable.
3. **Build Pipeline**:
   - Click the **Pipelines** tab.
   - Click `+` on the Data node -> **Add Node** -> **Supervised Learning** -> **Logistic Regression** (Champion).
   - Click `+` on the Data node -> **Add Node** -> **Supervised Learning** -> **XGBoost** (Challenger).
4. **Run & Publish**:
   - Right-click Logistic Regression -> **Set as Champion**.
   - Click **Run Pipeline**.
   - Once complete, click the **Pipeline Comparison** tab.
   - Select the XGBoost model -> **Publish** -> **SAS Micro Analytic Service**.

---

## 🛡️ Step 4: The 5-Stage Shield (Intelligent Decisioning)
*Goal: Orchestrate model scores and regulatory lookups into a final risk decision.*

1. **Navigate**: Click **Applications Menu** -> **Manage Decisions**.
2. **New Decision**: Click **New Decision**, name it `AML_Shield_Orchestration`.
3. **Configure Stages**:
   - **Stage 1 (Exclusion)**: Add a **Rule Set**. Logic: `IF customer_id IN aml_exclusions THEN Alert_Status = 'SKIP'`.
   - **Stage 2 (Velocity)**: Add a **Code Node** (Python). Paste logic to compare `amount` against 7-day averages.
   - **Stage 3 (AI Match)**: Add a **Model** node. Select the XGBoost model published in Step 3.
   - **Stage 4 (Regulatory Lookup)**: 
     - Add **Lookup** for `country_code` -> map to `aml_country_risk`.
     - Add **Lookup** for `FullName` -> map to `aml_pep_list`.
   - **Stage 5 (Prioritization)**: Add a **Rule Set** to calculate `Global_Alert_Value`.
4. **Variables**: Ensure `Global_Alert_Value` and `Alert_Priority` are set as **Output** variables.

---

## 📊 Step 5: Investigator Dashboard (Visual Analytics)
*Goal: Create a high-impact triage interface.*

1. **Navigate**: Click **Applications Menu** -> **Explore and Visualize**.
2. **Data**: Add `Public.AML_ABT`.
3. **Layout**:
   - **Key Value Object**: Drag to the top. Column: `Alert_Priority` (Count of 'URGENT').
   - **Network Diagram**: Drag to center. Roles: `customer_id` -> `counterparty_name`.
   - **Slider**: Map to `Global_Alert_Value`. This allows the user to see the "Alert Volume" shift in real-time.
4. **Action**: Click **Save** as "AML Compliance Command Center".

---
**Setup Complete!** You are now ready to perform the [User Walkthrough Guide](./User_Walkthrough.md).
