# SAS Viya 4 BFSI AML Demo: Advanced Setup Guide

This guide provides deep-dive, click-by-click instructions to implement the **Multi-Layered Shield** AML demonstration.

## ⚙️ Step 0: Synthetic Data Generation
*Goal: Generate the 75,000 transaction dataset with embedded AML typologies.*

1. **Prerequisites**: Ensure you have Python installed with the `pandas` and `numpy` libraries.
2. **Action**: Open your terminal (PowerShell or Bash) and run:
   ```bash
   python scripts/data_generator.py
   ```
3. **Outcome**: This creates 10 CSV files in the `data/` folder, including `aml_transactions.csv`.

---

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
    /* Connect to CAS and assign the PUBLIC libref */
    cas mysess;
    libname Public cas caslib="Public";
    /* 🧠 Step 2.1: Clear any existing copies (Double-drop for maximum compatibility) */
    proc casutil incaslib="Public" quiet;
       droptable casdata="AML_ABT";
       droptable casdata="AML_ABT";
    run;

    /* 🧠 Step 2.2: Create the Analytic Base Table in session scope */
    proc fedsql sessref=mysess;
       create table Public.AML_ABT {options replace=true} as
       select 
          t.*, 
          a.customer_id as acc_cust_id, 
          c.name, c.segment, c.kyc_risk_rating, c.nationality, c.profession, c.expected_monthly_turnover,
          (t.amount / c.expected_monthly_turnover) as turnover_ratio
       from Public.aml_transactions as t
       left join Public.aml_accounts as a on t.account_id = a.account_id
       left join Public.aml_customers as c on a.customer_id = c.customer_id;
    quit;

    /* 🧠 Step 2.3: Promote to Global Scope */
    proc casutil incaslib="Public" outcaslib="Public";
       promote casdata="AML_ABT";
    run;
    quit;
   ```
4. **Validation**: Check the **Log** tab for "NOTE: The data set PUBLIC.AML_ABT has 75000 observations".

---

## 🧠 Step 3: Champion/Challenger Strategy (Model Studio)
*Goal: Train multiple models to detect complex "Smurfing" and "Velocity" patterns.*

1. **Navigate**: Click **Applications Menu** -> **Build Models** (Model Studio).
2. **Create Project**:
   - Click **New Project**.
   - **Data**: Click **Browse** -> Select `Public.AML_ABT`.
   - **Variables**: Go to the **Data** tab. Click on each variable to set the correct **Role** and **Level**.
     
     | Variable Name | Role | Level | Note |
     | :--- | :--- | :--- | :--- |
     | **suspicious_flag** | **Target** | **Binary** | The outcome variable to predict |
     | **expected_monthly_turnover** | Input | **Interval** | *Crucial: Set to Interval for numeric range* |
     | **kyc_risk_rating** | Input | **Interval** | *Crucial: Set to Interval for numeric range* |
     | **amount** | Input | Interval | |
     | **turnover_ratio** | Input | Interval | |
     | **counterparty_country** | Input | Nominal | |
     | **nationality** | Input | Nominal | |
     | **profession** | Input | Nominal | |
     | **segment** | Segment | Nominal | |
     | **ACC_CUST_ID**, **account_id** | Rejected / ID | Nominal | Exclude unique IDs from training |
     | **name**, **counterparty_name** | Rejected / ID | Nominal | Exclude identifiers |
     | **tx_id**, **tx_date** | Rejected / ID | Nominal | Exclude transaction metadata |
     | **typology** | **Rejected** | Nominal | *Crucial: Exclude labels to avoid data leakage* |
3. **Build Pipeline**:
   - Click the **Pipelines** tab.
   - Click `+` on the Data node -> **Add Node** -> **Supervised Learning** -> **Logistic Regression**.
   - Click `+` on the Data node -> **Add Node** -> **Supervised Learning** -> **Gradient Boosting**.
4. **Run & Publish**:
   - Click **Run Pipeline**.
   - Once complete, go to the **Pipeline Comparison** tab.
   - Click the **Champion** column to verify the preferred model (usually Gradient Boosting).
   - Select the champion model -> **Publish** -> **SAS Micro Analytic Service**.

---

## 🛡️ Step 4: The 5-Stage Shield (Intelligent Decisioning)
*Goal: Orchestrate model scores and regulatory lookups into a final risk decision.*

### 🛠️ Step 4.1: Create Velocity Logic (DS2)
*To avoid Python environment configuration errors, we use DS2 (SAS native high-performance language) for our code logic.*

1. **Navigate**: Click **Applications Menu** -> **Manage Decisions**.
2. **Create Code File**:
   - Click the **Code Files** tab in the left sidebar.
   - Click **New Code File**.
   - **Name**: `AML_Velocity_Logic` | **Type**: `DS2 code file`.
   - **Location**: `/Public`.
   - Click **Save**.
3. **Variable Settings**: (Auto-populated from code, but verify in the Variables tab):
   - `turnover_ratio`: Decimal (Input)
   - `velocity_flag`: Decimal (Output)
4. **Paste Code**: Click the **Code** tab, paste the logic below, and click **Save**:
   ```ds2
   package "${PACKAGE_NAME}" /inline;
       method execute(double turnover_ratio, in_out double velocity_flag);
           /* Threshold: Flag if transaction consumes > 70% of expected monthly turnover */
           if (turnover_ratio > 0.7) then velocity_flag = 1;
           else velocity_flag = 0;
       end;
   endpackage;
   ```

### 🛠️ Step 4.2: Create Lookup Tables
*In SAS SID, lookups must be imported and activated before they can be used in rules.*

1. **Navigate**: Click **Applications Menu** -> **Manage Decisions**.
2. **Create PEP Table**:
   - Click the **Lookup Tables** tab in the sidebar.
   - Click **New Lookup Table**.
   - **Name**: `AML_PEP_CHECK`.
   - Click **Save**.
   - Click **Import** -> Select `data/aml_pep_list_lookup.csv`.
   - Click **Activate**.
3. **Create Country Risk Table**:
   - Click **New Lookup Table**.
   - **Name**: `AML_COUNTRY_RISK_CHECK`.
   - Click **Save**.
   - Click **Import** -> Select `data/aml_country_risk_lookup.csv`.
   - Click **Activate**.

### 🛠️ Step 4.3: Create Advanced Scoring Logic (DS2)
*To achieve a high-fidelity 'Shield' and reduce false-positive noise, we use an additive weighted scoring model.*

1. **Navigate**: **Manage Decisions** -> **Code Files** -> **New Code File**.
2. **Name**: `AML_Advanced_Scoring` | **Type**: `DS2 code file`.
3. **Paste Logic**:
   ```sas
   package "${PACKAGE_NAME}" / inline;
        method execute(
            double EM_EVENTPROBABILITY,
            varchar is_pep,
            varchar country_risk_level,
            double amount,
            double turnover_ratio,
            in_out double Global_Alert_Value,
            in_out varchar Alert_Priority
        );
            dcl double base_score;
            dcl double risk_additives;

           /* 1. Model Contribution (Scaled 0-50) */
           base_score = EM_EVENTPROBABILITY * 50;

           /* 2. Risk Overlays (Additives) */
           risk_additives = 0;
           if (trim(is_pep) = 'High' or trim(is_pep) = 'YES') then risk_additives = risk_additives + 25;
           if (trim(country_risk_level) = 'High') then risk_additives = risk_additives + 25;
           if (turnover_ratio > 0.7) then risk_additives = risk_additives + 15;

           /* 3. Final Calculation */
           Global_Alert_Value = base_score + risk_additives;
           if (Global_Alert_Value >= 90) then Alert_Priority = 'URGENT';
           else if (Global_Alert_Value >= 70) then Alert_Priority = 'High';
           else Alert_Priority = 'Medium';
       end;
   endpackage;
   ```
4. **Note**: This weighted approach ensures only "Multi-Layered" risks reach the `URGENT` threshold.

### 🛠️ Step 4.4: Build the Decision Flow
1. **New Decision**: Name it `AML_Shield_Orchestration`.
2. **Add Workflow Stages**:
   - **Stage 1 (Regulatory Checks - Rule Set)**:
     - Click the `+` icon after **Start** -> Select **Add Rule Set**.
     - Search and select `AML_Regulatory_Checks` -> Click **Add**.
   - **Stage 2 (Velocity - Code)**:
     - Click `+` after the rule set -> Select **Add Code File**.
     - Select `AML_Velocity_Logic`.
   - **Stage 3 (AI Brain - Model)**:
     - Click `+` -> Select **Add Model**.
     - Select your Champion Model.
   - **Stage 4 (Shield - Code)**:
     - Click `+` -> Select **Add Code File**.
     - Select `AML_Advanced_Scoring`.
3. **Logic Mapping & Verification**: 
   - **Mapping**: Click the `AML_Advanced_Scoring` node. 
     - Ensure `EM_EVENTPROBABILITY` (from Stage 3) is mapped.
     - Ensure `is_pep` and `country_risk_level` (from Stage 1) are mapped to the respective inputs.
   - **Outputs**: Map `Global_Alert_Value` and `Alert_Priority` as **Output** variables for the whole decision.


4. **Finalize**: 
   - Click the **Properties** tab of the Decision.
   - Ensure the **Output variables** list includes `Global_Alert_Value` and `Alert_Priority`.
   - Click **Validate**. You should see a green success message (0 errors).
   - Click **Publish** -> Select **maslocal**.

### 🧪 Step 4.5: Testing and Simulation
*Goal: Manually trigger the decision flow to verify alerting logic and visualize the processing path.*

1. **Navigate**: Inside the `AML_Shield_Orchestration` decision, click the **Scoring** tab (top-level menu).
2. **Create Test**:
   - Click **Tests** in the left sidebar -> Click **New Test**.
   - **Name**: `Manual_Shield_Simulation`.
   - **Data**: Click **Browse** -> Select `Public.AML_ABT`.
   - **Variables**: The UI will auto-map decision variables to table columns. Verify that `name`, `nationality`, `amount`, and `turnover_ratio` are mapped.
3. **Run Simulation**:
   - Click **Run** at the top.
   - Wait for the **Status** to change to a green checkmark (Completed).
4. **Visualize the Results**:
   - Click the **Results** icon (the chart/graph icon) in the test row.
   - **Output Variables**: Click the `Output Variables` tab. Look for `Global_Alert_Value` and `Alert_Priority`. Verify that "URGENT" alerts are being generated.
   - **Path Tracking (Magic Visualizer)**: 
     - Click **Decision Path** in the left sidebar of the results.
     - Select a specific record (row).
     - **Visual Flow**: This shows exactly which nodes in your 5-Stage Shield were executed. It will highlight your DS2 Velocity node, your ML Model, and your DS2 Scoring node in sequence.
     - **Rule Logic**: Click the node to see the input/output transformation at each stage.

---

## 📊 Step 5: Investigator Dashboard (Visual Analytics)
*Goal: Create a high-impact triage interface using the scoring results.*

1. **Verify Results Table**:
   - In **Intelligent Decisioning** -> **Scoring** -> **Tests**, find your successful test.
   - Click the **Results** icon.
   - Go to the **Output Variables** tab and confirm `alert_priority` and `Global_Alert_Value` are present.
   - **Note**: The decision does not modify the raw `AML_ABT` table. It creates a new "Output" table.

2. **Navigate**: Click **Applications Menu** -> **Explore and Visualize**.
3. **Data**: Add the **Output table** from your test (e.g., `Manual_Shield_Simulation_..._output`).
4. **Layout & Dashboarding**:
   - **Key Value Object (The "Triage Counter")**:
     - *Action*: Drag a **Key Value** object to the top of the canvas.
     - *Data Role*: Add `Frequency` (or any measure) to the **Measure** role.
     - *Remove Lattice*: If `Alert_Priority` was added to "Lattice category" by default, click the **X** to remove it. (You want one big number, not two boxes).
     - *Apply Filter*:
       - Click the **Filters** icon (funnel) on the right sidebar.
       - Click **+ New filter** -> Select `Alert_Priority`.
       - Select **only** the checkbox for **URGENT**.
     - *Styling*: In the **Options** pane, set the color to **Red** and the data label to "URGENT ALERTS".
    - **Network Analysis Object** (Investigation View):
      - *Source Role*: `counterparty_name`
      - *Target Role*: `account_id`
      - *Link Color Role*: `Global_Alert_Value` (Click **Options** -> **Links** -> Set Gradient to Yellow -> Orange -> Deep Red).
      - *Link Width Role*: `amount` (Highlights high-value movement).
    - **Slider Control (Critical for Noise Filtering)**:
      - Place a **Slider** at the top.
      - *Role*: `Global_Alert_Value`.
      - *Action*: In the **Filters** pane, set the default to **85 to 100**.
      - **Talk Track**: *"By sliding the threshold to 90+, we instantly cut through the noise of standard high-risk country matches and isolate the rare 'Multi-Layered' anomalies like our High-Risk Student."*

5. **Action**: Click **Save** as "AML Compliance Command Center".

---

## 🛠️ Troubleshooting Common Issues

### ❌ Error: "MAS host access mode specified requires an authenticated host account"
*   **Cause**: This happens when a code node (like `AML_Velocity_Logic`) is created as a **Python** file. The SAS Micro Analytic Service (MAS) requires specific authentication for Python that isn't always active.
*   **Solution**: 
    1. Delete the Python code file.
    2. Recreate it as a **DS2 code file** (see [Step 4.1](#-step-41-create-velocity-logic-ds2)). 
    3. Update your Decision Flow to use the new DS2 version.

### ⚠️ Symptom: Global Alert Value is stuck at 0.38 (or 100)
*   **Cause**: The Analytics Model is missing one or more required inputs (like `kyc_risk_rating`), triggering its "Fallback" probability.
*   **Solution**: 
    1. Go to the **Scoring** tab of your decision.
    2. Open your **Test** (e.g., `Manual_Shield_Simulation`).
    3. Click the **Variables** button.
    4. Ensure every variable is mapped to a column in the `Public.AML_ABT` table. If any say "None", select the matching column name manually.
    5. Save and rerun the test.

---
**Setup Complete!** You are now ready to perform the [User Walkthrough Guide](./User_Walkthrough.md).
