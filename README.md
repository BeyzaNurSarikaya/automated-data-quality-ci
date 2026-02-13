# Automated Data Quality CI Pipeline 🚀

This repository demonstrates a **Continuous Integration (CI)** pipeline designed for Data Engineers. It automatically validates incoming data on every `push` or `pull_request` using **Pydantic v2** and **GitHub Actions**.

## 🎯 The Problem & Solution

**The Problem:** Manually checking large datasets for inconsistencies (like negative quantities or wrong formats) is slow and prone to human error. Bad data often "leaks" into production.

**The Solution:** An automated "Gatekeeper." Before any code or data is merged, a GitHub Action runner executes a validation script. If the data doesn't meet the defined business rules, the **CI fails**, and the team is notified via **Slack** immediately.

## 🛠️ Tech Stack

* **Python 3.12:** Core logic.
* **Pydantic v2:** Row-level data validation and schema enforcement.
* **GitHub Actions:** Automated workflow orchestration.
* **Slack Webhooks:** Real-time incident alerting.
* **Pandas:** Efficient data handling.

## 🚀 Key Features

* **Self-Generating Test Data:** The pipeline includes a script that generates a sample `amazon_orders.csv` with intentional errors to test the system's resilience.
* **Zero-Leakage Policy:** The workflow is configured to return a non-zero exit code (`sys.exit(1)`) upon validation failure, effectively blocking the pipeline.
* **Secret Management:** Sensitive information like Slack Webhook URLs are handled securely using **GitHub Secrets**.

## 📋 Data Validation Rules

Every record must pass the following checks:

* `order_id`: Must be a valid string.
* `qty`: Must be an integer **** (Negative quantities trigger an alert).
* `amount`: Must be a float ****.
* `currency` & `ship_country`: Required fields for geographical reporting.

<img width="806" height="155" alt="Screenshot 2026-02-13 232326" src="https://github.com/user-attachments/assets/a436f6a9-4d9e-4aed-9b4f-81ea99d37f4f" />


## 🚨 Automated Alerting

When a commit contains invalid data, the system triggers a Slack notification:

> 🚨 **CI Data Quality Alert!**
> Found **1** invalid rows in commit.
> *Status: Pipeline Blocked*

<img width="731" height="205" alt="Screenshot 2026-02-13 233005" src="https://github.com/user-attachments/assets/5edb180b-2aee-4f33-a476-174666177a33" />

## 📂 Project Structure

```text
├── .github/workflows/
│   └── dq_validation.yml  # Pipeline definition
├── dq_pipeline.py         # Validation logic & data generator
├── requirements.txt       # Dependencies
└── README.md              # Documentation

```
<img width="722" height="620" alt="image" src="https://github.com/user-attachments/assets/9b3db12b-9337-4411-8038-1e345328dfd4" />

## ⚙️ How to Setup

1. Clone the repository.
2. Add your `SLACK_WEBHOOK_URL` to **GitHub Settings > Secrets > Actions**.
3. Push a change or run the workflow manually via the **Actions** tab.
