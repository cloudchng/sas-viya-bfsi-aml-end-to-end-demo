# SAS Viya 4 BFSI AML End-to-End Demo

![SAS Viya Architecture](https://img.shields.io/badge/Platform-SAS%20Viya%204-blue?style=for-the-badge&logo=sas)
![Use Case](https://img.shields.io/badge/Use%20Case-AML%20Triage-green?style=for-the-badge)
![Decisioning](https://img.shields.io/badge/Strategy-5--Stage%20Shield-orange?style=for-the-badge)

## 🎯 Project Overview
This repository contains a comprehensive, high-fidelity Anti-Money Laundering (AML) demonstration built for the latest **SAS Viya 4** platform. 

Unlike basic detection demos, this project implements a **Multi-Layered Shield** decisioning workflow. It simulates the complex triage process used by global financial institutions to balance regulatory compliance with operational efficiency.

### The 5-Stage "Multi-Layered Shield"
1.  **🚀 Pre-qualification (Exclusions)**: Immediate screening against trusted entity lists to reduce false positives.
2.  **⚙️ Real-time Feature Engineering**: Dynamic calculation of behavioral signals (e.g., 24h/7d velocity) within the decision flow.
3.  **🤖 Hybrid Detection (Champion/Challenger)**: A side-by-side comparison of explainable Logistic Regression and high-performance XGBoost models.
4.  **🗺️ Regulatory Overlay**: Geographic risk scoring and Politically Exposed Person (PEP) cross-referencing.
5.  **⚖️ Weighted Orchestration**: Calculation of a `Global_Alert_Value` to prioritize urgent investigations.

---

## 📂 Project Structure
```text
├── data/                   # Synthetic and Reference CSV datasets
│   ├── aml_customers.csv   # Core customer profile data
│   ├── aml_accounts.csv    # Account-level information
│   ├── aml_transactions.csv# 75,000+ synthetic transactions
│   ├── aml_exclusions.csv  # [New] Trusted entity reference data
│   ├── aml_country_risk.csv# [New] high-risk jurisdiction mapping
│   ├── aml_pep_list.csv    # [New] PEP reference list
│   └── ...                 # Watchlists and Risk History
├── docs/                   # Step-by-step implementation guides
│   ├── Setup_Guide.md      # Technical roadmap for implementation
│   └── User_Walkthrough.md # Sales/Success narrative for the demo
├── scripts/                # Automation and utilities
│   └── data_generator.py   # Python script to regenerate all assets
└── README.md               # You are here
```

---

## 🛠️ Quick Start

### 1. Requirements
- **SAS Viya 4** (Latest Release)
- **Python 3.x** (with `pandas` and `numpy` for data generation)

### 2. Generate Data
If you need to refresh the synthetic datasets, run the generator script:
```bash
python scripts/data_generator.py
```

### 3. Follow the Guides
- **Step 1: Implementation**: Follow the [Setup Guide](./docs/Setup_Guide.md) to upload data, train models, and configure the Intelligent Decisioning flow.
- **Step 2: Delivery**: Follow the [User Walkthrough](./docs/User_Walkthrough.md) to present the story of a Compliance Officer investigating complex "High Velocity" and "Income Inconsistency" typologies.

---

## 📊 Key Highlights
- **No SAS Visual Investigator? No Problem.**: This demo is architected to perform complete triage using **SAS Intelligent Decisioning** and **SAS Visual Analytics**.
- **Champion/Challenger Support**: Out-of-the-box support for demonstrating model performance comparisons.
- **Enterprise Grade Logic**: Uses Lookups, DS2/Python nodes, and weighted risk scoring to simulate true complexity.

---
