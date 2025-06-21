# Amharic E-commerce Data Extractor for FinTech Analysis 🚀

Transform unstructured Amharic e-commerce Telegram posts into structured business data for FinTech credit assessment.

---

## 📌 Table of Contents

- [Amharic E-commerce Data Extractor for FinTech Analysis 🚀](#amharic-e-commerce-data-extractor-for-fintech-analysis-)
  - [📌 Table of Contents](#-table-of-contents)
  - [🚀 Project Overview](#-project-overview)
    - [Business Need](#business-need)
    - [Technical Solution](#technical-solution)
  - [✨ Key Objectives](#-key-objectives)
  - [🛠️ Project Workflow](#️-project-workflow)
  - [📊 Dataset](#-dataset)
  - [⚙️ Getting Started: Full Development Environment Setup](#️-getting-started-full-development-environment-setup)
    - [1. GitHub Repository Setup](#1-github-repository-setup)

---

## 🚀 Project Overview

### Business Need

The Ethiopian e-commerce landscape is vibrant but fragmented, with the majority of transactions occurring across numerous independent Telegram channels. This decentralization creates challenges for buyers and sellers who must navigate multiple sources for discovery, communication, and transactions.

**EthioMart**, our envisioned platform, solves this by creating a centralized hub that aggregates real-time data from disparate Telegram channels, consolidating product listings, prices, and vendor information to provide a unified and seamless shopping experience.

### Technical Solution

At the core is a **custom-trained Named Entity Recognition (NER) model** fine-tuned on Amharic text to accurately identify and extract business-critical entities from Telegram posts. The structured data output populates the EthioMart database, turning messy unstructured text into a powerful tool for market analysis and financial assessment.

---

## ✨ Key Objectives

- **Automated Data Ingestion:** Develop a scalable, repeatable workflow to crawl and ingest data from a dynamic list of Amharic e-commerce Telegram channels.
- **High-Accuracy NER:** Fine-tune a state-of-the-art Large Language Model (LLM) to achieve high precision and recall in identifying PRODUCT, PRICE, and LOCATION entities.
- **Centralized Database:** Structure the extracted information to populate a centralized database powering EthioMart.
- **Actionable Insights:** Enable a FinTech engine to analyze vendor activity, sales volume, and market presence for creditworthiness scoring.

---

## 🛠️ Project Workflow

| Step                              | Description                                                                                          |
|----------------------------------|--------------------------------------------------------------------------------------------------|
| **Channel Identification**       | Maintain a curated list of Telegram e-commerce channels in `channels_to_crawl.csv`.               |
| **Data Ingestion**                | Scrape raw, unstructured posts from channels, stored in `telegram_data.csv`.                      |
| **Data Annotation**               | Manually or semi-automatically label tokens with IOB tags in `labeled_telegram_product_price_location.txt`. |
| **Model Fine-Tuning**             | Fine-tune a transformer-based model (e.g. mBERT, XLM-Roberta) on the labeled dataset for NER.     |
| **Model Evaluation & Interpretation** | Evaluate with precision, recall, F1; interpret predictions using SHAP and LIME.                    |
| **Inference & Database Population** | Use the fine-tuned model to extract entities from new posts; clean and load structured data into EthioMart database. |

---

## 📊 Dataset

| Filename                              | Description                                           | Sample Format                                 |
|-------------------------------------|-------------------------------------------------------|-----------------------------------------------|
| `channels_to_crawl.csv`              | List of Telegram channel URLs to scrape               | `channel_url`<br>`https://t.me/channel1`     |
| `telegram_data.csv`                  | Raw Telegram post data with metadata                   | `post_id,post_text,timestamp`<br>`123,"product info",2025-06-20T10:30:00` |
| `labeled_telegram_product_price_location.txt` | IOB-annotated tokens for training and evaluation        | `3pcs B-PRODUCT`<br>`silicon I-PRODUCT`<br>`brush I-PRODUCT`<br>`550ብር I-PRICE` |

---

## ⚙️ Getting Started: Full Development Environment Setup

### 1. GitHub Repository Setup

- **Fork the Repository**: Use the "Fork" button on GitHub to create your own copy.
- **Clone your Fork** (replace `your-username`):

```bash
git clone https://github.com/your-username/amharic-ecommerce-extractor.git
cd amharic-ecommerce-extractor
